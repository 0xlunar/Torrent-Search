import os, json, sys, subprocess
from prettytable import PrettyTable

def select(choices, *keys):
    x = PrettyTable()
    x.field_names = ["#"] + list(keys)
    x.align[x.field_names[1]] = "l"
    for i, choice in enumerate(choices):
        x.add_row([i] + value_to_list(choice, *keys))
    print(x)
    print("[CTRL+C] to exit")
    print("\nSelect an option")
    while True:
        try:
            selected = int(input("\n> "))
            if selected >= 0 and selected < len(choices):
                return choices[selected]
        except KeyboardInterrupt:
            print("\nExiting...")
            sys.exit()
        except:
            print("Invalid selection.")

def value_to_list(dictionary, *keys):
    return [f"{dictionary[key]}" for key in keys]

def create_magnet_uri(hash, slug):
    with open(f"{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}/trackers.json", "r") as f:
        trackers = json.load(f)
    magnet = f"magnet:?xt=urn:btih:{hash}&dn={slug}" + "".join(f"&tr={tracker}" for tracker in trackers)
    open_magnet(magnet)
    
def open_magnet(magnet): # source: https://stackoverflow.com/a/47526812
    """Open magnet according to os."""
    print("Opening Magnet URI...")
    if sys.platform.startswith('linux'):
        subprocess.Popen(['xdg-open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif sys.platform.startswith('win32'):
        os.startfile(magnet)
    elif sys.platform.startswith('cygwin'):
        os.startfile(magnet)
    elif sys.platform.startswith('darwin'):
        subprocess.Popen(['open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        subprocess.Popen(['xdg-open', magnet],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

