from bs4 import BeautifulSoup
import requests
import csv
import match_report

def get_seasons(url, header):
        seasons_link_exts = []

        response = requests.get(url, header)

        if response.status_code == 200:
                html_soup = BeautifulSoup(response.text, 'html.parser')

                table_element = html_soup.find('table')
                rows = table_element.find_all('tr')

                for r in rows:
                        columns = r.find_all('td')
                        for c in columns:
                                if c['data-stat'] == 'league_name' and c.text.strip() == "Premier League" :
                                        seasons_link_exts.append(c.find('a')['href'])
        
        return seasons_link_exts

def get_matches(url, header, links):
        data_list = []
        for ext in links:
                data_list.append(match_report.get_match_report(url + ext, header))
        return data_list

# MAIN STARTS HERE 
URL = "https://fbref.com" # Base website link
ext = "/en/comps/9/history/Premier-League-Seasons" # Extension for soccer seasons
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
          'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0 [ip:165.1.169.144]"}

# =========== CSV File Writing ===========
# Open a CSV file for writing
with open('match_report_info.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write header row
        header = ["Date", "Venue", "Attendance", "Refree", "Home Team", "Home xG", "Home Goals", "Home Formation", "Home Possession %", "Home Passing Accuracy", "Home Shots On", 
                  "Home Saves", "Home Fouls", "Home Corners", "Home Crosses", "Home Touches", "Home Intercepts", "Home Aerials Won", "Home Clearances", "Home Offsides", 
                  "Home Goal Kicks", "Home Throw Ins", "Home Long Balls", "Away Team", "Away xG", "Away Goals", "Away Formation", "Away Possession %", "Away Passing Accuracy", 
                  "Away Shots On", "Away Saves", "Away Fouls", "Away Corners", "Away Crosses", "Away Touches", "Away Intercepts", "Away Aerials Won", "Away Clearances", 
                  "Away Offsides", "Away Goal Kicks", "Away Throw Ins", "Away Long Balls"]
        writer.writerow(header)

        # Running method to get all applicable seasons
        links = get_seasons(URL + ext, HEADER)
        
        # Write data to CSV
        data = get_matches(URL, HEADER, links)
        while data:
                writer.writerow(data.pop())
        
        print("Match information written to CSV file.")