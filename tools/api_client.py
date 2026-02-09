from typing import Any

import requests
from loguru import logger
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class RestfulBookerClient(requests.Session):
    def __init__(
        self,
        base_url: str,
        default_timeout=10,
        max_retries=3,
        status_to_retry: list[int] | None = None,
        verify_ssl=True,
        *args,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.base_url = base_url
        self.default_timeout = default_timeout
        self.max_retries = max_retries
        self.status_to_retry = status_to_retry or [429, 502, 503, 504]
        self.verify_ssl = verify_ssl
        logger.info(f"Initialising a session for {self.base_url}")

    def _request_with_retry(
        self, method: str, endpoint: str, max_retries: int, **kwargs
    ) -> requests.Response:
        retry_strategy = Retry(
            total=max_retries,
            status_forcelist=self.status_to_retry,
            allowed_methods=[
                "HEAD",
                "GET",
                "POST",
                "PUT",
                "DELETE",
                "OPTIONS",
                "TRACE",
            ],
            backoff_factor=1,
            read=0,
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.mount("https://", adapter)
        self.mount("http://", adapter)

        try:
            logger.debug(
                f"Sending {method} {endpoint} with payload: "
                f"{kwargs.get('data') or kwargs.get('json')}"
            )
            response = super().request(method, endpoint, **kwargs)
            logger.debug(f"Request sent to {response.request.url}")
            logger.debug(
                (
                    f"Response status code: <{response.status_code}>;"
                    f"Elapsed time: {response.elapsed.total_seconds()} seconds;"
                    f"Content: {response.content};"
                )
            )
            return response
        except requests.exceptions.RetryError as e:
            logger.error(f"{max_retries} Max retry is reached")
            raise e
        except requests.exceptions.SSLError as e:
            logger.error(f"SSL ERROR: {e}")
            raise e
        except Exception as e:
            logger.error(f"Other exceptions are caught: {e}")
            raise e

    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        prefixed_url = "/".join([self.base_url.strip("/"), endpoint.strip("/")])
        kwargs["timeout"] = kwargs.get("timeout", self.default_timeout)
        kwargs["verify"] = kwargs.get("verify", self.verify_ssl)
        response = self._request_with_retry(
            method, prefixed_url, self.max_retries, **kwargs
        )
        return response

    def authenticate(self, username: str, password: str):
        """Get authentication to update or delete bookings"""
        response = self.post("/auth", json={"username": username, "password": password})
        response.raise_for_status()
        token = response.json()["token"]
        self.cookies.update({"token": token})

    def booking_ids_get_all(
        self, params: dict[str, Any] | None = None
    ) -> requests.Response:
        """Get all bookings."""
        return self.get("/booking", params=params)

    def booking_get_by_id(self, booking_id: int) -> requests.Response:
        """Get specific booking by ID."""
        return self.get(f"/booking/{booking_id}")

    def booking_create(self, booking_data: dict[str, Any]) -> requests.Response:
        """Create a new booking."""
        return self.post("/booking", json=booking_data)

    def booking_update(
        self, booking_id: int, booking_data: dict[str, Any]
    ) -> requests.Response:
        """Update an existing booking."""
        return self.put(f"/booking/{booking_id}", json=booking_data)

    def booking_update_partial(
        self, booking_id: int, booking_data: dict[str, Any]
    ) -> requests.Response:
        """Partially update an existing booking."""
        return self.patch(f"/booking/{booking_id}", json=booking_data)

    def health_check(self) -> requests.Response:
        """Check API health."""
        return self.get("/ping")
