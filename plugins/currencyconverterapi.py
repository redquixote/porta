import requests

__version__ = '0.1'


class Plugin:
    def __init__(self):
        self.uri = 'http://free.currencyconverterapi.com/api/v5/convert?q={pair}&compact=y'
        self.session = requests.Session()
        self.response = None
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        self.session.headers.update(self.HEADERS)
        self._json_options = {}

    def get_current_value(self, symbol):
        # Uses USD_EUR format.
        urlpath = self.uri.format(pair=symbol)
        self.response = self.session.get(urlpath, timeout=None)
        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()
        return(float(self.response.json(**self._json_options)[symbol]['val']))
