import yahoo_fs
import urllib.request
import requests
from bs4 import BeautifulSoup


file = open("sample_html.html")

item = BeautifulSoup(file, "html.parser")
item.find_all("table")

url = "https://harrypotter.fandom.com/wiki/Harry_Potter"
type(urllib.request.urlopen(url).read())

ticker = yahoo_fs.Share("AAPL")


ticker.get_52_week_change()
ticker.get_peg_ratio()

requests.get(url).content

print(ticker.get_historical_days('2018-03-19', '2018-03-23'))

ticker.get_previous_close()


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


search_soup(head_sections[0])
search_for = "PEG Ratio (5 yr expected)"

head_sections = item.find_all("h2")
for i in range(len(head_sections)):
    head_section = search_soup(head_sections[i])
    if "Valuation Measures" == head_section:
        table_section = head_sections[i].find_next_sibling()
        try:
            while search_for not in table_section.text:
                table_section = table_section.find_next_sibling()
        except ValueError:
            print(f"No table value found for {search_for}")

head_sections
search_for in table_section2

def _statistics_search(heading, search_for=None):
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
