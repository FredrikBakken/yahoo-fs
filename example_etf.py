#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Author: Fredrik Bakken
# Website: https://www.fredrikbakken.no/

from pprint import pprint
from yahoo_fs import ETF


def etf_examples():
    robo = ETF('ROBO')
    print(robo.get_price())

    # All available commands (commented)

    '''
    print(robo.get_stock_exchange())
    print(robo.get_currency())
    print(robo.get_price())
    print(robo.get_change())
    print(robo.get_percent_change())
    print(robo.get_previous_trade_time())
    print(robo.get_trade_timezone())
    print(robo.get_previous_close())
    print(robo.get_open())
    print(robo.get_bid())
    print(robo.get_ask())
    print(robo.get_day_range())
    print(robo.get_52_week_range())
    print(robo.get_volume())
    print(robo.get_avg_daily_volume())
    print(robo.get_net_assets())
    print(robo.get_nav())
    print(robo.get_pe_ratio())
    print(robo.get_yield())
    print(robo.get_ytd_return())
    print(robo.get_beta())
    print(robo.get_expense_ratio())
    print(robo.get_inception_date())
    '''

    '''
    print(robo.get_company_name())
    print(robo.get_company_phone())
    pprint(robo.get_fund_overview())
    pprint(robo.get_fund_operations())
    '''

    '''
    pprint(robo.get_historical_day('2018-02-20'))
    pprint(robo.get_historical_days('2018-03-19', '2018-03-23'))
    pprint(robo.get_historical_range('2018-02-01', '2018-02-15'))
    '''

    '''
    pprint(robo.get_portfolio_composition())
    pprint(robo.get_sector_weightings())
    pprint(robo.get_equity_holdings())
    pprint(robo.get_bond_ratings())
    pprint(robo.get_top_10_holdings())
    '''

    '''
    pprint(robo.get_trailing_returns_vs_benchmark())
    pprint(robo.get_annual_total_return_history())
    '''

    '''
    pprint(robo.get_risk_statistics())
    '''


if __name__ == '__main__':
    etf_examples()
