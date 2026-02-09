from http import HTTPStatus

import pytest

from tools.api_client import RestfulBookerClient


@pytest.fixture
def example_booking_id(authenticated_client: RestfulBookerClient, booking_data: dict):
    response = authenticated_client.booking_create(booking_data)
    response.raise_for_status()
    return response.json()["bookingid"]


@pytest.mark.parametrize("field_name,new_value,static_assertions", [
    ("firstname", "UpdatedFirstName", {"lastname": "Doep", "additionalneeds": "Breakfast"}),
    ("additionalneeds", "Breakfast, Wifi", {"firstname": "Johny", "lastname": "Doep"}),
])
def test_booking_update_field_successful(
    authenticated_client: RestfulBookerClient,
    booking_data: dict,
    example_booking_id: int,
    field_name: str,
    new_value: str,
    static_assertions: dict,
):
    """Test updating individual booking fields and verify persistence."""
    booking_data.update({field_name: new_value})
    update_response = authenticated_client.booking_update(
        booking_id=example_booking_id,
        booking_data=booking_data,
    )
    assert update_response.status_code == HTTPStatus.OK

    get_response = authenticated_client.booking_get_by_id(example_booking_id)
    assert get_response.status_code == HTTPStatus.OK

    updated_booking_data = get_response.json()
    assert updated_booking_data[field_name] == new_value
    for field, expected_value in static_assertions.items():
        assert updated_booking_data[field] == expected_value
