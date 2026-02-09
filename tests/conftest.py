import json
from datetime import datetime, timezone

import pytest
from loguru import logger

from tools.api_client import RestfulBookerClient
from tools.config import Config


@pytest.fixture(scope="session")
def test_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")


@pytest.fixture(scope="session", autouse=True)
def set_logger(test_timestamp: str):
    logger.add(f"logs/{test_timestamp}.log", mode="w")


@pytest.fixture(scope="session")
def config() -> Config:
    return Config()


@pytest.fixture
def api_client(config: Config) -> RestfulBookerClient:
    return RestfulBookerClient(base_url=config.base_url)


@pytest.fixture(autouse=True)
def server_health_check(api_client: RestfulBookerClient):
    response = api_client.health_check()
    try:
        response.raise_for_status()
    except Exception:
        pytest.exit(
            reason=f"Server {api_client.base_url} is not healthy: {response.text}"
        )


@pytest.fixture
def authenticated_client(config: Config) -> RestfulBookerClient:
    client = RestfulBookerClient(base_url=config.base_url)
    client.authenticate(username=config.auth_username, password=config.auth_password)
    return client

@pytest.fixture
def booking_data() -> dict:
    with open("data/booking_example.json") as fpread:
        return json.load(fpread)
