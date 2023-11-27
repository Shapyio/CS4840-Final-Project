from bs4 import BeautifulSoup
import requests

url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}

response = requests.get(url, headers=header)

if response.status_code == 200:
        html_soup = BeautifulSoup(response.text, 'html.parser')

        table_element = html_soup.find('table')
        rows = table_element.find_all('tr')

        count = 0
        for r in rows:
                count = count + 1
                columns = r.find_all('td')
                for c in columns:
                        if c['data-stat'] == 'match_report' and c.text.strip() == "Match Report" :
                                print(count, ". ", c.find('a')['href'])