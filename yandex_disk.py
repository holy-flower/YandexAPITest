import requests
from typing import Optional, Dict, Any

class YandexApi:
    def __init__(self,
                 token: Optional[str] = None,
                 headers: Optional[Dict] = None,
                 base_url: Optional[str] = None):
        self.base_url = base_url,

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
        return response.status_code in [201, 204]

    def get_resource_info(self, path: str) -> Dict[str, Any]:
        url = f"{self.base_url}/v1/disk/resources"
        params = {"path" : path}

        respopnse = requests.get(url, headers=self.headers, params=params)
        respopnse.raise_for_status()
        return respopnse.json()

