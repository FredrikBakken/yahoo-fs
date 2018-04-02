#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Yahoo! Finance Scraper
# https://github.com/FredrikBakken/yahoo-fs
#
# Author: Fredrik Bakken
# Version: 0.0.6
# Website: https://www.fredrikbakken.no/

import sys
import math
import calendar
from datetime import datetime, timedelta

from bs4 import BeautifulSoup

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.request
else:
    import urllib2


def open_page_content(url):
    """ Method for opening and reading urls.
    """
    if PYTHON_VERSION == 3:
        try:
            return urllib.request.urlopen(url).read()
        except urllib.error.HTTPError as err:
            print('HTTP Error Code: %s' % (str(err.code)))
    else:
        try:
            return urllib2.urlopen(url).read()
        except urllib2.HTTPError as err:
            print('HTTP Error Code: %s' % (str(err.code)))


def search_soup(soup, tag=None, attribute=None, value=None):
    """ Method for finding specific web element text.
    """
    try:
        if tag == None and attribute == None and value == None:
            return soup.getText()
        elif attribute == None and value == None:
            return soup.find(tag).getText()
        else:
            return soup.find(tag, attrs={attribute : value}).getText()
    except:
        return None


def time_setup(date, timezone):
    """ Method for setting time offset according to timezone.
    """
    time_offset = ''
    if timezone == 'EST' or timezone == 'EDT':
        time_offset = 5
    elif timezone == 'BRT' or timezone == 'BRST':
        time_offset = 3
    elif timezone == 'GMT' or timezone == 'BST':
        time_offset = 0
    elif timezone == 'CET' or timezone == 'CEST':
        time_offset = -1
    elif timezone == 'SAST' or timezone == 'EEST':
        time_offset = -2
    elif timezone == 'IST':
        time_offset = -5.5
    elif timezone == 'CST':
        time_offset = -8
    elif timezone == 'JST':
        time_offset = -9
    elif timezone == 'AEST' or timezone == 'AEDT':
        time_offset = -10
    else:
        time_offset = 0

    return datetime.strptime(date, '%Y-%m-%d') + timedelta(hours=time_offset)


def historical_data(url_summary, soup_summary, from_date, to_date=None, day_range=None):
    """ Method for getting historical data for stocks/ETFs by specific
        dates or over a range of dates.
    """
    timezone = search_soup(soup_summary, 'div', 'id', 'quote-market-notice').split(' ')[4].replace('.', '')
    from_date = time_setup(from_date, timezone)
    if not to_date == None:
        to_date = time_setup(to_date, timezone)

    urls = []
    if to_date == None:
        timestamp = int(calendar.timegm(from_date.timetuple()))
        url = url_summary + "/history?period1=" + str(timestamp) + "&period2=" + str(timestamp) + "&interval=1d&filter=history&frequency=1d"
        urls.append(url)
    elif to_date and day_range == 'days':
        timestamp_from = int(calendar.timegm(from_date.timetuple()))
        url_from = url_summary + "/history?period1=" + str(timestamp_from) + "&period2=" + str(timestamp_from) + "&interval=1d&filter=history&frequency=1d"
        urls.append(url_from)

        timestamp_to = int(calendar.timegm(to_date.timetuple()))
        url_to = url_summary + "/history?period1=" + str(timestamp_to) + "&period2=" + str(timestamp_to) + "&interval=1d&filter=history&frequency=1d"
        urls.append(url_to)
    elif to_date and day_range == 'range':
        difference = int((to_date - from_date).days)
        
        days_per_run = 120
        number_of_runs = math.ceil(difference / days_per_run)

        for i in range(number_of_runs):
            start_at = days_per_run * i
            end_at   = days_per_run * (i+1)

            start_date = from_date + timedelta(days=start_at)
            end_date   = from_date + timedelta(days=end_at)
            if end_date > to_date:
                end_date = to_date
            
            timestamp_from = int(calendar.timegm(start_date.timetuple()))
            timestamp_to = int(calendar.timegm(end_date.timetuple()))
            url = url_summary + "/history?period1=" + str(timestamp_from) + "&period2=" + str(timestamp_to) + "&interval=1d&filter=history&frequency=1d"
            urls.append(url)

    historic_result = []
    for url in urls:
        content_history = open_page_content(url)
        soup_history = BeautifulSoup(content_history, 'html.parser')

        table = soup_history.find('table', attrs={'class': 'W(100%)'})
        table_head = table.find('thead')
        table_head_row = table_head.find_all('th')
        
        table_headings = []
        for cell in table_head_row:
            cell_text = search_soup(cell).replace('*', '')
            table_headings.append(cell_text)

        table_body = table.find('tbody')
        table_rows = table_body.find_all('tr')
        
        for row in table_rows:
            cols = row.find_all('td')
            current_row = {}
            if len(cols) != 2:
                for i in range(len(cols)):
                    cols_cell_text = search_soup(cols[i]).replace(',', '')
                    current_row[table_headings[i]] = cols_cell_text

                if not any(current_row[table_headings[0]] == cols[0] for current_row in historic_result) and \
                    not all(current_row[table_headings[i]] == '-' for i in range(1, len(current_row))):
                    historic_result.append(current_row)
            else:
                current_row_date = search_soup(cols[0]).replace(',', '')
                current_row['Date'] = current_row_date
                current_row_dividend = search_soup(cols[1]).replace(',', '')
                current_row['Dividend'] = current_row_dividend
                historic_result.append(current_row)

    if day_range == 'range':
        historic_result = sorted(historic_result, key = lambda x : datetime.strptime(x['Date'], '%b %d %Y'))

    return historic_result


class ETF:
    def __init__(self, ticker):
        self.ticker = ticker

        self.url_summary = "https://finance.yahoo.com/quote/" + self.ticker
        self.url_profile = self.url_summary + "/profile?p=" + self.ticker
        self.url_holdings = self.url_summary + "/holdings?p=" + self.ticker
        self.url_performance = self.url_summary + "/performance?p=" + self.ticker
        self.url_risk = self.url_summary + "/risk?p=" + self.ticker

        self.content_summary = open_page_content(self.url_summary)
        self.content_profile = open_page_content(self.url_profile)
        self.content_holdings = open_page_content(self.url_holdings)
        self.content_performance = open_page_content(self.url_performance)
        self.content_risk = open_page_content(self.url_risk)

        self.soup_summary = BeautifulSoup(self.content_summary, 'html.parser')
        self.soup_profile = BeautifulSoup(self.content_profile, 'html.parser')
        self.soup_holdings = BeautifulSoup(self.content_holdings, 'html.parser')
        self.soup_performance = BeautifulSoup(self.content_performance, 'html.parser')
        self.soup_risk = BeautifulSoup(self.content_risk, 'html.parser')


    def _profile_data(self, heading):
        profile_results = {}
        sections = self.soup_profile.find('div', attrs={'class' : 'W(48%) smartphone_W(100%) Fl(end)'}).find_all('div', attrs={'class' : 'Mb(25px) '})
        for section in sections:
            section_heading = search_soup(section, 'h3')
            section_rows = section.find('div').find_all('div')
            if heading == section_heading and heading == 'Fund Overview':
                for row in section_rows:
                    row_text_start = search_soup(row, 'span', 'class', 'Fl(start)')
                    row_text_end = search_soup(row, 'span', 'class', 'Fl(end)')
                    if not row_text_start == None:
                        profile_results[row_text_start] = row_text_end
                return profile_results
                
            elif heading == section_heading and heading == 'Fund Operations':
                etf_title = search_soup(section_rows[0], 'span', 'class', 'W(20%)')
                avg_title = search_soup(section_rows[0], 'span', 'class', 'W(30%)')
                if etf_title != None and avg_title != None:
                    for i in range(1, len(section_rows)):
                        attributes = search_soup(section_rows[i], 'span', 'class', 'W(50%)')
                        etf_data = search_soup(section_rows[i], 'span', 'class', 'W(20%)')
                        avg_data = search_soup(section_rows[i], 'span', 'class', 'W(30%)')
                        if not attributes == None:
                            profile_results[attributes] = {}
                            profile_results[attributes][etf_title] = etf_data
                            profile_results[attributes][avg_title] = avg_data
                return profile_results


    def _holdings_data(self, heading):
        holdings_results = {}
        section = self.soup_holdings.find('section', attrs={'class' : 'Pb(20px)'})
        top_part = section.find_all('div', attrs={'class' : 'W(48%)'})
        for part in top_part:
            part_sections = part.find_all('div', attrs={'class' : 'Mb(25px)'})
            for part_section in part_sections:
                part_section_title = search_soup(part_section, 'h3')
                if heading == part_section_title:
                    start_row = 0
                    check_section_title = part_section.find('div', attrs={'class' : 'Fz(xs)'})
                    if check_section_title:
                        start_row = 1
                    
                    part_section_contents = part_section.find('div').find_all('div')
                    for i in range(start_row, len(part_section_contents)):
                        span_content = part_section_contents[i].find_all('span')
                        if len(span_content) > 0:
                            data_key = search_soup(span_content[0])
                            data_value = search_soup(span_content[-1])
                            if not data_key == None:
                                holdings_results[data_key] = data_value

                    return holdings_results
        
        bottom_part = section.find('div', attrs={'data-test' : 'top-holdings'})
        bottom_title = search_soup(bottom_part, 'span')
        if heading in bottom_title:
            table = bottom_part.find('table')
            table_head_cells = table.find('thead').find_all('th')
            table_head_list = []
            for table_head_cell in table_head_cells:
                table_head_cell_text = search_soup(table_head_cell)
                table_head_list.append(table_head_cell_text)
            
            table_body_rows = table.find('tbody').find_all('tr')
            for table_body_row in table_body_rows:
                table_body_row_cells = table_body_row.find_all('td')
                name = search_soup(table_body_row_cells[0])
                if not name == None:
                    holdings_results[name] = {}
                    for i in range(1, len(table_body_row_cells)):
                        symbol_asset = search_soup(table_body_row_cells[i])
                        holdings_results[name][table_head_list[i]] = symbol_asset

            return holdings_results

        return

    def _performance_data(self, heading):
        performance_results = {}
        section = self.soup_performance.find('section', attrs={'class' : 'Pb(20px)'})
        section_parts = section.find_all('div', attrs={'class' : 'Mb(25px)'})
        for section_part in section_parts:
            section_part_title = search_soup(section_part, 'h3')
            if heading == section_part_title:
                section_part_list_rows = section_part.find('div').find_all('div')
                section_part_list_titles = []
                for section_part_list_row in section_part_list_rows:
                    if len(section_part_list_titles) == 0:
                        etf_head = search_soup(section_part_list_row, 'span', 'class', 'W(20%)')
                        category_head = search_soup(section_part_list_row, 'span', 'class', 'W(30%)')
                        section_part_list_titles.append(etf_head)
                        section_part_list_titles.append(category_head)
                    else:
                        column_1 = search_soup(section_part_list_row, 'span', 'class', 'W(50%)')
                        if column_1 == None:
                            column_1 = search_soup(section_part_list_row, 'span', 'class', 'W(10%)')
                        column_2 = search_soup(section_part_list_row, 'span', 'class', 'W(20%)')
                        column_3 = search_soup(section_part_list_row, 'span', 'class', 'W(30%)')
                        
                        if not column_1 == None:
                            performance_results[column_1] = {}
                            performance_results[column_1][section_part_list_titles[0]] = column_2
                            performance_results[column_1][section_part_list_titles[1]] = column_3

                return performance_results
        
        return
    

    def _risk_data(self):
        risk_results = {}
        section = self.soup_risk.find('div', attrs={'class' : 'Miw(650px)'})
        section_title_row = section.find('div', attrs={'class' : 'Fz(xs)'}).find_all('div', attrs={'class' : 'W(25%)'})
        title_list = []
        for cell in section_title_row:
            year = search_soup(cell, 'span', 'class', 'Ta(c)')
            current_etf = search_soup(cell, 'span', 'class', 'Fl(start)')
            category_avg = search_soup(cell, 'span', 'class', 'Fl(end)')
            title_list.append([year, current_etf, category_avg])
        
        section_body_rows = section.find_all('div', attrs={'class' : 'H(25px)'})
        for section_body_row in section_body_rows:
            topic = search_soup(section_body_row, 'div', 'class', 'W(24%)')
            if not topic == None:
                risk_results[topic] = {}

                body_contents = section_body_row.find_all('div', attrs={'class' : 'W(25%)'})
                for i in range(len(body_contents)):
                    etf_data = search_soup(body_contents[i], 'span', 'class', 'W(39%)')
                    avg_data = search_soup(body_contents[i], 'span', 'class', 'W(57%)')
                    risk_results[topic][title_list[i][0]] = {}
                    risk_results[topic][title_list[i][0]][title_list[i][1]] = etf_data
                    risk_results[topic][title_list[i][0]][title_list[i][2]] = avg_data
        
        return risk_results


    # Summary
    def get_stock_exchange(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '9').split(' ')[0]
    
    def get_currency(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '9').split(' ')[-1]

    def get_price(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '14')
    
    def get_change(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '17').split(' ')[0]
    
    def get_percent_change(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '17').split(' ')[1].replace('(', '').replace(')', '')
    
    def get_previous_trade_time(self):
        return search_soup(self.soup_summary, 'div', 'id', 'quote-market-notice').split(' ')[3]
    
    def get_trade_timezone(self):
        return search_soup(self.soup_summary, 'div', 'id', 'quote-market-notice').split(' ')[4].replace('.', '')
    
    def get_previous_close(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'PREV_CLOSE-value')
    
    def get_open(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'OPEN-value')
    
    def get_bid(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'BID-value')
    
    def get_ask(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'ASK-value')

    def get_day_range(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'DAYS_RANGE-value')
    
    def get_52_week_range(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'FIFTY_TWO_WK_RANGE-value')
    
    def get_volume(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'TD_VOLUME-value')
    
    def get_avg_daily_volume(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'AVERAGE_VOLUME_3MONTH-value')
    
    def get_net_assets(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'NET_ASSETS-value')
    
    def get_nav(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'NAV-value')
    
    def get_pe_ratio(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'PE_RATIO-value')
    
    def get_yield(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'TD_YIELD-value')
    
    def get_ytd_return(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'YTD_RETURN-value')
    
    def get_beta(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'BETA_3Y-value')
    
    def get_expense_ratio(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'EXPENSE_RATIO-value')
    
    def get_inception_date(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'FUND_INCEPTION_DATE-value')
    

    # Profile
    def get_company_name(self):
        return search_soup(self.soup_profile, 'h3', 'class', 'Mend(40px)')
    
    def get_company_phone(self):
        return search_soup(self.soup_profile, 'span', 'class', 'C($c-fuji-blue-1-b)')
    
    def get_fund_overview(self):
        return self._profile_data('Fund Overview')
    
    def get_fund_operations(self):
        return self._profile_data('Fund Operations')
    

    # Historical data
    def get_historical_day(self, date):
        return historical_data(self.url_summary, self.soup_summary, date)
    
    def get_historical_days(self, from_date, to_date):
        return historical_data(self.url_summary, self.soup_summary, from_date, to_date, 'days')
    
    def get_historical_range(self, from_date, to_date):
        return historical_data(self.url_summary, self.soup_summary, from_date, to_date, 'range')
    

    # Holdings
    def get_portfolio_composition(self):
        return self._holdings_data('Overall Portfolio Composition (%)')

    def get_sector_weightings(self):
        return self._holdings_data('Sector Weightings (%)')

    def get_equity_holdings(self):
        return self._holdings_data('Equity Holdings')
    
    def get_bond_ratings(self):
        return self._holdings_data('Bond Ratings')
    
    def get_top_10_holdings(self):
        return self._holdings_data('Total Assets')
    

    # Performance
    def get_trailing_returns_vs_benchmark(self):
        return self._performance_data('Trailing Returns (%) Vs. Benchmarks')
    
    def get_annual_total_return_history(self):
        return self._performance_data('Annual Total Return (%) History')


    # Risk
    def get_risk_statistics(self):
        return self._risk_data()


    # Refresh newest content
    def refresh(self):
        self.__init__(self.ticker)


class Share:
    def __init__(self, ticker):
        self.ticker = ticker

        self.url_summary = "https://finance.yahoo.com/quote/" + self.ticker
        self.url_statistics = self.url_summary + "/key-statistics?p=" + self.ticker
        self.url_profile = self.url_summary + "/profile?p=" + self.ticker
        self.url_analysts = self.url_summary + "/analysts?p=" + self.ticker

        self.content_summary = open_page_content(self.url_summary)
        self.content_statistics = open_page_content(self.url_statistics)
        self.content_profile = open_page_content(self.url_profile)
        self.content_analysts = open_page_content(self.url_analysts)

        self.soup_summary = BeautifulSoup(self.content_summary, 'html.parser')
        self.soup_statistics = BeautifulSoup(self.content_statistics, 'html.parser')
        self.soup_profile = BeautifulSoup(self.content_profile, 'html.parser')
        self.soup_analysts = BeautifulSoup(self.content_analysts, 'html.parser')

    
    def _statistics_search(self, heading, search_for=None):
        table_section = ''
        head_sections = self.soup_statistics.find_all('h2')
        for i in range(len(head_sections)):
            head_section = search_soup(head_sections[i])
            if heading == head_section:
                table_section = head_sections[i].find_next_sibling()
                break
        
        statistics_search = {}
        tables = table_section.find_all('table')
        for table in tables:
            table_body = table.find('tbody')
            table_rows = table_body.find_all('tr')
            for row in table_rows:
                cells = row.find_all('td')
                cell_topic = search_soup(cells[0], 'span')
                cell_content = search_soup(cells[1])
                if not cell_topic == None:
                    if search_for == None:
                        statistics_search[cell_topic] = cell_content
                    elif cell_topic == search_for:
                        return cell_content
        
        if search_for == None:
            return statistics_search
        return None


    def _company_address(self, tag, attribute, value):
        company_location = self.soup_profile.find(tag, attrs={attribute : value})
        
        company_address = {}
        element_counter = 0
        for element in company_location:
            element_counter += 1
            if element_counter == 2:
                company_address['street'] = element
            elif element_counter == 6:
                company_address['address'] = element
            elif element_counter == 10:
                company_address['country'] = element
        return company_address

    
    def _key_executives(self, tag, attribute, value):
        table = self.soup_profile.find(tag, attrs={attribute : value})
        table_head = table.find('thead').find('tr')
        table_head_row = table_head.find_all('th')

        table_headings = []
        for row in table_head_row:
            row_text = search_soup(row)
            table_headings.append(row_text)

        table_body = table.find('tbody')
        table_rows = table_body.find_all('tr')
            
        key_executive_result = []
        for row in table_rows:
            cols = row.find_all('td')
            current_row = {}
            for i in range(len(cols)):
                cell_data = search_soup(cols[i])
                current_row[table_headings[i]] = cell_data
            key_executive_result.append(current_row)

        return key_executive_result

    
    def _analysts_search(self, heading):
        analysts_search_result = {}
        table_headings = []

        all_tables = self.soup_analysts.find_all('table')

        for table in all_tables:
            table_head = table.find('thead')
            table_head_row = table_head.find('tr').find_all('th')
            table_title = search_soup(table_head_row[0])
            if heading == table_title:
                for i in range(1, len(table_head_row)):
                    table_heading_content = search_soup(table_head_row[i])
                    table_headings.append(table_heading_content)

                table_body = table.find('tbody').find_all('tr')
                for table_body_row in table_body:
                    table_body_row_cell = table_body_row.find_all('td')
                    table_row_name = search_soup(table_body_row_cell[0])
                    if not table_row_name == None:
                        analysts_search_result[table_row_name] = {}
                        for j in range(1, len(table_body_row_cell)):
                            table_row_cell = search_soup(table_body_row_cell[j])
                            analysts_search_result[table_row_name][table_headings[j-1]] = table_row_cell

        return analysts_search_result

    
    # Summary
    def get_stock_exchange(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '9').split(' ')[0]
    
    def get_currency(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '9').split(' ')[-1]

    def get_price(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '14')
    
    def get_change(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '17').split(' ')[0]
    
    def get_percent_change(self):
        return search_soup(self.soup_summary, 'span', 'data-reactid', '17').split(' ')[1].replace('(', '').replace(')', '')
    
    def get_previous_trade_time(self):
        return search_soup(self.soup_summary, 'div', 'id', 'quote-market-notice').split(' ')[3]
    
    def get_trade_timezone(self):
        return search_soup(self.soup_summary, 'div', 'id', 'quote-market-notice').split(' ')[4].replace('.', '')
    
    def get_previous_close(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'PREV_CLOSE-value')
    
    def get_open(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'OPEN-value')
    
    def get_bid(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'BID-value')
    
    def get_ask(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'ASK-value')

    def get_day_range(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'DAYS_RANGE-value')
    
    def get_52_week_range(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'FIFTY_TWO_WK_RANGE-value')
    
    def get_volume(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'TD_VOLUME-value')
    
    def get_avg_daily_volume(self):
        return search_soup(self.soup_summary, 'td', 'data-test', 'AVERAGE_VOLUME_3MONTH-value')
    

    # Custom Statistics Search
    def get_custom_statistics_search(self, heading, row=None):
        return self._statistics_search(heading, row)


    # Statistics | Valuation measures
    def get_valuation_measures(self):
        return self._statistics_search('Valuation Measures')

    def get_market_cap(self):
        return self._statistics_search('Valuation Measures', 'Market Cap (intraday)')
    
    def get_enterprise_value(self):
        return self._statistics_search('Valuation Measures', 'Enterprise Value')

    def get_trailing_pe(self):
        return self._statistics_search('Valuation Measures', 'Trailing P/E')
    
    def get_forward_pe(self):
        return self._statistics_search('Valuation Measures', 'Forward P/E')
    
    def get_peg_ratio(self):
        return self._statistics_search('Valuation Measures', 'PEG Ratio (5 yr expected)')
    
    def get_price_per_sales(self):
        return self._statistics_search('Valuation Measures', 'Price/Sales')
    
    def get_price_per_book(self):
        return self._statistics_search('Valuation Measures', 'Price/Book')

    def get_enterprise_value_per_revenue(self):
        return self._statistics_search('Valuation Measures', 'Enterprise Value/Revenue')

    def get_enterprise_value_per_ebitda(self):
        return self._statistics_search('Valuation Measures', 'Enterprise Value/EBITDA')
    

    # Statistics | Financial highlights
    def get_financial_highlights(self):
        return self._statistics_search('Financial Highlights')

    def get_fiscal_year_ends(self):
        return self._statistics_search('Financial Highlights', 'Fiscal Year Ends')
    
    def get_most_recent_quarter(self):
        return self._statistics_search('Financial Highlights', 'Most Recent Quarter')
    
    def get_profit_margin(self):
        return self._statistics_search('Financial Highlights', 'Profit Margin')
    
    def get_operating_margin(self):
        return self._statistics_search('Financial Highlights', 'Operating Margin')
    
    def get_return_assets(self):
        return self._statistics_search('Financial Highlights', 'Return on Assets')
    
    def get_return_equity(self):
        return self._statistics_search('Financial Highlights', 'Return on Equity')
    
    def get_revenue(self):
        return self._statistics_search('Financial Highlights', 'Revenue')

    def get_revenue_per_share(self):
        return self._statistics_search('Financial Highlights', 'Revenue Per Share')
    
    def get_quarterly_revenue_growth(self):
        return self._statistics_search('Financial Highlights', 'Quarterly Revenue Growth')

    def get_gross_profit(self):
        return self._statistics_search('Financial Highlights', 'Gross Profit')
    
    def get_ebitda(self):
        return self._statistics_search('Financial Highlights', 'EBITDA')
    
    def get_net_income_avi_to_common(self):
        return self._statistics_search('Financial Highlights', 'Net Income Avi to Common')

    def get_diluted_eps(self):
        return self._statistics_search('Financial Highlights', 'Diluted EPS')
    
    def get_quarterly_earnings_growth(self):
        return self._statistics_search('Financial Highlights', 'Quarterly Earnings Growth')
    
    def get_total_cash(self):
        return self._statistics_search('Financial Highlights', 'Total Cash')
    
    def get_total_cash_per_share(self):
        return self._statistics_search('Financial Highlights', 'Total Cash Per Share')
    
    def get_total_debt(self):
        return self._statistics_search('Financial Highlights', 'Total Debt')
    
    def get_total_debt_per_equity(self):
        return self._statistics_search('Financial Highlights', 'Total Debt/Equity')
    
    def get_current_ratio(self):
        return self._statistics_search('Financial Highlights', 'Current Ratio')
    
    def get_book_value_per_share(self):
        return self._statistics_search('Financial Highlights', 'Book Value Per Share')
    
    def get_operating_cash_flow(self):
        return self._statistics_search('Financial Highlights', 'Operating Cash Flow')
    
    def get_levered_free_cash_flow(self):
        return self._statistics_search('Financial Highlights', 'Levered Free Cash Flow')
    

    # Statistics | Trading information
    def get_trading_information(self):
        return self._statistics_search('Trading Information')

    def get_beta(self):
        return self._statistics_search('Trading Information', 'Beta')
    
    def get_52_week_change(self):
        return self._statistics_search('Trading Information', '52-Week Change')
    
    def get_sp500_52_week_change(self):
        return self._statistics_search('Trading Information', 'S&P500 52-Week Change')
    
    def get_52_week_high(self):
        return self._statistics_search('Trading Information', '52 Week High')
    
    def get_52_week_low(self):
        return self._statistics_search('Trading Information', '52 Week Low')
    
    def get_50_day_average(self):
        return self._statistics_search('Trading Information', '50-Day Moving Average')
    
    def get_200_day_average(self):
        return self._statistics_search('Trading Information', '200-Day Moving Average')
    
    def get_avg_3_month_volume(self):
        return self._statistics_search('Trading Information', 'Avg Vol (3 month)')
    
    def get_avg_10_day_volume(self):
        return self._statistics_search('Trading Information', 'Avg Vol (10 day)')
    
    def get_shares_outstanding(self):
        return self._statistics_search('Trading Information', 'Shares Outstanding')
    
    def get_float(self):
        return self._statistics_search('Trading Information', 'Float')

    def get_percent_held_insiders(self):
        return self._statistics_search('Trading Information', '% Held by Insiders')
    
    def get_percent_held_institutions(self):
        return self._statistics_search('Trading Information', '% Held by Institutions')
    
    def get_shares_short(self):
        return self._statistics_search('Trading Information', 'Shares Short')

    def get_short_ratio(self):
        return self._statistics_search('Trading Information', 'Short Ratio')
    
    def get_short_percent_of_float(self):
        return self._statistics_search('Trading Information', 'Short % of Float')
    
    def get_shares_short_prior(self):
        return self._statistics_search('Trading Information', 'Shares Short (prior month)')
    
    def get_forward_dividend_rate(self):
        return self._statistics_search('Trading Information', 'Forward Annual Dividend Rate')
    
    def get_forward_dividend_yield(self):
        return self._statistics_search('Trading Information', 'Forward Annual Dividend Yield')
    
    def get_trailing_dividend_rate(self):
        return self._statistics_search('Trading Information', 'Trailing Annual Dividend Rate')
    
    def get_trailing_dividend_yield(self):
        return self._statistics_search('Trading Information', 'Trailing Annual Dividend Yield')
    
    def get_5_year_avg_dividend_yield(self):
        return self._statistics_search('Trading Information', '5 Year Average Dividend Yield')
    
    def get_payout_ratio(self):
        return self._statistics_search('Trading Information', 'Payout Ratio')
    
    def get_dividend_date(self):
        return self._statistics_search('Trading Information', 'Dividend Date')
    
    def get_exdividend_date(self):
        return self._statistics_search('Trading Information', 'Ex-Dividend Date')
    
    def get_last_split_factor(self):
        return self._statistics_search('Trading Information', 'Last Split Factor (new per old)')
    
    def get_last_split_date(self):
        return self._statistics_search('Trading Information', 'Last Split Date')
    

    # Profile | Company information
    def get_company_name(self):
        return search_soup(self.soup_profile, 'h3', 'class', 'Fz(m)')
    
    def get_company_address(self):
        return self._company_address('p', 'data-reactid', '8')
    
    def get_company_phone_number(self):
        return search_soup(self.soup_profile, 'a', 'data-reactid', '15')

    def get_company_website(self):
        return search_soup(self.soup_profile, 'a', 'target', '_blank')
    
    def get_sector(self):
        return search_soup(self.soup_profile, 'strong', 'data-reactid', '21')
    
    def get_industry(self):
        return search_soup(self.soup_profile, 'strong', 'data-reactid', '25')
    
    def get_number_of_full_time_employees(self):
        return search_soup(self.soup_profile, 'strong', 'data-reactid', '29')
    
    def get_key_executives(self):
        return self._key_executives('table', 'class', 'W(100%)')
 
    
    # Historical data
    def get_historical_day(self, date):
        return historical_data(self.url_summary, self.soup_summary, date)
    
    def get_historical_days(self, from_date, to_date):
        return historical_data(self.url_summary, self.soup_summary, from_date, to_date, 'days')
    
    def get_historical_range(self, from_date, to_date):
        return historical_data(self.url_summary, self.soup_summary, from_date, to_date, 'range')
    

    # Custom Analysts Search
    def get_custom_analysts_search(self, heading):
        return self._analysts_search(heading)


    # Analysts
    def get_analysts_earnings_estimate(self):
        return self._analysts_search('Earnings Estimate')
    
    def get_analysts_revenue_estimate(self):
        return self._analysts_search('Revenue Estimate')
    
    def get_analysts_earnings_history(self):
        return self._analysts_search('Earnings History')
    
    def get_analysts_eps_trend(self):
        return self._analysts_search('EPS Trend')
    
    def get_analysts_eps_revisions(self):
        return self._analysts_search('EPS Revisions')
    
    def get_analysts_growth_estimates(self):
        return self._analysts_search('Growth Estimates')


    # Refresh newest content
    def refresh(self):
        self.__init__(self.ticker)
