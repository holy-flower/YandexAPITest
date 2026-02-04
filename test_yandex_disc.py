from unittest.mock import patch, Mock
import pytest
import requests

from yandex_disc import YandexApi

class TestYandexDisc:
    BASE_URL = "https://cloud-api.yandex.net"

    @pytest.fixture
    def headers(self):
        return {
            "Authorization" : "OAuth y0__xCSqK65BhjblgMgnq7Vpha78vjLLbS0bVlYXJGivA5ty2bdnw",
            "Content-Type" : "application/json"
        }

    def test_get_disk_info(self, headers):
        response = requests.get(f"{self.BASE_URL}/v1/disk/", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert "total_space" in data
        assert "used_space" in data







