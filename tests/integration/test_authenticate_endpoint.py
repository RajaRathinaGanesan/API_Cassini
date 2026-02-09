import time
from http import HTTPStatus

import pytest
from requests.exceptions import RequestException

from tools.api_client import RestfulBookerClient
from tools.config import Config


@pytest.fixture
def creds(config: Config) -> tuple[str, str]:
    return config.auth_username, config.auth_password


def test_authenticate_success_sets_token_cookie(api_client: RestfulBookerClient, creds: tuple[str, str]):
    """Authenticate with valid credentials and verify a token is returned and cookie can be set."""
    username, password = creds
    resp = api_client.post("/auth", json={"username": username, "password": password})
    assert resp.status_code == HTTPStatus.OK
    token = resp.json().get("token")
    assert token is not None and isinstance(token, str) and len(token) > 0

    # exercise the client's authenticate helper to set cookie
    api_client.authenticate(username=username, password=password)
    assert api_client.cookies.get("token") is not None


def test_authenticate_invalid_credentials_handled(api_client: RestfulBookerClient):
    """Invalid credentials should be handled gracefully; API may return a reason field."""
    resp = api_client.post("/auth", json={"username": "baduser", "password": "badpass"})
    # API sometimes returns 200 with a reason, or a 4xx. Ensure it does not return a token.
    if resp.status_code == HTTPStatus.OK:
        assert "token" not in resp.json()
        assert "reason" in resp.json()
    else:
        assert resp.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN)


def test_update_requires_auth_then_succeeds(api_client: RestfulBookerClient, creds: tuple[str, str]):
    """Create a booking, verify update without auth is rejected, then authenticate and update succeeds."""
    booking_payload = {
        "firstname": "AuthTest",
        "lastname": "User",
        "totalprice": 10,
        "depositpaid": False,
        "bookingdates": {"checkin": "2025-05-01", "checkout": "2025-05-02"},
        "additionalneeds": "None",
    }
    try:
        create_resp = api_client.booking_create(booking_payload)
        create_resp.raise_for_status()
    except RequestException as exc:
        pytest.skip(f"Network error creating booking: {exc}")

    booking_id = create_resp.json()["bookingid"]

    try:
        update_payload = {**booking_payload, "firstname": "NoAuthUpdate"}
        update_resp = api_client.booking_update(booking_id=booking_id, booking_data=update_payload)

        assert update_resp.status_code in (
            HTTPStatus.UNAUTHORIZED,
            HTTPStatus.FORBIDDEN,
            HTTPStatus.METHOD_NOT_ALLOWED,
        )

        # authenticate and retry
        username, password = creds
        api_client.authenticate(username=username, password=password)
        update_resp2 = api_client.booking_update(booking_id=booking_id, booking_data=update_payload)
        assert update_resp2.status_code == HTTPStatus.OK

    finally:
        # cleanup - best-effort
        try:
            api_client.authenticate(username=creds[0], password=creds[1])
            api_client.delete(f"/booking/{booking_id}")
        except Exception:
            pass
