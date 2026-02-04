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
        data = response.json()

        assert response.status_code == 200
        assert "total_space" in data
        assert "used_space" in data
        assert data["used_space"] <= data["total_space"]

    def test_create_folder(self, headers):
        url = f"{self.BASE_URL}/v1/disk/resources"
        params = {"path" : "/test_folder"}

        requests.delete(url, headers=headers, params=params)
        response = requests.put(url, headers=headers, params=params)

        data = response.json()

        assert response.status_code == 201
        assert "method" in data
        assert "href" in data
        assert "templated" in data







