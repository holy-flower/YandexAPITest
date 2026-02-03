import requests


class YandexApi:
    def __init__(self, base_url="https://cloud-api.yandex.net"):
        self.token = None
        self.base_url = base_url
        self.session = requests.Session()
        self.token_type = "OAuth"

    def authorize(self, token):
        self.token = token
        if self.token:
            self.session.headers.update({
                "Authorization": f"{self.token_type} {self.token}"
            })

        return bool(self.token)

    def get_disk_info(self):
        url = f"{self.base_url}/v1/disk"
        response = self.session.get(url)
        return response

    def upload_file(self, file_path, remote_path="/"):
        url = f"{self.base_url}/v1/disk/resources/upload"

        params = {
            "path": remote_path,
            "overwrite": True
        }

        response = self.session.get(url, params=params)
        if response.status_code != 200:
            return response

        upload_url = response.json().get("href")

        with open(file_path, 'rb') as file:
            upload_response = requests.put(upload_url, files={"file": file})

        return upload_response

    def list_files(self, path="/", limit=20):
        url = f"{self.base_url}/v1/disk/resources"

        params = {
            "path": path,
            "limit": limit
        }

        response = self.session.get(url, params=params)
        return response
