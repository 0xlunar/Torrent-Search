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
        r = s.get(f"https://eztv.re/search/{query}", headers=headers)
        if r.status_code == 200:
            soup = bs(r.text, "html.parser")
            results = soup.find_all("table")[5].find_all("tr")
            headers = [ re.sub(r'[^A-Za-z0-9 ]+', '', el.text) for el in results[1].find_all("td")]
            headers.pop(0)
            results.pop(0)
            results.pop(0)
            if len(results) == 0:
                print("No results found.")
                return
            else:
                results = table_to_dict(results, headers)
                print(headers)
                headers.pop(1)
                selected = helpers.select(results, *tuple(headers))
                helpers.open_magnet(selected['magnet'])
    except Exception as e:
        print(e)
    
        
def table_to_dict(table, headers):
    results = []
    for row in table:
        d = {headers[i]: re.sub(r'[^A-Za-z0-9 ]+', '', el.text) for i, el in enumerate(row.find_all("td")[1:]) }
        d["magnet"] = row.find_all("a", { "class":"magnet" }, href=True)[0]["href"]
        del d["Dload"]
        results.append(d)
    return results