from http import HTTPStatus

import pytest

from tools.api_client import RestfulBookerClient


@pytest.fixture(scope="module")
def booking_data() -> list[dict]:
    return [
        {
            "firstname": "User1",
            "lastname": "LastName1",
            "totalprice": 50,
            "depositpaid": True,
            "bookingdates": {"checkin": "2026-10-20", "checkout": "2026-10-25"},
            "additionalneeds": "Breakfast",
        },
        {
            "firstname": "User2",
            "lastname": "LastName2",
            "totalprice": 150,
            "depositpaid": True,
            "bookingdates": {"checkin": "2025-12-20", "checkout": "2025-12-25"},
            "additionalneeds": "Breakfast,Dinner",
        },
        {
            "firstname": "User2",
            "lastname": "LastName3",
            "totalprice": 120,
            "depositpaid": False,
            "bookingdates": {"checkin": "2026-01-20", "checkout": "2026-10-25"},
            "additionalneeds": "Breakfast,Wifi",
        },
    ]


@pytest.fixture
def create_bookings(
    authenticated_client: RestfulBookerClient, booking_data: list[dict]
):
    booking_ids = []
    for booking in booking_data:
        response = authenticated_client.booking_create(booking)
        response.raise_for_status()
        booking_ids.append(response.json()["bookingid"])
    return booking_ids


@pytest.mark.parametrize("search_filter,min_expected_results", [
    ({"firstname": "User1"}, 1),
    ({"firstname": "User2"}, 2),
    ({"lastname": "LastName3"}, 1),
    ({"depositpaid": True}, 2),
    ({"depositpaid": False}, 1),
])
@pytest.mark.usefixtures("create_bookings")
def test_booking_search_by_filter(
    authenticated_client: RestfulBookerClient,
    search_filter: dict,
    min_expected_results: int,
):
    """Test booking search with various filter combinations.
    
    Args:
        search_filter: Search parameters to filter bookings
        min_expected_results: Minimum number of bookings expected in results
    """
    get_response = authenticated_client.booking_ids_get_all(params=search_filter)
    assert get_response.status_code == HTTPStatus.OK

    found_booking_ids = get_response.json()
    assert len(found_booking_ids) >= min_expected_results
    assert isinstance(found_booking_ids, list)
