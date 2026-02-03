from unittest.mock import patch, Mock
import pytest
from yandex_disc import YandexApi

class TestYandexDisc:
    def test_authorization(self):
        client = YandexApi()

        with patch.object(client.session, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"access_token": "y0__test_token"}

            mock_post.return_value = mock_response

            response = client.authorize("y0__xCSqK65BhiIuz0g_5uOpRaImZY0ipTP5hBOn_mWg7CwhISymw")

            assert response is True




