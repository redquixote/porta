import requests

__version__ = '0.1'


class Plugin:
    def __init__(self):
        self.uri = 'https://api.iextrading.com/1.0/stock/{symbol}/batch?types=quote'
        self.session = requests.Session()
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        self.session.headers.update(self.HEADERS)
        self.response = None
        self._json_options = {}
        self.MAPPING = {}

    def get_current_value(self, symbol):
        url = self.uri.format(symbol=symbol)
        self.response = self.session.get(url)
        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()
        # uses "close" price (not "open"):
        return(float(self.response.json(**self._json_options)['quote']['close']))
