"""porta
Usage:
    porta
    porta fx <curr_pair> [<value>]
    porta -h|--help
    porta -v|--version

Options:
    <cur>  Optional currency exchange mode.
    -h --help  Show this screen.
    -v --version  Show version.
"""

from docopt import docopt
import sys
import os
from configobj import ConfigObj
from terminaltables import AsciiTable
from colorclass import (
    Color,
)
import locale
import requests_cache
from datetime import timedelta

INIT_FILE = '~/.config/porta.ini'
PLUGINS = '/plugins/'

# setup
curr_dir = os.path.dirname(os.path.realpath(__file__))
cache_db_file = curr_dir + '/' + 'porta_cache'
locale.setlocale(locale.LC_ALL, '' )
filename = os.path.expanduser(INIT_FILE)
try:
    config = ConfigObj(filename)
except Exception as e:
    print('ERROR parsing ini file: ' + filename + ':\n' + str(e))
    # raise
    sys.exit(1)
#
# Plugins using Requests will be cached for CACHE_EXPIRE_HOURS hours:
cache_expire_hours = int(config.get('cache_hours', 2))
requests_cache.install_cache(cache_db_file, expire_after=timedelta(hours=cache_expire_hours))
#

# Load Plugins
path = os.path.abspath(curr_dir + PLUGINS)
plugins = {}
sys.path.insert(0, path)
for f in os.listdir(path):
    fname, ext = os.path.splitext(f)
    if ext == '.py':
        mod = __import__(fname)
        plugins[fname] = mod.Plugin()
sys.path.pop(0)


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if args['fx']:
        curr_pair = args['<curr_pair>']
        req_value = args['<value>'] if '<value>' in args else False
        currency_plug = plugins['currencyconverterapi']
        try:
            curr_val = currency_plug.get_current_value(curr_pair)
            res = float(req_value) * curr_val if req_value else curr_val
            print(locale.format_string('%.4f', float(res), True))
        except Exception as e:
            print('ERROR: ' + str(e))
            # raise e
        sys.exit(0)
#
# ############################
table_data = [["Name", "Symbol", "Units", "Price", "Change%", "Curr Value"]]
total_holding_value = 0

default_currency = config.get('default_currency', None)
fx_table = {}
for section in config:
    if section not in plugins:
        continue
    print("Processing...", section)
    plugin = plugins[section]
    for subsection in config[section]:
        # /f_tablex
        # mandatory in .ini
        symbol = config[section][subsection].get('symbol', None)
        units = config[section][subsection].get('units', None)
        #
        # optional in .ini
        ini_price = config[section][subsection].get('ini_price', None)
        # - if this sections hace 'currency', otherwise assume 'default_currency'. See above.
        this_currency = config[section][subsection].get('currency', default_currency)
        decimal_places = config[section][subsection].get('decimal_places', 2)
        add_to_total = config[section][subsection].get('add_to_total', True)
        is_fx = config[section][subsection].get('is_fx', False)
        #
        if add_to_total in ('no', 'False', '0'):
            add_to_total = False
        dec_place_format = '%.{0}f'.format(decimal_places)

        try:
            if section == 'default':
                curr_val = float(config[section][subsection].get('fixed_price', 1))
            else:
                curr_val = plugin.get_current_value(symbol)
                # keep fx rates:
                if is_fx:
                    fx_table.update({symbol: curr_val})
                    # and the inverse for convenience:
                    # (assume XYZABC format. so USDGBP => GBPUSD)
                    inv_symbol = symbol[3:6] + symbol[0:3]
                    fx_table.update({inv_symbol: 1 / curr_val})
            # Convert currency if needed:
            if this_currency != default_currency:
                # convert:
                curr_pair = '{0}{1}'.format(this_currency, default_currency)
                if curr_pair in fx_table:
                    curr_val = curr_val * fx_table[curr_pair]
                else:
                    print('WARNING: Could not find fx rate for {0}'
                          'Consider adding the currency pair to .ini file'.format(curr_pair))
            #
            if symbol and units:
                curr_holding_val = float(curr_val) * float(units)
                init_holding_val = ""
                change_perc_str = ""
                diff = 0
                if ini_price:
                    init_holding_val = float(ini_price) * float(units)
                    change_perc = (curr_holding_val / init_holding_val - 1) * 100
                    change_perc_str = str('{:+.2f}'.format(change_perc))
                    diff = curr_holding_val - init_holding_val
                if add_to_total:
                    total_holding_value += curr_holding_val
                #
                table_data.append(
                    [
                        subsection,
                        symbol,
                        # units,
                        locale.format_string('%.2f', float(units), True),
                        locale.format_string(dec_place_format, curr_val, True),
                        Color('{autored}' + change_perc_str + '{/autored}') if diff < 0  else Color('{autogreen}' + change_perc_str + '{/autogreen}'),
                        locale.format_string(dec_place_format, curr_holding_val, True) if add_to_total else ''
                    ]
                )
        except Exception as e:
            print('ERROR in ' + section + ' => ' + str(e))
            # raise e

# Totals:
table_data.append(
    ['', '', '', '',
     Color('{autoyellow}Total{/autoyellow}'),
     Color('{autoyellow}' + locale.format_string('%.2f', total_holding_value, True) + '{/autoyellow}')
     ]

)
# print(fx_table)
table = AsciiTable(table_data)
table.justify_columns[2] = "right"
table.justify_columns[3] = "right"
table.justify_columns[4] = "right"
table.justify_columns[5] = "right"
print(table.table)
