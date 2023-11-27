import requests # Call HTML webstie using computer
from bs4 import BeautifulSoup # HTML parser
import csv # To output HTML to usable CSV format
import re # To manipulate strings

match_report_url = "https://fbref.com/en/matches/3a6836b4/Burnley-Manchester-City-August-11-2023-Premier-League"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0 [ip:165.1.169.144]"}

response = requests.get(match_report_url, headers=headers)

if response.status_code == 200:
    match_report_soup = BeautifulSoup(response.text, 'html.parser')
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
    venue_element = score_metabox_soup.find_all('div')[-2].find('small').find_next()
    venue = venue_element.text.strip() if venue_element else "Venue not found"

    # ATTENDANCE
    attendance_element = score_metabox_soup.find_all('div')[-3].find('small').find_next()
    attendance = attendance_element.text.strip() if attendance_element else "Attendance not found"

    # REFREE
    refree_element = score_metabox_soup.find_all('div')[-1].find('small').find_next().find('span')
    refree = refree_element.text.strip() if refree_element else "Refree not found"
    refree = refree.split(' (', 1)[0] # To remove '(Refree)' at end of text

    # =========== Home Team Info ===========

    # Home Team Name
    home_team_element = scorebox_soup.find_all('div', {'class' : 'media-item logo loader'})[0].find_next('a')
    home_team = home_team_element.text.strip() if home_team_element else "Home team name not found"

    # Home Expected Goals
    home_xg_element = scorebox_soup.find_all()[0].find('div', {'class' : 'score_xg'})
    home_xg = home_xg_element.text.strip() if home_xg_element else "Home xG not found"

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
    print("Home Fouls: ", home_fouls)

    # Home Corners
    home_corners_element = team_stats_extra_soup.find_all()[7]
    home_corners = home_corners_element.text.strip() if home_corners_element else "Home corners not found"
    print("Home Corners: ", home_corners)

    # Home Crosses
    home_crosses_element = team_stats_extra_soup.find_all()[10]
    home_crosses = home_crosses_element.text.strip() if home_crosses_element else "Home crosses not found"
    print("Home Crosses: ", home_crosses)

    # Home Touches
    home_touches_element = team_stats_extra_soup.find_all()[13]
    home_touches = home_touches_element.text.strip() if home_touches_element else "Home touches not found"
    print("Home Touches: ", home_touches)

    # Home Tackles
    home_tackles_element = team_stats_extra_soup.find_all()[20]
    home_tackles = home_tackles_element.text.strip() if home_tackles_element else "Home tackles not found"
    print("Home Tackles: ", home_tackles)

    # Home Interceptions
    home_interceptions_element = team_stats_extra_soup.find_all()[23]
    home_interceptions = home_interceptions_element.text.strip() if home_interceptions_element else "Home interceptions not found"
    print("Home Interceptions :", home_interceptions)

    # Home Aerials Won
    home_aerials_element = team_stats_extra_soup.find_all()[26]
    home_aerials = home_aerials_element.text.strip() if home_aerials_element else "Home aerials won not found"
    print("Home Aerials: ", home_aerials)

    # Home Clearances
    home_clearances_element = team_stats_extra_soup.find_all()[29]
    home_clearances = home_clearances_element.text.strip() if home_clearances_element else "Home clearances not found"
    print("Home Clearances: ", home_clearances)

    # Home Offsides
    home_offsides_element = team_stats_extra_soup.find_all()[36]
    home_offsides = home_offsides_element.text.strip() if home_offsides_element else "Home offsides not found"
    print("Home Offsides: ", home_offsides)

    # Home Goal Kicks
    home_gk_element = team_stats_extra_soup.find_all()[39]
    home_gk = home_gk_element.text.strip() if home_gk_element else "Home goal kicks not found"
    print("Home Goal Kicks: ", home_gk)

    # Home Throw Ins
    home_ti_element = team_stats_extra_soup.find_all()[42]
    home_ti = home_ti_element.text.strip() if home_ti_element else "Home throw ins won not found"
    print("Home Throw Ins: ", home_ti)

    # Home Long Balls
    home_lb_element = team_stats_extra_soup.find_all()[45]
    home_lb = home_lb_element.text.strip() if home_lb_element else "Home long balls not found"
    print("Home Long Balls: ", home_lb)

    # =========== Away Team Info ===========

    # Away Team Name
    away_team_element = scorebox_soup.find_all('div', {'class' : 'media-item logo loader'})[1].find_next('a')
    away_team = away_team_element.text.strip() if away_team_element else "Away team name not found"
    print("Away Name: ", away_team)

    # Away Expected Goals
    away_xg_element = scorebox_soup.find_all()[1].find('div', {'class' : 'score_xg'})
    away_xg = away_xg_element.text.strip() if away_xg_element else "Away xG not found"

    # Away Goals
    away_goals_element = scorebox_soup.find_all()[1].find('div', {'class' : 'score'})
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
    print("Away Fouls: ", away_fouls)

    # Away Corners
    away_corners_element = team_stats_extra_soup.find_all()[9]
    away_corners = away_corners_element.text.strip() if away_corners_element else "Away corners not found"
    print("Away Corners: ", away_corners)

    # Away Crosses
    away_crosses_element = team_stats_extra_soup.find_all()[12]
    away_crosses = away_crosses_element.text.strip() if away_crosses_element else "Away crosses not found"
    print("Away Crosses: ", away_crosses)

    # Away Touches
    away_touches_element = team_stats_extra_soup.find_all()[15]
    away_touches = away_touches_element.text.strip() if away_touches_element else "Away touches not found"
    print("Away Touches: ", away_touches)

    # Away Tackles
    away_tackles_element = team_stats_extra_soup.find_all()[22]
    away_tackles = away_tackles_element.text.strip() if away_tackles_element else "Away tackles not found"
    print("Away Tackles: ", away_tackles)

    # Away Interceptions
    away_interceptions_element = team_stats_extra_soup.find_all()[25]
    away_interceptions = away_interceptions_element.text.strip() if away_interceptions_element else "Away interceptions not found"
    print("Away Interceptions :", away_interceptions)

    # Away Aerials Won
    away_aerials_element = team_stats_extra_soup.find_all()[28]
    away_aerials = away_aerials_element.text.strip() if away_aerials_element else "Away aerials won not found"
    print("Away Aerials: ", away_aerials)

    # Away Clearances
    away_clearances_element = team_stats_extra_soup.find_all()[31]
    away_clearances = away_clearances_element.text.strip() if away_clearances_element else "Away clearances not found"
    print("Away Clearances: ", away_clearances)

    # Away Offsides
    away_offsides_element = team_stats_extra_soup.find_all()[38]
    away_offsides = away_offsides_element.text.strip() if away_offsides_element else "Away offsides not found"
    print("Away Offsides: ", away_offsides)

    # Away Goal Kicks
    away_gk_element = team_stats_extra_soup.find_all()[41]
    away_gk = away_gk_element.text.strip() if away_gk_element else "Away goal kicks not found"
    print("Away Goal Kicks: ", away_gk)

    # Away Throw Ins
    away_ti_element = team_stats_extra_soup.find_all()[44]
    away_ti = away_ti_element.text.strip() if away_ti_element else "Away throw ins won not found"
    print("Away Throw Ins: ", away_ti)

    # Away Long Balls
    away_lb_element = team_stats_extra_soup.find_all()[47]
    away_lb = away_lb_element.text.strip() if away_lb_element else "Away long balls not found"
    print("Away Long Balls: ", away_lb)

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
        
        # Write data to CSV
        data = [date, venue, attendance, refree, home_team, home_xg, home_goals, home_formation, home_possession, home_passing_accuracy, home_shots_on, home_saves, home_fouls,
                home_corners, home_crosses, home_touches, home_interceptions, home_aerials, home_clearances, home_offsides, home_gk, home_ti, home_lb, away_team, away_xg, 
                away_goals, away_formation, away_possession, away_passing_accuracy, away_shots_on, away_saves, away_fouls, away_corners, away_crosses, away_touches, 
                away_interceptions, away_aerials, away_clearances, away_offsides, away_gk, away_ti, away_lb]
        writer.writerow(data)
        
    print("Match information written to CSV file.")
else:
    print(f"Failed to retrieve Match Report page. Status code: {response.status_code}")
