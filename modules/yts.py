import requests
from modules import helpers

def search(query):
    try:
        r = requests.get(f"https://yts.mx/api/v2/list_movies.json?query_term={query}&order_by=asc&sort_by=seeds&with_rt_ratings=true")
        if r.status_code == 200:
            if r.json()["data"]["movie_count"] == 0:
                print("No results found.")
                return
            else:
                choice = helpers.select(r.json()["data"]["movies"], "title", "year", "rating", "runtime")
                quality = helpers.select(choice["torrents"], "quality", "size", "type", "seeds", "peers")
                return helpers.create_magnet_uri(quality["hash"], choice["slug"])
    except Exception as e:
        print(e)