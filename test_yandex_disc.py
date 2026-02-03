from unittest.mock import patch, Mock

from yandex_disc import YandexApi

class test_yandex_disc:
    def test_authorization(self):
        client = YandexApi()

        with patch.object(client, 'ensure_token', return_value=True):
            with patch.object(client.session, 'post') as mock_post:
                mock_post.return_value = Mock(status_code=200)

                response = client.authorize("y0__xCSqK65BhiIuz0g_5uOpRaImZY0ipTP5hBOn_mWg7CwhISymw")

                assert response is True
                assert response.status_code==200


