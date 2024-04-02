import requests

class QBittorrentWrapper:
    def __init__(self, base_url, username, password):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        # Set common headers for all requests
        self.session.headers.update({
            'Referer': self.base_url,
            'Origin': self.base_url,
        })
        self.username = username
        self.password = password
        self.login()

    def login(self):
        login_url = f"{self.base_url}/api/v2/auth/login"
        response = self.session.post(login_url, data={'username': self.username, 'password': self.password})
        # Use a more flexible way to check if the login is successful
        if 'Ok.' not in response.text:
            raise Exception(f"Failed to log in to qBittorrent Web UI: {response.text}")

    def add_torrent(self, torrent_url, category=None):
        add_url = f"{self.base_url}/api/v2/torrents/add"
        data = {'urls': torrent_url}
        if category:  # Add the category if specified
            data['category'] = category
        response = self.session.post(add_url, data=data)
        return response.status_code == 200