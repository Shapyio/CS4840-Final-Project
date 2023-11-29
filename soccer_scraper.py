from bs4 import BeautifulSoup
import requests
import csv
import match_report
import re

def get_seasons(url, header):
        print("GETTING SEASONS...", end='')
        seasons_link_exts = []

        response = requests.get(url, header)

        if response.status_code == 200:
                html_soup = BeautifulSoup(response.text, 'html.parser')

                table_element = html_soup.find('table')
                # Gets every element part of rows
                seasons = table_element.find_all('th', {'data-stat' : 'year_id', 'scope' : 'row'})

                for s in seasons:
                        if s.find('a') and s.find('a').text.strip() != "1993-1994":
                                seasons_link_exts.append(s.find('a')['href'])
                        else:
                                break
        print("DONE")
        return seasons_link_exts

def get_matches(url, header, links):
        print("GETTING MATCHES...", end='')
        matches_links_list = []
        for ext in links:

                response = requests.get(url + ext, header)

                if response.status_code == 200:
                        html_soup = BeautifulSoup(response.text, 'html.parser')

                        table_element = html_soup.find('table')
                        rows = table_element.find_all('tr')

                        for r in rows:
                                columns = r.find_all('td')
                                for c in columns:
                                        if c['data-stat'] == 'match_report' and c.text.strip() == "Match Report" :
                                                matches_links_list.append(c.find('a')['href'])
        
        print("DONE")
        return matches_links_list

def convert_urls(original_urls):
    print("FORMATTING URLS...", end='')
    converted_urls = []
    # Use regular expression to match the pattern and extract relevant parts
    for url in original_urls:
        match = re.match(r"(/en/comps/9/\d{4}-\d{4}/)(\d{4}-\d{4}-Premier-League-Stats)", url)

        if match:
                # Extract matched parts
                prefix = match.group(1)
                suffix = match.group(2)

                # Construct the converted URL
                converted_url = f"{prefix}schedule/{suffix}-Premier-League-Scores-and-Fixtures"

                converted_urls.append(converted_url)

        print("DONE")
        # Return the original URL if no match is found
        return converted_urls

# MAIN STARTS HERE 
URL = "https://fbref.com" # Base website link
EXT = "/en/comps/9/history/Premier-League-Seasons" # Extension for soccer seasons
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
        links = get_seasons(URL + EXT, HEADER)
        links = convert_urls(get_seasons(URL + EXT, HEADER))
        # Conversion removes current season so I added it in manually
        links.insert(0, "/en/comps/9/schedule/Premier-League-Scores-and-Fixtures")
        # From season links, get all the matches
        links = get_matches(URL, HEADER, links) 
        print("NUMBER OF MATCHES: ", len(links))
        print("STARTING TO WRITE DATA...")
        # Write data to CSV
        for i in links:
                writer.writerow((match_report.get_match_report(URL + i, HEADER)))
        print("DONE")
        
        print("Match information written to CSV file.")