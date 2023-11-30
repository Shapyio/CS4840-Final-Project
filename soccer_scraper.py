from bs4 import BeautifulSoup
import requests
import csv
import re
import os
import random
import time

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

def get_matches(url, ext):
    matches_links_list = []
    header = random.choice(HEADER)
    response = requests.get(url + ext, headers=header)
    if response.status_code == 200:
            html_soup = BeautifulSoup(response.text, 'html.parser')

            table_element = html_soup.find('table')
            rows = table_element.find_all('tr')

            for r in rows:
                    columns = r.find_all('td')
                    for c in columns:
                            if c['data-stat'] == 'match_report' and c.text.strip() == "Match Report" :
                                    matches_links_list.append(c.find('a')['href'])
    return matches_links_list

def convert_urls(original_urls):
    print("FORMATTING URLS...", end='')
    converted_urls = []
    # Use regular expression to match the pattern and extract relevant parts
    count = 0
    for url in original_urls:
            match = re.match(r"(/en/comps/9/\d{4}-\d{4}/)(\d{4}-\d{4}-Premier-League-Stats)", url)

            if match:
                    # Extract matched parts
                    prefix = match.group(1)
                    suffix = match.group(2)
                    # Construct the converted URL
                    converted_url = f"{prefix}schedule/{suffix}-Premier-League-Scores-and-Fixtures"
                    converted_urls.append(converted_url)
            count+=1

    print("DONE\nCONVERTED: ", str(len(converted_urls)), " URLS.")
    # Return the original URL if no match is found
    return converted_urls

# Function to read the list of links from a file
def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        links = [line.strip() for line in file.readlines()]
    return links

# Function to write the list of links to a file
def create_file(file_path):
    with open(file_path, 'w') as file:
        print("FILE CREATED")

# Function to append the list of links to a file
def append_links_to_file(file_path, links):
    with open(file_path, 'a') as file:
        for link in links:
            file.write(f"{link}\n")

# Function to append the list of links to a file
def write_links_to_file(file_path, links):
    with open(file_path, 'w') as file:
        for link in links:
            file.write(f"{link}\n")

def get_match_report(match_report_url):
    header = random.choice(HEADER)

    response = requests.get(match_report_url, headers=header)
    
    if response.status_code == 200:
        match_report_soup = BeautifulSoup(response.text, 'html.parser')
        with open('last_operation_log.txt', 'w', newline='', encoding='utf-8') as file:
            file.write("CURRENT SITE: " + match_report_url + "\n\n")
            file.write("LOADED: " + match_report_soup.prettify())
            file.write("EOS===================STOP")
        scorebox_soup = match_report_soup.find('div', {'class': 'scorebox'})
        field_wrap_soup = match_report_soup.find('div', {'id' : 'field_wrap'})
        team_stats_soup = match_report_soup.find('div', {'id' : 'team_stats'})
        team_stats_extra_soup = match_report_soup.find('div', {'id' : 'team_stats_extra'})

        # =========== Match Venue Info ===========
        score_metabox_soup = scorebox_soup.find('div', {'class': 'scorebox_meta'})

        # DATE
        date_element = score_metabox_soup.find('span', {'class' : 'venuetime'})
        date = date_element.get('data-venue-date') if date_element else "Date not found"

        # VENUE
        venue_element = score_metabox_soup.find_all('div')[-2].find_all('small')[-1]
        venue = venue_element.text.strip() if venue_element else "Venue not found"

        # ATTENDANCE
        if len(score_metabox_soup.find_all('div')[-3].find_all('small')) >= 2:
            attendance_element = score_metabox_soup.find_all('div')[-3].find_all('small')[-1]
            attendance = attendance_element.text.strip() if attendance_element else "Attendance not found"
        else:
            attendance = "Attendance not found"

        # REFREE
        refree_element = score_metabox_soup.find_all('div')[-1].find('small').find_next().find('span')
        refree = refree_element.text.strip() if refree_element else "Refree not found"
        refree = refree.split(' (', 1)[0] # To remove '(Refree)' at end of text

        # =========== Home Team Info ===========

        # Home Team Name
        home_team_element = scorebox_soup.find_all('div', {'class' : 'media-item logo loader'})[0].find_next('a')
        home_team = home_team_element.text.strip() if home_team_element else "Home team name not found"

        # Home Expected Goals - REMOVED because not many seasons before 2010s have xG
        #home_xg_element = scorebox_soup.find_all()[0].find('div', {'class' : 'score_xg'})
        #home_xg = home_xg_element.text.strip() if home_xg_element else "Home xG not found"

        # Home Goals
        home_goals_element = scorebox_soup.find_all()[0].find('div', {'class' : 'score'})
        home_goals = home_goals_element.text.strip() if home_goals_element else "Home goals not found"

        # Home Team Formation
        home_formation_element = field_wrap_soup.find('div', {'class' : 'lineup', 'id' : 'a'}).find('th')
        home_formation = home_formation_element.text.strip() if home_formation_element else "Home formation not found"
        home_formation = re.search(r'\((.*?)\)', home_formation).group(1) # I don't understand how "re" works. But it does. 

        # Home Possession %
        home_possession_element = team_stats_soup.find_all('tr')[2].find_all('td')[0].find('strong')
        home_possession = home_possession_element.text.strip() if home_possession_element else "Home possession % not found"

        # Home Passing Accuracy
        home_passing_accuracy_element = team_stats_soup.find_all('tr')[4].find_all('td')[0].find('strong')
        home_passing_accuracy = home_passing_accuracy_element.text.strip() if home_passing_accuracy_element else "Home passing % not found"

        # Home Shots on Target
        home_shots_on_element = team_stats_soup.find_all('tr')[6].find_all('td')[0].find('strong')
        home_shots_on = home_shots_on_element.text.strip() if home_shots_on_element else "Home shots on target % not found"
        
        # Home Saves
        home_saves_element = team_stats_soup.find_all('tr')[8].find_all('td')[0].find('strong')
        home_saves = home_saves_element.text.strip() if home_saves_element else "Home saves % not found"

        # Home Fouls
        home_fouls_element = team_stats_extra_soup.find_all()[4]
        home_fouls = home_fouls_element.text.strip() if home_fouls_element else "Home fouls not found"

        # Home Corners
        home_corners_element = team_stats_extra_soup.find_all()[7]
        home_corners = home_corners_element.text.strip() if home_corners_element else "Home corners not found"

        # Home Crosses
        home_crosses_element = team_stats_extra_soup.find_all()[10]
        home_crosses = home_crosses_element.text.strip() if home_crosses_element else "Home crosses not found"

        # Home Touches
        home_touches_element = team_stats_extra_soup.find_all()[13]
        home_touches = home_touches_element.text.strip() if home_touches_element else "Home touches not found"

        # Home Tackles
        home_tackles_element = team_stats_extra_soup.find_all()[20]
        home_tackles = home_tackles_element.text.strip() if home_tackles_element else "Home tackles not found"

        # Home Interceptions
        home_interceptions_element = team_stats_extra_soup.find_all()[23]
        home_interceptions = home_interceptions_element.text.strip() if home_interceptions_element else "Home interceptions not found"

        # Home Aerials Won
        home_aerials_element = team_stats_extra_soup.find_all()[26]
        home_aerials = home_aerials_element.text.strip() if home_aerials_element else "Home aerials won not found"

        # Home Clearances
        home_clearances_element = team_stats_extra_soup.find_all()[29]
        home_clearances = home_clearances_element.text.strip() if home_clearances_element else "Home clearances not found"

        # Home Offsides
        home_offsides_element = team_stats_extra_soup.find_all()[36]
        home_offsides = home_offsides_element.text.strip() if home_offsides_element else "Home offsides not found"

        # Home Goal Kicks
        home_gk_element = team_stats_extra_soup.find_all()[39]
        home_gk = home_gk_element.text.strip() if home_gk_element else "Home goal kicks not found"

        # Home Throw Ins
        home_ti_element = team_stats_extra_soup.find_all()[42]
        home_ti = home_ti_element.text.strip() if home_ti_element else "Home throw ins won not found"

        # Home Long Balls
        home_lb_element = team_stats_extra_soup.find_all()[45]
        home_lb = home_lb_element.text.strip() if home_lb_element else "Home long balls not found"

        # =========== Away Team Info ===========

        # Away Team Name
        away_team_element = scorebox_soup.find_all('div', {'class' : 'media-item logo loader'})[1].find_next('a')
        away_team = away_team_element.text.strip() if away_team_element else "Away team name not found"

        # Away Expected Goals - REMOVED because not many seasons before 2010s have xG
        #away_xg_element = scorebox_soup.find_all('div', {'class' : 'score_xg'})[-1]
        #away_xg = away_xg_element.text.strip() if away_xg_element else "Away xG not found"

        # Away Goals
        away_goals_element = scorebox_soup.find_all('div', {'class' : 'score'})[-1]
        away_goals = away_goals_element.text.strip() if away_goals_element else "Away goals not found"

        # Away Team Formation
        away_formation_element = field_wrap_soup.find('div', {'class' : 'lineup', 'id' : 'b'}).find('th')
        away_formation = away_formation_element.text.strip() if away_formation_element else "Away formation not found"
        away_formation = re.search(r'\((.*?)\)', away_formation).group(1) # I don't understand how "re" works. But it does. 

        # Away Possession %
        away_possession_element = team_stats_soup.find_all('tr')[2].find_all('td')[1].find('strong')
        away_possession = away_possession_element.text.strip() if away_possession_element else "Away possession % not found"

        # Away Passing Accuracy
        away_passing_accuracy_element = team_stats_soup.find_all('tr')[4].find_all('td')[1].find('strong')
        away_passing_accuracy = away_passing_accuracy_element.text.strip() if away_passing_accuracy_element else "Away passing % not found"

        # Away Shots on Target
        away_shots_on_element = team_stats_soup.find_all('tr')[6].find_all('td')[1].find('strong')
        away_shots_on = away_shots_on_element.text.strip() if away_shots_on_element else "Away shots on target % not found"
        
        # Away Saves
        away_saves_element = team_stats_soup.find_all('tr')[8].find_all('td')[1].find('strong')
        away_saves = away_saves_element.text.strip() if away_saves_element else "Away saves % not found"

        # Away Fouls
        away_fouls_element = team_stats_extra_soup.find_all()[6]
        away_fouls = away_fouls_element.text.strip() if away_fouls_element else "Away fouls not found"

        # Away Corners
        away_corners_element = team_stats_extra_soup.find_all()[9]
        away_corners = away_corners_element.text.strip() if away_corners_element else "Away corners not found"

        # Away Crosses
        away_crosses_element = team_stats_extra_soup.find_all()[12]
        away_crosses = away_crosses_element.text.strip() if away_crosses_element else "Away crosses not found"

        # Away Touches
        away_touches_element = team_stats_extra_soup.find_all()[15]
        away_touches = away_touches_element.text.strip() if away_touches_element else "Away touches not found"

        # Away Tackles
        away_tackles_element = team_stats_extra_soup.find_all()[22]
        away_tackles = away_tackles_element.text.strip() if away_tackles_element else "Away tackles not found"

        # Away Interceptions
        away_interceptions_element = team_stats_extra_soup.find_all()[25]
        away_interceptions = away_interceptions_element.text.strip() if away_interceptions_element else "Away interceptions not found"

        # Away Aerials Won
        away_aerials_element = team_stats_extra_soup.find_all()[28]
        away_aerials = away_aerials_element.text.strip() if away_aerials_element else "Away aerials won not found"

        # Away Clearances
        away_clearances_element = team_stats_extra_soup.find_all()[31]
        away_clearances = away_clearances_element.text.strip() if away_clearances_element else "Away clearances not found"

        # Away Offsides
        away_offsides_element = team_stats_extra_soup.find_all()[38]
        away_offsides = away_offsides_element.text.strip() if away_offsides_element else "Away offsides not found"

        # Away Goal Kicks
        away_gk_element = team_stats_extra_soup.find_all()[41]
        away_gk = away_gk_element.text.strip() if away_gk_element else "Away goal kicks not found"

        # Away Throw Ins
        away_ti_element = team_stats_extra_soup.find_all()[44]
        away_ti = away_ti_element.text.strip() if away_ti_element else "Away throw ins won not found"

        # Away Long Balls
        away_lb_element = team_stats_extra_soup.find_all()[47]
        away_lb = away_lb_element.text.strip() if away_lb_element else "Away long balls not found"


        # Write data to CSV
        data = [date, venue, attendance, refree, home_team, home_goals, home_formation, home_possession, home_passing_accuracy, home_shots_on, home_saves, home_fouls,
                    home_corners, home_crosses, home_touches, home_interceptions, home_aerials, home_clearances, home_offsides, home_gk, home_ti, home_lb, away_team, 
                    away_goals, away_formation, away_possession, away_passing_accuracy, away_shots_on, away_saves, away_fouls, away_corners, away_crosses, away_touches, 
                    away_interceptions, away_aerials, away_clearances, away_offsides, away_gk, away_ti, away_lb]
        
    return data

# MAIN STARTS HERE 
URL = 'https://fbref.com' # Base website link
HEADER = [{"User-Agent": "Mozilla/5.0 (Windows NT 10.1; Win64; x64; en-US) AppleWebKit/603.26 (KHTML, like Gecko) Chrome/48.0.1177.392 Safari/535.9 Edge/16.19452"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0 [ip:165.1.169.144]"},
        {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 10.4; Win64; x64) AppleWebKit/603.28 (KHTML, like Gecko) Chrome/52.0.3838.306 Safari/601.0 Edge/14.17115"},
        {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 10.1; x64; en-US) AppleWebKit/537.45 (KHTML, like Gecko) Chrome/50.0.1744.251 Safari/602.2 Edge/14.38768"}]
LINKS_PATH = 'matches_links.txt'
MATCHES_PER_SEASON = {'/en/comps/9/schedule/Premier-League-Scores-and-Fixtures': 130, 
                      '/en/comps/9/2022-2023/schedule/2022-2023-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 439,
                      '/en/comps/9/2021-2022/schedule/2021-2022-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 458, 
                      '/en/comps/9/2020-2021/schedule/2020-2021-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 449, 
                      '/en/comps/9/2019-2020/schedule/2019-2020-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 429,
                      '/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 434,
                      '/en/comps/9/2017-2018/schedule/2017-2018-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 432,
                      '/en/comps/9/2016-2017/schedule/2016-2017-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 433,
                      '/en/comps/9/2015-2016/schedule/2015-2016-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 435,
                      '/en/comps/9/2014-2015/schedule/2014-2015-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 431,
                      '/en/comps/9/2013-2014/schedule/2013-2014-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 433,
                      '/en/comps/9/2012-2013/schedule/2012-2013-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 432,
                      '/en/comps/9/2011-2012/schedule/2011-2012-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 431,
                      '/en/comps/9/2010-2011/schedule/2010-2011-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 435,
                      '/en/comps/9/2009-2010/schedule/2009-2010-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 444,
                      '/en/comps/9/2008-2009/schedule/2008-2009-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 434,
                      '/en/comps/9/2007-2008/schedule/2007-2008-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 431,
                      '/en/comps/9/2006-2007/schedule/2006-2007-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 439,
                      '/en/comps/9/2005-2006/schedule/2005-2006-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 443,
                      '/en/comps/9/2004-2005/schedule/2004-2005-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 435,
                      '/en/comps/9/2003-2004/schedule/2003-2004-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 435,
                      '/en/comps/9/2002-2003/schedule/2002-2003-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 436,
                      '/en/comps/9/2001-2002/schedule/2001-2002-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 443,
                      '/en/comps/9/2000-2001/schedule/2000-2001-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 437,
                      '/en/comps/9/1999-2000/schedule/1999-2000-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 441,
                      '/en/comps/9/1998-1999/schedule/1998-1999-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 438,
                      '/en/comps/9/1997-1998/schedule/1997-1998-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 443,
                      '/en/comps/9/1996-1997/schedule/1996-1997-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 452,
                      '/en/comps/9/1995-1996/schedule/1995-1996-Premier-League-Stats-Premier-League-Scores-and-Fixtures': 450}

# =========== CSV File Writing ===========
# Create a CSV file for writing if not already one
if not os.path.isfile('match_report_data.csv'):
    with open('match_report_data.csv', 'w', newline='') as csv_file:
            header = ["Date", "Venue", "Attendance", "Refree", "Home Team", "Home Goals", "Home Formation", "Home Possession %", "Home Passing Accuracy", "Home Shots On", 
              "Home Saves", "Home Fouls", "Home Corners", "Home Crosses", "Home Touches", "Home Intercepts", "Home Aerials Won", "Home Clearances", "Home Offsides", 
              "Home Goal Kicks", "Home Throw Ins", "Home Long Balls", "Away Team", "Away Goals", "Away Formation", "Away Possession %", "Away Passing Accuracy", 
              "Away Shots On", "Away Saves", "Away Fouls", "Away Corners", "Away Crosses", "Away Touches", "Away Intercepts", "Away Aerials Won", "Away Clearances", 
              "Away Offsides", "Away Goal Kicks", "Away Throw Ins", "Away Long Balls"]
            
            # Write header row
            writer = csv.writer(csv_file)
            writer.writerow(header)

# Open CSV file for writing data
with open('match_report_data.csv', 'a', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
        
    # Create and write to text file with all match links
    if not os.path.isfile(LINKS_PATH):
            print("SAVING MATCH LINKS TO FILE...", end='')
            create_file(LINKS_PATH)
            create_file('error_links.txt')
            # Get all season links from constant var
            links = list(MATCHES_PER_SEASON.keys())
            print("NUMBER OF SEASONS: ", len(links))
            # Iterate through each season link getting matches from the season
            for season in links:
                    print("SEASON: ", season)
                    # Extract matches, check if number of matches is correct, if not rerun search
                    # From season links, get all the matches
                    num_of_matches = get_matches(URL, season) 
                    print("FOUND ", len(num_of_matches), " MATCHES")
                    # Once all matches fonud, write to the text file
                    append_links_to_file(LINKS_PATH, num_of_matches)
                    # Adding artificial delay so it does not seem like scraping activity
                    time.sleep(2)

            print("TOTAL NUMBER OF MATCHES: ", len(read_links_from_file(LINKS_PATH)))
            print("DONE")
            time.sleep(5)
        
    print("LOADING MATCH LINKS FROM FILE... ", end='')
    links = read_links_from_file(LINKS_PATH)
    print("DONE")

    print("STARTING TO WRITE DATA TO CSV...")
    # Write data to CSV
    error_links = read_links_from_file('error_links.txt')
    error_count = 0

    # If there is no error log file, create one
    if not os.path.isfile('error_log.txt'):
            create_file('error_log.txt')
            print("ERROR LOG FILE CREATED.")

    for i in links:
            try:
                    # Get data from match report using home link and extension
                    data = (get_match_report(URL + i))
                    print("(", data[0], ")-", data[1], ": ", data[4], " vs ", data[22], "... ", end='')
                    # If there is data, write it down
                    writer.writerow(data)
                    # Remove the written down link from the list
                    print("RECORDED MATCH... ", end='')
                    links.remove(i)
                    print("REMOVED LINK... ", end='')
                    write_links_to_file(LINKS_PATH, links)
                    print("SAVED FILE.")
            except Exception as e:
                    # Increment to count # of errors
                    error_count+=1
                    # Print error link and error number
                    print(str(error_count), ". ", f"ERROR PROCESSING LINK: {i}")
                    # PRINT ERROR MESSAGE
                    print(e)
                    with open('error_log.txt', 'a') as file:  
                            file.write(str(error_count), ". ", f"ERROR PROCESSING LINK: {i}\n", e)
                    # Remove error from link list and add to error list
                    links.remove(i)
                    error_links.append(i)
                    # Save both new lists back to file
                    print("SAVING MATCH LINKS TO FILE...", end='')
                    write_links_to_file(LINKS_PATH, links)
                    write_links_to_file('error_links.txt', error_links)
                    print("DONE")
            # Adding artificial delay so it does not seem like scraping activity
            time.sleep(2)
            
    print("Match information written to CSV file.")