import os
import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--token",
        action="store",
        default=os.getenv("YANDEX_DISK_TOKEN"),
        help="Yandex disc OAuth token"
    )

@pytest.fixture
def token(request):
    """
    token_value = request.config.getoption("--token")

    if not token_value:
        try:
            with open(".token", "r") as f:
                token_value = f.read().strip()
        except FileNotFoundError:
            pass

    if not token_value:
        pytest.skip("Требуется OAuth-токен. Используйте --token или YANDEX_DISK_TOKEN")
    """

    token_value = "y0__xCSqK65BhjblgMgnq7Vpha78vjLLbS0bVlYXJGivA5ty2bdnw"
    return token_value

@pytest.fixture
def headers(token):
    return {
        "Authorization" : f"OAuth {token}",
        "Content-Type" : "application/json"
    }

@pytest.fixture
def BASE_URL():
    return "https://cloud-api.yandex.net"
