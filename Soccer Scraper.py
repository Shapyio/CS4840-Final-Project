import pandas as pd
from urllib.request import Request, urlopen

url = "https://fbref.com/en/comps/9/schedule/Premier-League-Scores-and-Fixtures"

request = Request(url)
request.add_header("user-agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.60")
page = urlopen(request)
html_content = page.read()

table = pd.read_html(html_content)

for x in table:
        print(x, "\n")