import os

import dotenv
import requests
from requests.auth import HTTPBasicAuth

dotenv.load_dotenv()

app_key = os.getenv('APP_KEY') # Primary key or secondary key from your TFL User profile, stored in a .env file in this folder


def get_bikepoints_json():
    '''
    Get basic bikepoints data from TFL bikepoints API
    '''
    auth = HTTPBasicAuth('app_key', app_key)
    url = "https://api.tfl.gov.uk/BikePoint/"
    hdr ={'Cache-Control': 'no-cache'}
    response = requests.get(url, headers=hdr, auth=auth)
    return response.json()


def get_bikepoints_locations(bikepoints_json):
    '''
    Get latitude and longitude data from TFL bikepoints API JSON reponse
    '''
    return {entry['commonName']: {'lat': entry['lat'], 'lon': entry['lon']} for entry in bikepoints_json}


if __name__ == "__main__":
    bikepoints_json = get_bikepoints_json()
    geog_data = get_bikepoints_locations(bikepoints_json)
    print(geog_data)
