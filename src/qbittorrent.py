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

    def add_torrent(self, torrent_url, info_hash, category=None):
        if not self.is_torrent_present(info_hash):
            add_url = f"{self.base_url}/api/v2/torrents/add"
            data = {'urls': torrent_url}
            if category:
                data['category'] = category
            response = self.session.post(add_url, data=data)
            return response.ok
        else:
            print("Torrent is already present in the client.")
            return False

    def is_torrent_present(self, info_hash):
        list_url = f"{self.base_url}/api/v2/torrents/info"
        response = self.session.get(list_url)
        torrents = response.json()
        for torrent in torrents:
            if info_hash.lower() == torrent.get('hash').lower():  # Compare hashes in a case-insensitive manner
                return True
        return False
