import requests

class OTWAPIWrapper:
	def __init__(self, api_token):
		self.base_url = 'https://oldtoons.world'
		self.api_token = api_token
		self.session = requests.Session()
		self.session.headers.update({'Accept': 'application/json'})

	def get_torrents(self, per_page=25):
		# Passing token as a query string
		response = self.session.get(f'{self.base_url}/api/torrents?api_token={self.api_token}&perPage={per_page}')
		return response.json()

	def upload_torrent(self, torrent_details):
		# Passing token in the request's form parameters
		torrent_details['api_token'] = self.api_token
		response = self.session.post(f'{self.base_url}/api/torrents/upload', files=torrent_details)
		return response.json()

	def get_specific_torrent(self, torrent_id):
		# Using the Bearer token
		self.session.headers.update({'Authorization': f'Bearer {self.api_token}'})
		response = self.session.get(f'{self.base_url}/api/torrents/{torrent_id}')
		return response.json()

	# Add more methods as needed to interact with other API endpoints
