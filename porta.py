import os
import sys
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
requests_cache.install_cache('porta_cache', expire_after=timedelta(hours=cache_expire_hours))
#

# Load plugins
path = os.path.abspath(curr_dir + PLUGINS)
plugins = {}
sys.path.insert(0, path)
for f in os.listdir(path):
    fname, ext = os.path.splitext(f)
    if ext == '.py':
        mod = __import__(fname)
        plugins[fname] = mod.Plugin()
sys.path.pop(0)

# ############################
table_data = [["Name", "Symbol", "Units", "Price", "Change%", "Curr Value"]]
total_holding_value = 0
for section in config:
    if section not in plugins:
        continue
    print("Processing...", section)
    plugin = plugins[section]
    for subsection in config[section]:
        symbol = config[section][subsection].get('symbol', None)
        ini_price = config[section][subsection].get('ini_price', None)
        units = config[section][subsection].get('units', None)
        decimal_places = config[section][subsection].get('decimal_places', 2)
        add_to_total = config[section][subsection].get('add_to_total', True)
        #
        if add_to_total in ('no', 'False', '0'):
            add_to_total = False
        dec_place_format = '%.{0}f'.format(decimal_places)

        try:
            curr_val = plugin.get_current_value(symbol)
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
                        units,
                        locale.format_string(dec_place_format, curr_val, True),
                        Color('{autored}' + change_perc_str + '{/autored}') if diff < 0  else Color('{autogreen}' + change_perc_str + '{/autogreen}'),
                        locale.format_string(dec_place_format, curr_holding_val, True) if add_to_total else ''
                    ]
                )
        except Exception as e:
            print('ERROR on ' + section + '. ' + str(e))

# totals:
table_data.append(
    ['', '', '', '',
     Color('{autoyellow}Total{/autoyellow}'),
     Color('{autoyellow}' + locale.format_string('%.2f', total_holding_value, True) + '{/autoyellow}')
     ]

)
table = AsciiTable(table_data)
table.justify_columns[2] = "right"
table.justify_columns[3] = "right"
table.justify_columns[4] = "right"
table.justify_columns[5] = "right"
print(table.table)
