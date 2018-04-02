#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Author: Fredrik Bakken
# Website: https://www.fredrikbakken.no/

from pprint import pprint
from yahoo_fs import Share


def stock_examples():
    goog = Share('GOOG')
    print(goog.get_price())

    # All available commands (commented)
    
    '''
    # Summary
    print(goog.get_stock_exchange())
    print(goog.get_currency())
    print(goog.get_price())
    print(goog.get_change())
    print(goog.get_percent_change())
    print(goog.get_previous_trade_time())
    print(goog.get_trade_timezone())
    print(goog.get_previous_close())
    print(goog.get_open())
    print(goog.get_bid())
    print(goog.get_ask())
    print(goog.get_day_range())
    print(goog.get_52_week_range())
    print(goog.get_volume())
    print(goog.get_avg_daily_volume())
    '''

    '''
    # Custom Statistics Search
    pprint(goog.get_custom_statistics_search('Valuation Measures'))
    print(goog.get_custom_statistics_search('Trading Information', '200-Day Moving Average'))
    '''

    '''
    # Statistics | Valuation measures
    pprint(goog.get_valuation_measures())
    print(goog.get_market_cap())
    print(goog.get_enterprise_value())
    print(goog.get_trailing_pe())
    print(goog.get_forward_pe())
    print(goog.get_peg_ratio())
    print(goog.get_price_per_sales())
    print(goog.get_price_per_book())
    print(goog.get_enterprise_value_per_revenue())
    print(goog.get_enterprise_value_per_ebitda())
    '''

    '''
    # Statistics | Financial highlights
    pprint(goog.get_financial_highlights())
    print(goog.get_fiscal_year_ends())
    print(goog.get_most_recent_quarter())
    print(goog.get_profit_margin())
    print(goog.get_operating_margin())
    print(goog.get_return_assets())
    print(goog.get_return_equity())
    print(goog.get_revenue())
    print(goog.get_revenue_per_share())
    print(goog.get_quarterly_revenue_growth())
    print(goog.get_gross_profit())
    print(goog.get_ebitda())
    print(goog.get_net_income_avi_to_common())
    print(goog.get_diluted_eps())
    print(goog.get_quarterly_earnings_growth())
    print(goog.get_total_cash())
    print(goog.get_total_cash_per_share())
    print(goog.get_total_debt())
    print(goog.get_total_debt_per_equity())
    print(goog.get_current_ratio())
    print(goog.get_book_value_per_share())
    print(goog.get_operating_cash_flow())
    print(goog.get_levered_free_cash_flow())
    '''

    '''
    # Statistics | Trading information
    pprint(goog.get_trading_information())
    print(goog.get_beta())
    print(goog.get_52_week_change())
    print(goog.get_sp500_52_week_change())
    print(goog.get_52_week_high())
    print(goog.get_52_week_low())
    print(goog.get_50_day_average())
    print(goog.get_200_day_average())
    print(goog.get_avg_3_month_volume())
    print(goog.get_avg_10_day_volume())
    print(goog.get_shares_outstanding())
    print(goog.get_float())
    print(goog.get_percent_held_insiders())
    print(goog.get_percent_held_institutions())
    print(goog.get_shares_short())
    print(goog.get_short_ratio())
    print(goog.get_short_percent_of_float())
    print(goog.get_shares_short_prior())
    print(goog.get_forward_dividend_rate())
    print(goog.get_forward_dividend_yield())
    print(goog.get_trailing_dividend_rate())
    print(goog.get_trailing_dividend_yield())
    print(goog.get_5_year_avg_dividend_yield())
    print(goog.get_payout_ratio())
    print(goog.get_dividend_date())
    print(goog.get_exdividend_date())
    print(goog.get_last_split_factor())
    print(goog.get_last_split_date())
    '''

    '''
    # Profile | Company information
    print(goog.get_company_name())
    pprint(goog.get_company_address())
    print(goog.get_company_phone_number())
    print(goog.get_company_website())
    print(goog.get_sector())
    print(goog.get_industry())
    print(goog.get_number_of_full_time_employees())
    pprint(goog.get_key_executives())
    '''

    '''
    # Historical data
    pprint(goog.get_historical_day('2018-02-20'))
    pprint(goog.get_historical_days('2018-03-19', '2018-03-23'))
    pprint(goog.get_historical_range('2018-02-01', '2018-02-15'))
    '''

    '''
    # Custom Analysts Search
    pprint(goog.get_custom_analysts_search('Revenue Estimate'))
    '''

    '''
    # Analysts
    pprint(goog.get_analysts_earnings_estimate())
    pprint(goog.get_analysts_revenue_estimate())
    pprint(goog.get_analysts_earnings_history())
    pprint(goog.get_analysts_eps_trend())
    pprint(goog.get_analysts_eps_revisions())
    pprint(goog.get_analysts_growth_estimates())
    '''


if __name__ == '__main__':
    stock_examples()
