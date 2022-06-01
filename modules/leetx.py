import requests
from modules import helpers
from bs4 import BeautifulSoup as bs



def search(query):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,en-AU;q=0.8",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "referer": "https://1337x.to/search/Spiderman/1/",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.62 Safari/537.36"
    }
    try:
        s = requests.session()
        r = s.get(f"https://1337x.to/search/{query}/1/", headers=headers)
        r = s.get(f"https://1337x.to/sort-search/{query}/seeders/desc/1/", headers=headers) # for some reason this doesn't work without the above request, just returns nothing
        if r.status_code == 200:
            soup = bs(r.text, "html.parser")
            results = soup.find("tbody").find_all("tr")
            headers = soup.find("thead").find_all("tr")
            headers = [el.text for el in headers[0].find_all("th")]
            if len(results) == 0:
                print("No results found.")
                return
            else:
                results = table_to_dict(results, headers)
                selected = helpers.select(results, *tuple(headers))
                magnet = fetch_magnet_hash(results[0]["url"], s)
                helpers.create_magnet_uri(magnet, selected[headers[0]])
    except Exception as e:
        print(e)
        
def fetch_magnet_hash(url, session):
    r = session.get(url)
    soup = bs(r.text, "html.parser")
    return soup.find("div", {"class": "infohash-box"}).find("span").text
    
        
def table_to_dict(table, headers):
    results = []
    for row in table:
        d = {headers[i]: el.text for i, el in enumerate(row.find_all("td"))}
        d["url"] = "https://1337x.to" + row.find_all("a", href=True)[1]["href"]
        results.append(d)
    return results