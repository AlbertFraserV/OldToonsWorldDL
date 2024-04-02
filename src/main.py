from OTWAPIWrapper import OTWAPIWrapper
from qbittorrent import QBittorrentWrapper
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
import os

def download_new_freeleach(debug=True):
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
        torrent_hash = torrent['attributes']['info_hash']

        provided_timestamp_str = torrent['attributes']['created_at']
        provided_timestamp = datetime.strptime(provided_timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        provided_timestamp = provided_timestamp.replace(tzinfo=timezone.utc)  # Make it timezone-aware

        current_timestamp = datetime.now(timezone.utc)
        if (current_timestamp - provided_timestamp > timedelta(hours=1)) or torrent_fl != '100%':
            # If the torrent is older than 1 hour or not 100% freeleech, skip it
            continue

        torrent_link = torrent['attributes']['download_link']
        if not debug:
            qbit.add_torrent(torrent_link, torrent_hash, 'Upload Grinding')
        else:
            print(f"{torrent_name} - {torrent_fl}")

if __name__ == '__main__':
    download_new_freeleach(False)
