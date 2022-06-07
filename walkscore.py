import requests
import csv
import urllib.parse


API_KEY = "5ee17e21890232c74c619778c75d7343"

class Spot:
    def __init__(self, spot_raw_data):
        """spot_raw_data is a list, let's make it nice ojbect"""
        self.name = spot_raw_data[0]
        self.address = f"{spot_raw_data[1]} {spot_raw_data[2]} {spot_raw_data[3]}"
        self.lat = f'{spot_raw_data[4]}'
        self.lon = f'{spot_raw_data[5]}'
        self.walk_score_points = None # will be set later
        self.walk_score_text = None # will be set later


def get_spots():
    spots_file = open("spots.csv")
    spots = list(csv.reader(spots_file))
    spots = [Spot(spot) for spot in spots]

    return spots


def get_walk_score_api(spot):
    """ spot should have address, lat, lon"""
    url_base = "https://api.walkscore.com/score?format=json"
    address_param = "&address=" + urllib.parse.quote(spot.address.encode('utf8'))
    lat = "&lat=" + spot.lat
    lon = "&lon=" + spot.lon
    api_key_param = "&wsapikey=" + API_KEY
    url = url_base + address_param + lat + lon + api_key_param
    print(url)
    return url

spots = get_spots()
spots = spots[1:6] # Get first 5 spots


results = []
for spot in spots:
    api_url = get_walk_score_api(spot)
    result = requests.get(api_url).json()
    spot.walk_score_points = result['walkscore']
    spot.walk_score_text = result['description']


# Print spots and walk 
for spot in spots:
    print(spot.name)
    print(f'{spot.walk_score_points} - {spot.walk_score_text}')
    print("\n")



