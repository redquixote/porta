# Porta

The most simple Holdings Portfolio command line with a Plugin system.

## Features:
- Few lines, simple code, easy to audit (1 min). (Don't give your data to anyone)
- simple simple plugins
- caches requests using request_cache


```
+-----------------+----------+---------+----------+---------+------------+
| Name            | Symbol   |   Units |    Price | Change% | Curr Value |
+-----------------+----------+---------+----------+---------+------------+
| USD -> GBP      | USD_GBP  |       1 |  0.78291 |         |            |
| Bitcoin         | XBTUSD   |       1 | 3,860.00 |  -73.94 |   3,860.00 |
| Ethereum        | ETHUSD   |       1 |   107.27 |         |            |
| My Bitcoin SV   | BSVUSD   |       1 |    91.90 |         |            |
| My Bitcoin Cash | BCHUSD   |       1 |   140.40 |         |            |
|                 |          |         |          |   Total |   3,860.00 |
+-----------------+----------+---------+----------+---------+------------+

```



## Installation

1. Clone / download

2. Install requirements (in a virtualenv, recommended):

    ```
    pip install -r requirements.txt
    ```

## configure portfolio

Create a configuration file `~/.config/porta.ini`  like:

    [currencyconverterapi]

    [[USD -> GBP]]
    symbol = USD_GBP
    units = 1
    # decimal_places is optional (default to 2)
    decimal_places = 5

    [[GBP -> SEK]]
    symbol = GBP_SEK
    units = 1


    [kraken]
    [[hold1]]
    symbol = XBTUSD
    # ini_price is optional:
    ini_price =
    units = 0.52

    [[hold2]]
    symbol = XBTUSD
    ini_price = 432.0
    units = 1

    [[Bitcoin]]
    symbol = XBTUSD
    ini_price = 19242.48
    units = 1

    [[Ethereum]]
    symbol = ETHUSD
    ini_price =
    units = 1

    [[My Bitcoin SV]]
    symbol = BSVUSD
    ini_price =
    units = 1

    [[My Bitcoin Cash]]
    symbol = BCHUSD
    ini_price =
    units = 1

Check `porta.example.ini`


# Usage

```
python porta.py
```

And you'll get something like:

```
+-----------------+----------+---------+----------+---------+------------+
| Name            | Symbol   |   Units |    Price | Change% | Curr Value |
+-----------------+----------+---------+----------+---------+------------+
| USD -> GBP      | USD_GBP  |       1 |  0.78291 |         |            |
| Bitcoin         | XBTUSD   |       1 | 3,860.00 |  -73.94 |   3,860.00 |
| Ethereum        | ETHUSD   |       1 |   107.27 |         |            |
| My Bitcoin SV   | BSVUSD   |       1 |    91.90 |         |            |
| My Bitcoin Cash | BCHUSD   |       1 |   140.40 |         |            |
|                 |          |         |          |   Total |   3,860.00 |
+-----------------+----------+---------+----------+---------+------------+

```

# Plugins


Current Included Plugins:

- Kraken (for Cryptocurrencies)
- Currency Converter API (for FX)
- (add yours: See plugins directory)

# TODO

Check TODO.md file


