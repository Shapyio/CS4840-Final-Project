from bs4 import BeautifulSoup
import requests

seasons_link_exts = []

url = "https://fbref.com" # Base website link
ext = "/en/comps/9/history/Premier-League-Seasons" # Extension for soccer seasons
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}

# This method should be able to be used for past seasons page, season games pages, and match report pages
def html_table_parser(url, ext, header):
        csv_list = [] # List containing all CSV data
        response = requests.get(url + ext, header)

        if response.status_code == 200:
                html_soup = BeautifulSoup(response.text, 'html.parser')

                table_element = html_soup.find('table')
                rows = table_element.find_all('tr')

                for r in rows:
                        columns = r.find_all('td')
                        for c in columns:
                                if c['data-stat'] == 'league_name' and c.text.strip() == "Premier League" :
                                        response = requests.get(url + c.find('a')['href'], header)

                print(seasons_link_exts)
        
        return csv_list
