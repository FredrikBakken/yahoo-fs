#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Yahoo! Finance Scraper
# https://github.com/FredrikBakken/yahoo-fs
#
# Author: Fredrik Bakken
# Version: 0.0.1
# Website: https://www.fredrikbakken.no/

import sys
import json
import time
import math
import datetime

from bs4 import BeautifulSoup

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.request
else:
    import urllib2


class Share:
    def __init__(self, ticker, loader=None):
        self.ticker = ticker
        self.loader = loader

        self.url_summary = "https://finance.yahoo.com/quote/" + self.ticker
        self.url_statistics = self.url_summary + "/key-statistics?p=" + self.ticker
        self.url_profile = self.url_summary + "/profile?p=" + self.ticker
        self.url_analysts = self.url_summary + "/analysts?p=" + self.ticker

        self.content_summary = self._open_page_content(self.url_summary)
        self.content_statistics = self._open_page_content(self.url_statistics)
        self.content_profile = self._open_page_content(self.url_profile)
        self.content_analysts = self._open_page_content(self.url_analysts)

        self.soup_summary = BeautifulSoup(self.content_summary, 'html.parser')
        self.soup_statistics = BeautifulSoup(self.content_statistics, 'html.parser')
        self.soup_profile = BeautifulSoup(self.content_profile, 'html.parser')
        self.soup_analysts = BeautifulSoup(self.content_analysts, 'html.parser')


    def _open_page_content(self, url):
        if PYTHON_VERSION == 3:
            return urllib.request.urlopen(url).read()
        else:
            return urllib2.urlopen(url).read()


    def _search_soup(self, soup_url, tag, attribute, value):
        return soup_url.find(tag, attrs={attribute : value}).getText()
    
    def _search_soup_html(self, soup_url, tag, attribute, value):
        return soup_url.find(tag, attrs={attribute : value})

    
    def _company_address(self, soup_url, tag, attribute, value):
        company_location = self._search_soup_html(soup_url, tag, attribute, value)
        
        element_counter = 0
        for element in company_location:
            element_counter += 1
            if element_counter == 2:
                street = element
            elif element_counter == 6:
                address = element
            elif element_counter == 10:
                country = element
        return json.dumps({'street': street, 'address': address, 'country': country})

    
    def _key_executives(self, soup_url, tag, attribute, value):
        table = self._search_soup_html(soup_url, tag, attribute, value)
        table_body = table.find('tbody')
        table_rows = table_body.find_all('tr')

        key_executives = []
        for row in table_rows:
            cols = row.find_all('td')
            column = []
            for cell in cols:
                column.extend([cell.getText()])
            key_executives.append(column)
        return key_executives


    def _historical_data(self, from_date, to_date=None, day_range=None):
        urls = []
        if to_date == None:
            timestamp = int(time.mktime(datetime.datetime.strptime(from_date, '%Y-%m-%d').timetuple()))
            url = "https://finance.yahoo.com/quote/OCY.OL/history?period1=" + str(timestamp) + "&period2=" + str(timestamp) + "&interval=1d&filter=history&frequency=1d"
            urls.append(url)
        elif to_date and day_range == 'days':
            timestamp_from = int(time.mktime(datetime.datetime.strptime(from_date, '%Y-%m-%d').timetuple()))
            url_from = "https://finance.yahoo.com/quote/OCY.OL/history?period1=" + str(timestamp_from) + "&period2=" + str(timestamp_from) + "&interval=1d&filter=history&frequency=1d"
            urls.append(url_from)

            timestamp_to = int(time.mktime(datetime.datetime.strptime(to_date, '%Y-%m-%d').timetuple()))
            url_to = "https://finance.yahoo.com/quote/OCY.OL/history?period1=" + str(timestamp_to) + "&period2=" + str(timestamp_to) + "&interval=1d&filter=history&frequency=1d"
            urls.append(url_to)
        elif to_date and day_range == 'range':
            date_format = '%Y-%m-%d'
            d0 = datetime.datetime.strptime(from_date, date_format)
            d1 = datetime.datetime.strptime(to_date, date_format)
            difference = int((d1 - d0).days)
            
            days_per_run = 120
            number_of_runs = math.ceil(difference / days_per_run)

            for i in range(number_of_runs):
                start_at = days_per_run * i
                end_at   = days_per_run * (i+1)

                start_date = d0 + datetime.timedelta(days=start_at)
                end_date   = d0 + datetime.timedelta(days=end_at)
                if end_date > d1:
                    end_date = d1
                
                timestamp_from = int(time.mktime(datetime.datetime.strptime(start_date.strftime('%Y-%m-%d'), '%Y-%m-%d').timetuple()))
                timestamp_to = int(time.mktime(datetime.datetime.strptime(end_date.strftime('%Y-%m-%d'), '%Y-%m-%d').timetuple()))
                url = "https://finance.yahoo.com/quote/OCY.OL/history?period1=" + str(timestamp_from) + "&period2=" + str(timestamp_to) + "&interval=1d&filter=history&frequency=1d"
                urls.append(url)

        historic_result = []
        for url in urls:
            content_history = self._open_page_content(url)
            soup_history = BeautifulSoup(content_history, 'html.parser')

            table = soup_history.find('table', attrs={'class': 'W(100%)'})
            table_body = table.find('tbody')
            table_rows = table_body.find_all('tr')
            
            for row in table_rows:
                cols = row.find_all('td')
                current_row = []
                for cell in cols:
                    current_row.extend([cell.getText().replace(',', '')])
                if current_row not in historic_result and not set(['-', '-', '-', '-', '-', '-']).issubset(set(current_row)):
                    historic_result.append(current_row)

        if day_range == 'range':
            historic_result = sorted(historic_result, key = lambda x : datetime.datetime.strptime(x[0], '%b %d %Y'))

        return historic_result
    
    
    def _analysts_tables(self, tag, attribute, value):
        table_content = []
        table = self.soup_analysts.find_all(tag, attrs={attribute : value})
        table_head = table[0].find('thead').find('tr')
        table_body = table[0].find('tbody')
        head_rows = table_head.find_all('th')
        body_rows = table_body.find_all('tr')
        
        for i in range(1, len(head_rows)):
            row_dictionary = {}
            table_content.append([head_rows[i].getText(), row_dictionary])
            for j in range(1, len(body_rows)):
                row_dictionary[body_rows[j].find_all('td')[0].getText()] = body_rows[j].find_all('td')[i].getText()
        
        return table_content

    
    # Summary
    def get_stock_exchange(self):
        return self._search_soup(self.soup_summary, 'span', 'data-reactid', '9').split(' ')[0]
    
    def get_currency(self):
        return self._search_soup(self.soup_summary, 'span', 'data-reactid', '9').split(' ')[-1]

    def get_price(self):
        return self._search_soup(self.soup_summary, 'span', 'data-reactid', '14')
    
    def get_change(self):
        return self._search_soup(self.soup_summary, 'span', 'data-reactid', '17').split(' ')[0]
    
    def get_percent_change(self):
        return self._search_soup(self.soup_summary, 'span', 'data-reactid', '17').split(' ')[1].replace('(', '').replace(')', '')
    
    def get_previous_trade_time(self):
        return self._search_soup(self.soup_summary, 'div', 'id', 'quote-market-notice').split(' ')[3]
    
    def get_trade_timezone(self):
        return self._search_soup(self.soup_summary, 'div', 'id', 'quote-market-notice').split(' ')[4].replace('.', '')
    
    def get_previous_close(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'PREV_CLOSE-value')
    
    def get_open(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'OPEN-value')
    
    def get_bid(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'BID-value')
    
    def get_ask(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'ASK-value')

    def get_day_range(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'DAYS_RANGE-value')
    
    def get_52_week_range(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'FIFTY_TWO_WK_RANGE-value')
    
    def get_volume(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'TD_VOLUME-value').replace(',', '')
    
    def get_avg_daily_volume(self):
        return self._search_soup(self.soup_summary, 'td', 'data-test', 'AVERAGE_VOLUME_3MONTH-value').replace(',', '')
    

    # Statistics | Valuation measures
    def get_market_cap(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '19')
    
    def get_enterprise_value(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '26')

    def get_trailing_pe(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '33')
    
    def get_forward_pe(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '40')
    
    def get_peg_ratio(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '47')
    
    def get_price_per_sales(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '55')
    
    def get_price_per_book(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '62')

    def get_enterprise_value_per_revenue(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '69')

    def get_enterprise_value_per_ebitda(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '76')
    

    # Statistics | Financial highlights
    def get_fiscal_year_ends(self):
        return self._search_soup(self.soup_statistics, 'span', 'data-reactid', '97')
    
    def get_most_recent_quarter(self):
        return self._search_soup(self.soup_statistics, 'span', 'data-reactid', '105')
    
    def get_profit_margin(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '117')
    
    def get_operating_margin(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '124')
    
    def get_return_assets(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '136')
    
    def get_return_equity(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '143')
    
    def get_revenue(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '155')

    def get_revenue_per_share(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '162')
    
    def get_quarterly_revenue_growth(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '169')

    def get_gross_profit(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '176')
    
    def get_ebitda(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '183')
    
    def get_net_income_avi_to_common(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '190')

    def get_diluted_eps(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '197')
    
    def get_quarterly_earnings_growth(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '204')
    
    def get_total_cash(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '217')
    
    def get_total_cash_per_share(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '224')
    
    def get_total_debt(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '231')
    
    def get_total_debt_per_equity(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '238')
    
    def get_current_ratio(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '245')
    
    def get_book_value_per_share(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '252')
    
    def get_operating_cash_flow(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '264')
    
    def get_levered_free_cash_flow(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '271')
    

    # Statistics | Trading information
    def get_beta(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '290')
    
    def get_52_week_change(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '297')
    
    def get_sp500_52_week_change(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '304')
    
    def get_52_week_high(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '311')
    
    def get_52_week_low(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '318')
    
    def get_50_day_average(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '325')
    
    def get_200_day_average(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '332')
    
    def get_avg_3_month_volume(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '344')
    
    def get_avg_10_day_volume(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '351')
    
    def get_shares_outstanding(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '358')
    
    def get_float(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '365')

    def get_percent_held_insiders(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '372')
    
    def get_percent_held_institutions(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '380')
    
    def get_shares_short(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '388')

    def get_short_ratio(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '396')
    
    def get_short_percent_of_float(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '404')
    
    def get_shares_short_prior(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '412')
    
    def get_forward_dividend_rate(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '425')
    
    def get_forward_dividend_yield(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '432')
    
    def get_trailing_dividend_rate(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '439')
    
    def get_trailing_dividend_yield(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '446')
    
    def get_5_year_avg_dividend_yield(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '453')
    
    def get_payout_ratio(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '461')
    
    def get_dividend_date(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '468')
    
    def get_exdividend_date(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '476')
    
    def get_last_split_factor(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '484')
    
    def get_last_split_date(self):
        return self._search_soup(self.soup_statistics, 'td', 'data-reactid', '492')
    

    # Profile | Company information
    def get_company_name(self):
        return self._search_soup(self.soup_profile, 'h3', 'data-reactid', '6')
    
    def get_company_address(self):
        return self._company_address(self.soup_profile, 'p', 'data-reactid', '8')
    
    def get_company_phone_number(self):
        return self._search_soup(self.soup_profile, 'a', 'data-reactid', '15')

    def get_company_website(self):
        return self._search_soup(self.soup_profile, 'a', 'target', '_blank')
    
    def get_sector(self):
        return self._search_soup(self.soup_profile, 'strong', 'data-reactid', '21')
    
    def get_industry(self):
        return self._search_soup(self.soup_profile, 'strong', 'data-reactid', '25')
    
    def get_number_of_full_time_employees(self):
        return self._search_soup(self.soup_profile, 'strong', 'data-reactid', '29')
    
    def get_key_executives(self):
        return self._key_executives(self.soup_profile, 'table', 'class', 'W(100%)')
 
    
    # Historical data
    def get_historical_day(self, date):
        return self._historical_data(date)
    
    def get_historical_days(self, from_date, to_date):
        return self._historical_data(from_date, to_date, 'days')
    
    def get_historical_range(self, from_date, to_date):
        return self._historical_data(from_date, to_date, 'range')
    

    # Analysts
    def get_analysts_earnings_estimate(self):
        return self._analysts_tables('table', 'data-reactid', '5')
    
    def get_analysts_revenue_estimate(self):
        return self._analysts_tables('table', 'data-reactid', '106')
    
    def get_analysts_earnings_history(self):
        return self._analysts_tables('table', 'data-reactid', '225')
    
    def get_analysts_eps_trend(self):
        return self._analysts_tables('table', 'data-reactid', '299')
    
    def get_analysts_eps_revisions(self):
        return self._analysts_tables('table', 'data-reactid', '400')
    
    def get_analysts_growth_estimates(self):
        return self._analysts_tables('table', 'data-reactid', '477')


    # Refresh newest content
    def refresh(self):
        self.__init__(self.ticker)
