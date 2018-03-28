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
    [['Mar 22 2018', '66.20', '66.80', '65.60', '65.80', '65.80', '202380']]
    >>> print(goog.get_historical_days('2018-03-19', '2018-03-23'))
    [['Mar 19 2018', '66.10', '66.20', '64.80', '65.40', '65.40', '440896'], ['Mar 23 2018', '65.30', '66.30', '64.20', '65.80', '65.80', '387302']]
    >>> pprint(goog.get_historical_range('2018-02-01', '2018-03-09'))
    [['Feb 01 2018', '70.00', '70.00', '68.80', '69.10', '67.67', '112631'],
     ['Feb 02 2018', '69.20', '69.70', '68.40', '69.30', '67.87', '57038'],
     ['Feb 05 2018', '68.50', '68.50', '66.90', '67.60', '66.20', '190831'],
     ['Feb 06 2018', '64.90', '67.10', '63.90', '67.10', '65.71', '296252'],
     ['Feb 07 2018', '68.00', '68.60', '67.20', '67.20', '65.81', '140968'],
     ['Feb 08 2018', '67.40', '68.00', '67.00', '67.80', '66.40', '101122'],
     ['Feb 09 2018', '65.80', '67.20', '65.10', '66.60', '65.22', '300361'],
     ['Feb 12 2018', '67.60', '69.40', '67.60', '68.80', '67.38', '141069'],
     ['Feb 13 2018', '71.80', '71.80', '67.80', '68.70', '67.28', '239136'],
     ['Feb 14 2018', '68.50', '69.20', '67.50', '68.20', '66.79', '173618'],
     ['Feb 15 2018', '69.60', '70.80', '69.10', '70.50', '69.04', '179485'],
     ['Feb 16 2018', '70.40', '70.90', '69.80', '70.60', '69.14', '159332'],
     ['Feb 19 2018', '70.80', '71.70', '70.70', '71.40', '69.93', '151256'],
     ['Feb 20 2018', '70.50', '70.50', '69.70', '70.40', '70.40', '108784'],
     ['Feb 20 2018', '1.47469 Dividend'],
     ['Feb 21 2018', '70.40', '70.50', '69.80', '70.30', '70.30', '100970'],
     ['Feb 22 2018', '70.00', '70.80', '69.60', '70.80', '70.80', '190904'],
     ['Feb 23 2018', '71.20', '71.90', '70.80', '71.60', '71.60', '170627'],
     ['Feb 26 2018', '72.00', '72.10', '71.50', '72.10', '72.10', '101789'],
     ['Feb 27 2018', '72.20', '72.50', '72.10', '72.40', '72.40', '242005'],
     ['Feb 28 2018', '72.40', '73.00', '72.00', '73.00', '73.00', '241673'],
     ['Mar 01 2018', '68.20', '69.50', '68.20', '68.50', '68.50', '1682413'],
     ['Mar 02 2018', '68.50', '69.30', '67.00', '68.10', '68.10', '950845'],
     ['Mar 05 2018', '68.40', '68.80', '68.00', '68.20', '68.20', '238511'],
     ['Mar 06 2018', '68.80', '69.20', '68.70', '69.10', '69.10', '396357'],
     ['Mar 07 2018', '68.80', '69.10', '68.60', '69.00', '69.00', '189578'],
     ['Mar 08 2018', '69.00', '69.10', '68.80', '69.00', '69.00', '148020'],
     ['Mar 09 2018', '69.00', '69.10', '68.80', '69.00', '69.00', '151205']]

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