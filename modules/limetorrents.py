import requests, re
from modules import helpers
from bs4 import BeautifulSoup as bs

def search(query):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-language": "en-US,en;q=0.9,en-AU;q=0.8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36"
    }
    try:
        s = requests.session()
        r = s.get(f"https://www.limetorrents.lol/search/all/{query}", headers=headers)
        if r.status_code == 200:
            soup = bs(r.text, "html.parser")
            results = soup.find("table", { "class": "table2" }).find_all("tr")
            headers = [ re.sub(r'[^A-Za-z0-9 ]+', '', el.text) for el in results[0].find_all("th")]
            headers.pop()
            if len(results) <= 1:
                print("No results found.")
                return
            else:
                results = table_to_dict(results[1:], headers)
                selected = helpers.select(results, *tuple(headers))
                magnet = fetch_magnet_hash(selected["url"], s)
                helpers.create_magnet_uri(magnet, selected[headers[0]])
    except Exception as e:
        print(e)
        
def fetch_magnet_hash(url, session):
    r = session.get(url)
    if r.status_code == 200:
        soup = bs(r.text, "html.parser")
        return soup.find_all("tr")[0].find_all("td")[1].text
    
        
def table_to_dict(table, headers):
    results = []
    print(headers)
    for row in table:
        d = {headers[i]: el.text for i, el in enumerate(row.find_all("td")[:-1])}
        d["url"] = "https://www.limetorrents.lol" + row.find_all("a", href=True)[1]["href"]
        results.append(d)
    return results