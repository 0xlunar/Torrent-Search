# Torrent-Search
Search for torrents via command-line and open magnet uri's

This project was purely made out of boredom and not much else, as long as the code does it's job that's all that matters for this project
If you wish to contribute go for it, but it was only intended to be for my own personal home use.

## Requirements
qBitTorrent (with WebUI enabled)

## Install

Clone Repo

pip install -r ./requirements.txt

Add directory to PATH

Update torrent-search.cmd with the directory to the search.py file

example (python "C:\PATH\TO\REPO\search.py" %*)

Enable WebUI in qBittorrent: Tools -> Preferences -> Web UI

Set the Port to 9998, and leave everything else on default

## Usage

torrent-search -h

torrent-search -q Query Goes Here

torrent-search -q Query Goes Here -p Provider 

## Providers

- YTS
- 1337x
- LimeTorrents
- EzTv 
