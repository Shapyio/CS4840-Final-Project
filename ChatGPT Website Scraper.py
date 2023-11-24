import requests
from bs4 import BeautifulSoup
import csv

url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"
headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the table containing match information
    table = soup.find('table', {'id': 'sched_2023-2024_9_1'})
    
    if table:
        # Open a CSV file for writing
        with open('premier_league_matches.csv', 'w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            
            # Write header row
            header = [th.text.strip() for th in table.select('thead th')]
            writer.writerow(header)
            
            # Iterate through rows
            for row in table.select('tbody tr'):
                # Exclude matches that have not taken place yet
                if 'future' not in row.get('class', []):
                    data = [td.text.strip() for td in row.find_all(['td', 'th'])]
                    
                    # Extract the Match Report link
                    match_report_link = row.find('td', {'data-stat': 'match_report'}).find('a')['href']
                    
                    # Open the Match Report link and scrape information
                    match_report_response = requests.get(match_report_link, headers=headers)
                    
                    if match_report_response.status_code == 200:
                        match_report_soup = BeautifulSoup(match_report_response.text, 'html.parser')
                        
                        # Here, you can add code to extract information from the Match Report page
                        # Modify the code below based on the structure of the Match Report page
                        
                        # Example: Extracting the match summary
                        match_summary = match_report_soup.find('div', {'class': 'match_summary'}).text.strip()
                        
                        # Append the match summary to the data list
                        data.append(match_summary)
                        
                        # Write the data to the CSV file
                        writer.writerow(data)
                    else:
                        print(f"Failed to retrieve Match Report page. Status code: {match_report_response.status_code}")
                    
        print("Completed writing to CSV file.")
    else:
        print("Table with ID 'sched_2023-2024_9_1' not found.")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")

