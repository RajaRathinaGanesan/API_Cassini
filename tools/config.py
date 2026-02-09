import os
import tomllib
from pathlib import Path


class Config:
    DEFAULT_CONFIG_PATH = Path(__file__).resolve().parents[1] / "config.toml"

    def __init__(self, config_toml_path: str | Path | None = None):
        with open(config_toml_path or Config.DEFAULT_CONFIG_PATH, "rb") as fpread:
            self.config_data = tomllib.load(fpread)

    @property
    def base_url(self) -> str:
        return os.getenv("API_BASE_URL") or self.config_data["base_url"]
    @property
    def auth_username(self) -> str:
        return os.getenv("API_AUTH_USERNAME") or self.config_data.get("auth_username")

    @property
    def auth_password(self) -> str:
        return os.getenv("API_AUTH_PASSWORD") or self.config_data.get("auth_password")