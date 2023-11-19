import os

import dotenv
from fingertips_py import retrieve_data
import geopandas
import requests
from requests.auth import HTTPBasicAuth

dotenv.load_dotenv()

app_key = os.getenv('APP_KEY') # Primary key or secondary key from your TFL User profile, stored in a .env file in this folder

latest_obesity_time_period = '2021/22'

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


def get_london_las():
    geog = geopandas.read_file('data/Local_Authority_Districts_December_2022_UK_BUC_V2_-5963189729337928393.geojson')
    london_geog = geog[geog['LAD22CD'].str.contains('E09')]
    return london_geog


def get_london_adult_obesity():
    obesity = retrieve_data.get_data_by_indicator_ids(['93088'], 301)
    obesity = obesity[obesity['Age'] == '18+ yrs']
    obesity = obesity[obesity['Sex'] == 'Persons']
    obesity_london = obesity[obesity['Area Code'].str.contains('E09')]
    obesity_latest = obesity_london[obesity_london['Time period'] == latest_obesity_time_period]
    obesity_latest['Value'] = obesity_latest['Value'].astype(float)
    return obesity_latest


def get_joined_obesity_geog_data(ldn_obesity, ldn_geog):
    ldn_obesity.rename({'Area Code': 'LAD22CD'}, axis=1, inplace=True)
    ldn_obesity['LAD22CD'] = ldn_obesity['LAD22CD'].astype(str)
    ldn_geog['LAD22CD'] = ldn_geog['LAD22CD'].astype(str)
    joined = ldn_obesity.merge(ldn_geog, on='LAD22CD')
    return joined


if __name__ == "__main__":
    bikepoints_json = get_bikepoints_json()
    geog_data = get_bikepoints_locations(bikepoints_json)
    ldn_obesity = get_london_adult_obesity()
    ldn_geog = get_london_las()
    joined = get_joined_obesity_geog_data(ldn_obesity, ldn_geog)
    print(joined)
