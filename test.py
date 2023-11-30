import requests

URL = "https://fbref.com" # Base website link
HEADER = [{"User-Agent": "Mozilla/5.0 (Windows NT 10.1; Win64; x64; en-US) AppleWebKit/603.26 (KHTML, like Gecko) Chrome/48.0.1177.392 Safari/535.9 Edge/16.19452"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0 [ip:165.1.169.144]"},
        {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 10.4; Win64; x64) AppleWebKit/603.28 (KHTML, like Gecko) Chrome/52.0.3838.306 Safari/601.0 Edge/14.17115"},
        {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 10.1; x64; en-US) AppleWebKit/537.45 (KHTML, like Gecko) Chrome/50.0.1744.251 Safari/602.2 Edge/14.38768"}]

for head in HEADER:
    response = requests.get(URL + "/en/comps/9/schedule/Premier-League-Scores-and-Fixtures", headers=head)

    print("RESPONSE STATUS CODE: ", response.status_code)
