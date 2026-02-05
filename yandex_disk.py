import time

import requests
from typing import Optional, Dict, Any

class YandexApi:
    def __init__(self,
                 token: Optional[str] = None,
                 headers: Optional[Dict] = None,
                 base_url: Optional[str] = None):
        self.base_url = base_url

        if headers:
            self.headers = headers
        elif token:
            self.headers = {
                "Authorization" : f"OAuth {token}",
                "Content-Type" : "application/json"
            }
        else:
            raise ValueError("Требуется либо token, либо headers")

    def get_disk_info(self) -> Dict[str, Any]:
        response = requests.get(f"{self.base_url}/v1/disk", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def create_folder(self, path: str) -> bool:
        url = f"{self.base_url}/v1/disk/resources"
        params = {"path" : path}

        response = requests.put(url, headers=self.headers, params=params)
        return response.status_code == 201

    def upload_file(self, path: str, file_content: bytes) -> bool:
        url = f"{self.base_url}/v1/disk/resources/upload"
        params = {
            "path": path,
            "overwrite": True
        }

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        upload_url = response.json()["href"]
        put_response = requests.put(upload_url, data=file_content)
        return put_response.status_code == 201

    def delete_resource(self, path: str, permanently: bool) -> bool:
        url = f"{self.base_url}/v1/disk/resources"
        params = {
            "path" : path,
            "permanently" : str(permanently).lower()
        }

        response = requests.delete(url, headers=self.headers, params=params)

        if response.status_code == 202:
            operation_href = response.json()["href"]

            while True:
                op_status = requests.get(operation_href, headers=self.headers).json()
                if op_status["status"] == "success":
                    break
                elif op_status["status"] == "failed":
                    raise Exception("Delete operation failed")
                time.sleep(1)

        return response.status_code in [201, 202, 204]

    def get_resource_info(self, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/disk/resources"
        params = {"path" : path}

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def file_move(self, from_res: str, path: str, overwrite: bool) -> bool:
        url = f"{self.base_url}/v1/disk/resources/move"
        params = {
            "from" : from_res,
            "path" : path,
            "overwrite" : overwrite
        }

        response = requests.post(url, headers=self.headers, params=params)
        print(f"Move status: {response.status_code}")
        print(f"Move response: {response.text}")

        return response.status_code in [201, 202]

    def publish_resources(self, path: str) -> bool:
        url = f"{self.base_url}/v1/disk/resources/publish"
        params = {"path" : path}

        response = requests.put(url, headers=self.headers, params=params)

        return response.status_code == 200

    def get_public_resource(self, public_key: str) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/disk/public/resources"
        params = {"public_key" : public_key}

        response = requests.get(url, params=params)
        response.raise_for_status()

        return response.json()

    def get_trash_resource_info(self, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/disk/trash/resources"
        params = {"path" : path}

        response = requests.get(url, headers=self.headers, params=params)
        assert response.status_code == 200
        return response.json()

    def restore_resource_from_trash(self, path: str, overwrite: bool) -> bool:
        url = f"{self.base_url}/v1/disk/trash/resources/restore"
        params = {
            "path" : path,
            "overwrite" : str(overwrite).lower()
        }

        response = requests.put(url, headers=self.headers, params=params)
        #return response.status_code in (201, 202)
        if response.status_code not in (201, 202):
            print(f"Failed to restore {path}: {response.status_code}, {response.text}")
            return False
        return True

    def wait_for_trash_resource(self, path: str, timeout: int = 30):
        url = f"{self.base_url}/v1/disk/trash/resources"
        params = {"path": path}

        for _ in range(timeout):
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                time.sleep(1)
            else:
                response.raise_for_status()
        raise Exception(f"Resource {path} did not appear in trash after {timeout} seconds")


