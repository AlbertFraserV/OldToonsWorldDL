from OTWAPIWrapper import OTWAPIWrapper
from qbittorrent import QBittorrentWrapper
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
import sys

load_dotenv()

api_key = os.environ['OTW_API_KEY']
api = OTWAPIWrapper(api_key)

qbit_user = os.environ['QBIT_USER']
qbit_pass = os.environ['QBIT_PASS']
qbit_url = os.environ['QBIT_URL']
qbit = QBittorrentWrapper(qbit_url, qbit_user, qbit_pass)

torrents = api.get_torrents()
for torrent in torrents['data']:
    torrent_fl = torrent['attributes']['freeleech']
    torrent_name = torrent['attributes']['name']
    provided_timestamp_str = torrent['attributes']['created_at']
    provided_timestamp = datetime.strptime(provided_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

    current_timestamp = datetime.utcnow()
    if (current_timestamp - provided_timestamp > timedelta(hours=1)) and torrent_fl != '100%':
        # print(f"{torrent_name} - {torrent_fl}")
        continue

    torrent_link = torrent['attributes']['download_link']
    qbit.add_torrent(torrent_link, 'Upload Grinding')
    