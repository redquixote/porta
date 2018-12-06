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
        self.MAPPING = {
            'USDEUR': 'USD_EUR',
            'USDGBP': 'USD_GBP',
            'EURUSD': 'EUR_USD',
            'EURGBP': 'EUR_GBP',
            'GBPUSD': 'GBP_USD',
            'GBPEUR': 'GBP_EUR',
            'JPYUSD': 'JPY_USD',
            'JPYEUR': 'JPY_EUR',
            'JPYGBP': 'JPY_GBP',
            'AUDUSD': 'AUD_USD',
            'AUDEUR': 'AUD_EUR',
            'AUDGBP': 'AUD_GBP',
            'CADUSD': 'CAD_USD',
            'CADEUR': 'CAD_EUR',
            'CADGBP': 'CAD_GBP',
            'SGDUSD': 'SGD_USD',
            'SGDEUR': 'SGD_EUR',
            'SGDGBP': 'SGD_GBP',
            'GBPCOP': 'GBP_COP',
            'USDCOP': 'USD_COP',
            'EURCOP': 'EUR_COP',
        }

    def get_current_value(self, symbol):
        # Uses USD_EUR format.
        request_symbol = self.MAPPING[symbol]
        urlpath = self.uri.format(pair=request_symbol)
        self.response = self.session.get(urlpath, timeout=None)
        if self.response.status_code not in (200, 201, 202):
            self.response.raise_for_status()
        return(float(self.response.json(**self._json_options)[request_symbol]['val']))
