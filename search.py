import argparse
from modules import yts, leetx

parser = argparse.ArgumentParser(description="Search for a movie on the internet.")
parser.add_argument("--query", "-q", help="The movie to search for. (Supports IMDB Id's)", nargs='+', required=True)
parser.add_argument("--provider", "-p", help="The provider to search for the movie on. (Default: YTS)", default="yts", choices=["yts", "1337x"])

args = parser.parse_args()

if (args.query):
    if args.provider == "1337x":
        leetx.search(args.query)
    else:
        yts.search(args.query)