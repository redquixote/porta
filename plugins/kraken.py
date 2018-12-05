import requests

__version__ = '0.1'


class Plugin:
    def __init__(self):
        self.uri = 'https://api.kraken.com'
        self.apiversion = '0'
        self.session = requests.Session()
        self.HEADERS = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        self.session.headers.update(self.HEADERS)
        self.response = None
        self._json_options = {}
        self.MAPPING = {
            'XBTUSD': 'XXBTZUSD',
            'XBTGBP': 'XXBTZGBP',
            'BSVUSD': 'BSVUSD',
            'BCHUSD': 'BCHUSD',
            'ETHUSD': 'XETHZUSD',
        }
        return

    def get_current_value(self, symbol):
        method = 'Ticker'
        params = 'pair={0}'.format(symbol)
        data = None
        if data is None:
            data = {}
        urlpath = '/' + self.apiversion + '/public/' + method + '?' + params
        url = self.uri + urlpath
        self.response = self.session.post(
            url, data = data, headers=None, timeout = None)
        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()

        request_symbol = self.MAPPING[symbol]
        return(float(self.response.json(**self._json_options)['result'][request_symbol]['c'][0]))

# TODO next: colours and other currencies and clean up this kk
