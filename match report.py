import requests
from bs4 import BeautifulSoup
import csv

match_report_url = "https://fbref.com/en/matches/3a6836b4/Burnley-Manchester-City-August-11-2023-Premier-League"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}

response = requests.get(match_report_url, headers=headers)

if response.status_code == 200:
    match_report_soup = BeautifulSoup(response.text, 'html.parser')
    
    # Print the HTML content of the 'scorebox' div to inspect its structure
    scorebox_div = match_report_soup.find('div', {'class': 'scorebox'})
    print("Scorebox HTML content:")
    print(scorebox_div.prettify() if scorebox_div else "Scorebox div not found")
    
    # Extracting information from the Match Report page
    date_element = match_report_soup.find('div', {'class': 'scorebox'}).find('div', {'itemprop': 'startDate'})
    date = date_element.text.strip() if date_element else "Date not found"
    
    # Continue with other extractions...
    
    # Open a CSV file for writing
    with open('match_report_info.csv', 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        
        # Write header row
        header = ["Date", "Venue", "Attendance", "Home Team", "Away Team", "Home Manager", "Away Manager", "Home Captain", "Away Captain", "Other Column Headers..."]
        writer.writerow(header)
        
        # Write data to CSV
        data = [date, "Other Data..."]
        writer.writerow(data)
        
    print("Match information written to CSV file.")
else:
    print(f"Failed to retrieve Match Report page. Status code: {response.status_code}")
