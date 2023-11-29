import match_report

URL = "https://fbref.com/en/matches/4b9f3f25/Manchester-United-Luton-Town-November-11-2023-Premier-League" # Base website link
HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60",
          'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0 [ip:165.1.169.144]"}

print(match_report.get_match_report(URL, HEADER))