import time
from http import HTTPStatus
from uuid import uuid4

import pytest

from tools.api_client import RestfulBookerClient


@pytest.fixture(scope="module")
def booking_data() -> dict:
    return {
        "firstname": "Pytest",
        "lastname": uuid4().hex,
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2025-10-20", "checkout": "2025-10-25"},
        "additionalneeds": "Breakfast",
    }


@pytest.mark.parametrize("field_to_update,new_value", [
    ("firstname", "Python"),
    ("additionalneeds", "Lunch"),
    ("totalprice", 200),
])
def test_booking_lifecycle_with_field_update(
    authenticated_client: RestfulBookerClient,
    booking_data: dict,
    field_to_update: str,
    new_value,
):
    """Test complete booking lifecycle: create, update specific field, verify persistence.
    
    Args:
        field_to_update: The field to update during the lifecycle
        new_value: The new value for the field
    """
    create_booking_response = authenticated_client.booking_create(booking_data)
    assert create_booking_response.status_code == HTTPStatus.OK
    booking_id = create_booking_response.json()["bookingid"]
    time.sleep(2)

    updated_booking_data = {**booking_data, field_to_update: new_value}
    update_response = authenticated_client.booking_update(
        booking_id=booking_id,
        booking_data=updated_booking_data,
    )
    assert update_response.status_code == HTTPStatus.OK

    get_updated_booking_response = authenticated_client.booking_get_by_id(booking_id)
    assert get_updated_booking_response.status_code == HTTPStatus.OK

    retrieved_booking = get_updated_booking_response.json()
    assert retrieved_booking[field_to_update] == new_value
    assert retrieved_booking == updated_booking_data
