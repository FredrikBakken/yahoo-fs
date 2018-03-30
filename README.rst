===========================
Yahoo! FS (Finance Scraper)
===========================

Python API to get stock data from Yahoo! Finance using web scraping technology provided by Beautifulsoup4.

Developed as an alternative to yahoo-finance by Łukasz Banasiak, after the backend API was taken down.

How to Install
--------------
1. Install the requirements (Beautifulsoup4):

.. code:: bash

    $ pip install -r requirements.txt

2. Clone the yahoo_fs.py file into your project.

Examples
--------

Get Summary Data
^^^^^^^^^^^^^^^^
.. code:: python

    >>> from yahoo_fs import Share

    >>> goog = Share('GOOG')

    >>> print(goog.get_stock_exchange())
    'NasdaqGS'
    >>> print(goog.get_currency())
    'USD'
    >>> print(goog.get_price())
    '1,007.72'
    >>> print(goog.get_change())
    '+2.62'
    >>> print(goog.get_percent_change())
    '+0.26%'
    >>> print(goog.get_previous_trade_time())
    '2:11PM'
    >>> print(goog.get_trade_timezone())
    'EDT'
    >>> print(goog.get_previous_close())
    '1,005.10'
    >>> print(goog.get_open())
    '998.00'
    >>> print(goog.get_bid())
    '1,014.74 x 200'
    >>> print(goog.get_ask())
    '1,016.02 x 100'
    >>> print(goog.get_day_range())
    '980.64 - 1,024.23'
    >>> print(goog.get_52_week_range())
    '817.02 - 1,186.89'
    >>> print(goog.get_volume())
    '2,728,590'
    >>> print(goog.get_avg_daily_volume())
    '1,836,955'

Refresh Market Data
^^^^^^^^^^^^^^^^^^^
.. code:: python

    >>> from yahoo_fs import Share

    >>> goog = Share('GOOG')

    >>> goog.refresh()

Custom Statistics Search
^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    >>> from yahoo_fs import Share
    >>> from pprint import pprint

    >>> goog = Share('GOOG')

    >>> pprint(goog.get_custom_statistics_search('Valuation Measures'))
    {'Enterprise Value': '631.52B',
     'Enterprise Value/EBITDA': '17.65',
     'Enterprise Value/Revenue': '5.70',
     'Forward P/E': '20.90',
     'Market Cap (intraday)': '705.66B',
     'PEG Ratio (5 yr expected)': '1.07',
     'Price/Book': '4.62',
     'Price/Sales': '6.37',
     'Trailing P/E': '56.30'}
    >>> print(goog.get_custom_statistics_search('Trading Information', '200-Day Moving Average'))
    '1,046.7584'

Historical Data
^^^^^^^^^^^^^^^
.. code:: python

    >>> from yahoo_fs import Share
    >>> from pprint import pprint

    >>> goog = Share('GOOG')

    >>> pprint(goog.get_historical_day('2018-03-23'))
    [{'Adj Close': '1021.57',
      'Close': '1021.57',
      'Date': 'Mar 23 2018',
      'High': '1063.36',
      'Low': '1021.22',
      'Open': '1047.03',
      'Volume': '2156700'}]
    >>> pprint(goog.get_historical_days('2018-03-19', '2018-03-23'))
    [{'Adj Close': '1099.82',
      'Close': '1099.82',
      'Date': 'Mar 19 2018',
      'High': '1121.99',
      'Low': '1089.01',
      'Open': '1120.01',
      'Volume': '2805900'},
     {'Adj Close': '1021.57',
      'Close': '1021.57',
      'Date': 'Mar 23 2018',
      'High': '1063.36',
      'Low': '1021.22',
      'Open': '1047.03',
      'Volume': '2156700'}]
    >>> pprint(goog.get_historical_range('2018-02-01', '2018-02-09'))
    [{'Adj Close': '1167.70',
      'Close': '1167.70',
      'Date': 'Feb 01 2018',
      'High': '1174.00',
      'Low': '1157.52',
      'Open': '1162.61',
      'Volume': '2412100'},
     {'Adj Close': '1111.90',
      'Close': '1111.90',
      'Date': 'Feb 02 2018',
      'High': '1123.07',
      'Low': '1107.28',
      'Open': '1122.00',
      'Volume': '4857900'},
     {'Adj Close': '1055.80',
      'Close': '1055.80',
      'Date': 'Feb 05 2018',
      'High': '1110.00',
      'Low': '1052.03',
      'Open': '1090.60',
      'Volume': '3798300'},
     {'Adj Close': '1080.60',
      'Close': '1080.60',
      'Date': 'Feb 06 2018',
      'High': '1081.71',
      'Low': '1023.14',
      'Open': '1027.18',
      'Volume': '3448000'},
     {'Adj Close': '1048.58',
      'Close': '1048.58',
      'Date': 'Feb 07 2018',
      'High': '1081.78',
      'Low': '1048.26',
      'Open': '1081.54',
      'Volume': '2369200'},
     {'Adj Close': '1001.52',
      'Close': '1001.52',
      'Date': 'Feb 08 2018',
      'High': '1058.62',
      'Low': '1000.66',
      'Open': '1055.41',
      'Volume': '2859100'},
     {'Adj Close': '1037.78',
      'Close': '1037.78',
      'Date': 'Feb 09 2018',
      'High': '1043.97',
      'Low': '992.56',
      'Open': '1017.25',
      'Volume': '3505900'}]

Available Methods
-----------------
- ``get_stock_exchange()``
- ``get_currency()``
- ``get_price()``
- ``get_change()``
- ``get_percent_change()``
- ``get_previous_trade_time()``
- ``get_trade_timezone()``
- ``get_previous_close()``
- ``get_open()``
- ``get_bid()``
- ``get_ask()``
- ``get_day_range()``
- ``get_52_week_range()``
- ``get_volume()``
- ``get_avg_daily_volume()``
- ``get_custom_statistics_search(heading, row=None)``
- ``get_valuation_measures()``
- ``get_market_cap()``
- ``get_enterprise_value()``
- ``get_trailing_pe()``
- ``get_forward_pe()``
- ``get_peg_ratio()``
- ``get_price_per_sales()``
- ``get_price_per_book()``
- ``get_enterprise_value_per_revenue()``
- ``get_enterprise_value_per_ebitda()``
- ``get_financial_highlights()``
- ``get_fiscal_year_ends()``
- ``get_most_recent_quarter()``
- ``get_profit_margin()``
- ``get_operating_margin()``
- ``get_return_assets()``
- ``get_return_equity()``
- ``get_revenue()``
- ``get_revenue_per_share()``
- ``get_quarterly_revenue_growth()``
- ``get_gross_profit()``
- ``get_ebitda()``
- ``get_net_income_avi_to_common()``
- ``get_diluted_eps()``
- ``get_quarterly_earnings_growth()``
- ``get_total_cash()``
- ``get_total_cash_per_share()``
- ``get_total_debt()``
- ``get_total_debt_per_equity()``
- ``get_current_ratio()``
- ``get_book_value_per_share()``
- ``get_operating_cash_flow()``
- ``get_levered_free_cash_flow()``
- ``get_trading_information()``
- ``get_beta()``
- ``get_52_week_change()``
- ``get_sp500_52_week_change()``
- ``get_52_week_high()``
- ``get_52_week_low()``
- ``get_50_day_average()``
- ``get_200_day_average()``
- ``get_avg_3_month_volume()``
- ``get_avg_10_day_volume()``
- ``get_shares_outstanding()``
- ``get_float()``
- ``get_percent_held_insiders()``
- ``get_percent_held_institutions()``
- ``get_shares_short()``
- ``get_short_ratio()``
- ``get_short_percent_of_float()``
- ``get_shares_short_prior()``
- ``get_forward_dividend_rate()``
- ``get_forward_dividend_yield()``
- ``get_trailing_dividend_rate()``
- ``get_trailing_dividend_yield()``
- ``get_5_year_avg_dividend_yield()``
- ``get_payout_ratio()``
- ``get_dividend_date()``
- ``get_exdividend_date()``
- ``get_last_split_factor()``
- ``get_last_split_date()``
- ``get_company_name()``
- ``get_company_address()``
- ``get_company_phone_number()``
- ``get_company_website()``
- ``get_sector()``
- ``get_industry()``
- ``get_key_executives()``
- ``get_historical_day(date)``
- ``get_historical_days(date_from, date_to)``
- ``get_historical_range(date_from, date_to)``
- ``get_analysts_earnings_estimate()``
- ``get_analysts_revenue_estimate()``
- ``get_analysts_earnings_history()``
- ``get_analysts_eps_trend()``
- ``get_analysts_eps_revisions()``
- ``get_analysts_growth_estimates()``
- ``refresh()``