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
    '2728590'
    >>> print(goog.get_avg_daily_volume())
    '1836955'

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

    >>> print(goog.get_historical_day('2018-03-22'))
    [['Mar 22 2018', '1081.88', '1082.90', '1045.91', '1049.08', '1049.08', '2667000']]
    >>> print(goog.get_historical_days('2018-03-19', '2018-03-23'))
    [['Mar 19 2018', '1120.01', '1121.99', '1089.01', '1099.82', '1099.82', '2805900'],
     ['Mar 23 2018', '1047.03', '1063.36', '1021.22', '1021.57', '1021.57', '2156700']]
    >>> pprint(goog.get_historical_range('2018-02-01', '2018-03-09'))
    [['Feb 01 2018', '1162.61', '1174.00', '1157.52', '1167.70', '1167.70', '2412100']
     ['Feb 02 2018', '1122.00', '1123.07', '1107.28', '1111.90', '1111.90', '4857900']
     ['Feb 05 2018', '1090.60', '1110.00', '1052.03', '1055.80', '1055.80', '3798300']
     ['Feb 06 2018', '1027.18', '1081.71', '1023.14', '1080.60', '1080.60', '3448000']
     ['Feb 07 2018', '1081.54', '1081.78', '1048.26', '1048.58', '1048.58', '2369200']
     ['Feb 08 2018', '1055.41', '1058.62', '1000.66', '1001.52', '1001.52', '2859100']
     ['Feb 09 2018', '1017.25', '1043.97', '992.56', '1037.78', '1037.78', '3505900']
     ['Feb 12 2018', '1048.00', '1061.50', '1040.93', '1051.94', '1051.94', '2057700']
     ['Feb 13 2018', '1045.00', '1058.37', '1044.09', '1052.10', '1052.10', '1265100']
     ['Feb 14 2018', '1048.95', '1071.72', '1046.75', '1069.70', '1069.70', '1555800']
     ['Feb 15 2018', '1079.07', '1091.48', '1064.34', '1089.52', '1089.52', '1843400']
     ['Feb 16 2018', '1088.41', '1104.67', '1088.31', '1094.80', '1094.80', '1681600']
     ['Feb 20 2018', '1090.57', '1113.95', '1088.52', '1102.46', '1102.46', '1423100']
     ['Feb 21 2018', '1106.47', '1133.97', '1106.33', '1111.34', '1111.34', '1512900']
     ['Feb 22 2018', '1116.19', '1122.82', '1102.59', '1106.63', '1106.63', '1317200']
     ['Feb 23 2018', '1112.64', '1127.28', '1104.71', '1126.79', '1126.79', '1261000']
     ['Feb 26 2018', '1127.80', '1143.96', '1126.69', '1143.75', '1143.75', '1559100']
     ['Feb 27 2018', '1141.24', '1144.04', '1118.00', '1118.29', '1118.29', '1774100']
     ['Feb 28 2018', '1123.03', '1127.53', '1103.24', '1104.73', '1104.73', '1882600']
     ['Mar 01 2018', '1107.87', '1110.12', '1067.00', '1069.52', '1069.52', '2515900']
     ['Mar 02 2018', '1053.08', '1082.00', '1048.11', '1078.92', '1078.92', '2271600']
     ['Mar 05 2018', '1075.14', '1097.10', '1069.00', '1090.93', '1090.93', '1202200']
     ['Mar 06 2018', '1099.22', '1101.85', '1089.78', '1095.06', '1095.06', '1532800']
     ['Mar 07 2018', '1089.19', '1112.22', '1085.48', '1109.64', '1109.64', '1292500']
     ['Mar 08 2018', '1115.32', '1127.60', '1112.80', '1126.00', '1126.00', '1355100']]

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