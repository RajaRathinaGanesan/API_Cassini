from http import HTTPStatus

import pytest

from tools.api_client import RestfulBookerClient


@pytest.mark.parametrize("expected_status,assertion_type", [
    (HTTPStatus.OK, "equal"),
    (HTTPStatus.CREATED, "not_equal"),
])
def test_create_booking(
    authenticated_client: RestfulBookerClient,
    booking_data: dict,
    expected_status: HTTPStatus,
    assertion_type: str,
):
    """Test booking creation with different status code assertions.
    
    Args:
        expected_status: The HTTP status code to validate against
        assertion_type: "equal" for successful creation, "not_equal" for error case
    """
    create_response = authenticated_client.booking_create(booking_data)
    
    if assertion_type == "equal":
        assert create_response.status_code == expected_status
    else:
        assert create_response.status_code != expected_status
