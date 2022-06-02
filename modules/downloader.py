import qbittorrentapi, os, json, time
from qbittorrentapi import Client

client = Client(host='localhost:9998', username='admin', password='adminadmin')

try:
    client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

def endswith_list(item, list):
    for i in list:
        if item.endswith(i):
            return True
    return False

def disable_bad_extensions(hash):
    with open(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/approvedExtensions.json", "r") as f:
        extensions = json.load(f)
    removed = []
    for torrent in client.torrents_files(hash):
        if not endswith_list(torrent["name"], extensions):
            client.torrents_file_priority(hash, torrent['id'], 0)
            removed.append(torrent['name'])
    return removed

def download_torrent(magnet):
    try:
        client.torrents_add(magnet)
        hash = magnet.split("&")[0].split("btih:")[1]
        print("Started Torrent, waiting for initialisation...")
        while client.torrents_info(hashes=hash)[0]['state'] != "stalledDL":
            time.sleep(1)
        removed = disable_bad_extensions(hash)
        print(f"Removed {len(removed)} files with bad extensions from torrent")
    except Exception as e:
        print(e)