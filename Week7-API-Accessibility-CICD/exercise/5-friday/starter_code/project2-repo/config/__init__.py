"""Single source of configuration. Everything comes from environment variables with local defaults."""
import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str
    user: str
    password: str
    admin_user: str
    admin_password: str
    timeout: float
    api_mode: str          # "live" (default) or "mock"
    require_api: bool      # True -> unreachable API is a hard failure instead of a skip
    price_api_url: str


def load_settings() -> Settings:
    e = os.getenv
    return Settings(
        base_url=e("BASE_URL", "http://127.0.0.1:8000").rstrip("/"),
        user=e("API_USER", "tester"),
        password=e("API_PASSWORD", "tester123"),
        admin_user=e("API_ADMIN_USER", "admin"),
        admin_password=e("API_ADMIN_PASSWORD", "admin123"),
        timeout=float(e("API_TIMEOUT", "5")),
        api_mode=e("API_MODE", "live").lower(),
        require_api=e("REQUIRE_API", "0") == "1",
        price_api_url=e("PRICE_API_URL", "https://prices.example.test"),
    )
