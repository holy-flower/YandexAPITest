import requests

from yandex_disk import YandexApi


class TestYandexDisk:
    def test_get_disk_info(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)
        data = client.get_disk_info()

        assert "total_space" in data
        assert "used_space" in data
        assert data["used_space"] <= data["total_space"]

    def test_create_folder(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        folder_path = "/test_folder"

        try:
            client.delete_resource(folder_path, permanently=True)
        except:
            pass

        assert client.create_folder("/test_folder") is True

    def test_upload_file(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        folder_path = "/test_upload_file"
        file_path = f"{folder_path}/test.txt"
        file_content = b"Hello Yandex"

        try:
            client.delete_resource(folder_path, permanently=True)
        except Exception:
            pass

        assert client.create_folder(folder_path) is True
        assert client.upload_file(file_path, file_content) is True

    def test_delete_resource(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        assert client.delete_resource("test_folder", permanently=True) is True

    def test_file_move(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        source_folder = "/test_source_folder"
        target_folder = "/test_target_folder"

        try:
            assert client.delete_resource(source_folder, permanently=True) is True
            assert client.delete_resource(target_folder, permanently=True) is True
        except:
            pass

        assert client.create_folder(source_folder) is True
        assert client.create_folder(target_folder) is True

        source_file = f"{source_folder}/test_file.txt"
        file_content = b"Test content for moving"
        assert client.upload_file(source_file, file_content) is True

        target_file = f"{target_folder}/moved_test.txt"
        assert client.file_move(source_file, target_file, overwrite=False) is True


