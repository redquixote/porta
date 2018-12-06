# Porta

The most simple Holdings Portfolio command line with a Plugin system.

## Features:
- Few lines, simple code,
- Privacy oriented and easy to audit (don't trust, take a look at the code)
- Simple *simple* plugins system
- Caches requests using request_cache (polite with services)


```
+-----------------+----------+---------+----------+---------+------------+
| Name            | Symbol   |   Units |    Price | Change% | Curr Value |
+-----------------+----------+---------+----------+---------+------------+
| Amazon Inc      | AMZN     |      10 | 1,668.40 |         |  16,684.00 |
| USD -> GBP      | USD_GBP  |       1 |  0.78291 |         |            |
| Bitcoin         | XBTUSD   |       1 | 3,860.00 |  -73.94 |   3,860.00 |
| Ethereum        | ETHUSD   |       1 |   107.27 |         |            |
| My Bitcoin SV   | BSVUSD   |       1 |    91.90 |         |            |
| My Bitcoin Cash | BCHUSD   |       1 |   140.40 |         |            |
|                 |          |         |          |   Total |  20,544.00 |
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


    cache_hours = 1

    [default]

        [[Savings Chase]]
        symbol = USD
        units = 1000
        # Case just fixed price, to show an asset w/o querying current price:
        fixed_price = 1.2

    [currencyconverterapi]

        [[USD -> GBP]]
        symbol = USD_GBP
        units = 1
        # decimal_places is optional (default to 2)
        decimal_places = 5

        [[GBP -> SEK]]
        symbol = GBP_SEK
        units = 1

    # stocks:
    [iextrading]
        [[Amazon Inc]]
        symbol = AMZN
        units = 1

        [[Google Be Evil Inc]]
        symbol = GOOG
        units = 2


    # crytocurrencies:
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


Mandatory fields:
- symbol
- units

Optional:
- ini_price: initial price ie. purchase price.
- fixed_price: Case just fixed price, to show an asset w/o querying current price:
- decimal_places: decimal places to display (default to 2)


`ini_price`

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
| Amazon Inc      | AMZN     |      10 | 1,668.40 |         |  16,684.00 |
| USD -> GBP      | USD_GBP  |       1 |  0.78291 |         |            |
| Bitcoin         | XBTUSD   |       1 | 3,860.00 |  -73.94 |   3,860.00 |
| Ethereum        | ETHUSD   |       1 |   107.27 |         |            |
| My Bitcoin SV   | BSVUSD   |       1 |    91.90 |         |            |
| My Bitcoin Cash | BCHUSD   |       1 |   140.40 |         |            |
|                 |          |         |          |   Total |  20,544.00 |
+-----------------+----------+---------+----------+---------+------------+

```

# Plugins


Current Included Plugins:

- Kraken (for Cryptocurrencies)
- Currency Converter API (for FX)
- (add yours: See plugin [plugins](plugins/) directory

# TODO

Check [TODO](TODO.md) file


