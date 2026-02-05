import time
import uuid

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

        assert client.create_folder("/test_folder")

    def test_upload_file(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        folder_path = "/test_upload_file"
        file_path = f"{folder_path}/test.txt"
        file_content = b"Hello Yandex"

        try:
            client.delete_resource(folder_path, permanently=True)
        except Exception:
            pass

        assert client.create_folder(folder_path)
        assert client.upload_file(file_path, file_content)

    def test_delete_resource(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        assert client.delete_resource("test_folder", permanently=True)

    def test_file_move(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        source_folder = "/test_source_folder"
        target_folder = "/test_target_folder"

        try:
            assert client.delete_resource(source_folder, permanently=True)
            assert client.delete_resource(target_folder, permanently=True)
        except:
            pass

        assert client.create_folder(source_folder)
        assert client.create_folder(target_folder)

        source_file = f"{source_folder}/test_file.txt"
        file_content = b"Test content for moving"
        assert client.upload_file(source_file, file_content)

        target_file = f"{target_folder}/moved_test.txt"
        assert client.file_move(source_file, target_file, overwrite=False)

    def test_get_public_resource(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        test_folder = "/folder_test"
        test_file = f"{test_folder}/test_file.txt"
        file_content = b"Test content for public"

        try:
            assert client.delete_resource(test_folder, permanently=True)
        except:
            pass

        assert client.create_folder(test_folder)
        assert client.upload_file(test_file, file_content)
        assert client.publish_resources(test_file)

        file_info = client.get_resource_info(test_file)
        public_key = file_info["public_key"]

        public_file = client.get_public_resource(public_key)

        assert "name" in public_file
        assert "size" in public_file

    def test_restore_trash(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        test_folder = f"/new_folder_{uuid.uuid4()}"
        test_file = f"{test_folder}/new_tile.txt"
        file_content = b"Text for trash"

        assert client.create_folder(test_folder)
        assert client.upload_file(test_file, file_content)
        assert client.delete_resource(test_folder, permanently=False)

        try:
            trash_info = client.wait_for_trash_resource(test_folder)
        except Exception:
            assert not client.restore_resource_from_trash(test_folder, overwrite=True)
        else:
            assert client.restore_resource_from_trash(test_folder, overwrite=True)
            info = client.get_resource_info(test_folder)
            assert info["type"] == "dir"

    def test_upload_file_to_disk(self, headers, BASE_URL):
        client = YandexApi(headers=headers, base_url=BASE_URL)

        new_folder = f"/new_folder_{uuid.uuid4()}"
        new_file = f"{new_folder}/new_file.txt"
        url_file = "https://raw.githubusercontent.com/github/gitignore/main/Python.gitignore"

        assert client.create_folder(new_folder)

        assert client.upload_file_to_disk(new_file, url_file)


