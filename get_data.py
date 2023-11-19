import os

import dotenv
import geopandas
import pandas as pd
import requests
from fingertips_py import retrieve_data
from requests.auth import HTTPBasicAuth

dotenv.load_dotenv()

app_key = os.getenv(
    "APP_KEY"
)  # Primary key or secondary key from your TFL User profile,
# stored in a .env file in this folder

latest_obesity_time_period = "2021/22"


def get_bikepoints_json():
    """
    Get basic bikepoints data from TFL bikepoints API
    """
    auth = HTTPBasicAuth("app_key", app_key)
    url = "https://api.tfl.gov.uk/BikePoint/"
    hdr = {"Cache-Control": "no-cache"}
    response = requests.get(url, headers=hdr, auth=auth)
    return response.json()


def get_bikepoints_locations(bikepoints_json):
    """
    Get latitude and longitude data from TFL bikepoints API JSON reponse
    """
    return {
        entry["commonName"]: {"lat": entry["lat"], "lon": entry["lon"]}
        for entry in bikepoints_json
    }


def get_london_las():
    geog = geopandas.read_file(
        "data/Local_Authority_Districts_December_2022_" +
        "UK_BUC_V2_-5963189729337928393.geojson"
    )
    london_geog = geog[geog["LAD22CD"].str.contains("E09")]
    return london_geog


def get_london_adult_obesity():
    obesity = retrieve_data.get_data_by_indicator_ids(["93088"], 301)
    obesity = obesity[obesity["Age"] == "18+ yrs"]
    obesity = obesity[obesity["Sex"] == "Persons"]
    obesity_london = obesity[obesity["Area Code"].str.contains("E09")]
    obesity_latest = obesity_london[
        obesity_london["Time period"] == latest_obesity_time_period
    ]
    obesity_latest.loc[:, "Value"] = obesity_latest.loc[:, "Value"].astype(float)
    obesity_latest.rename({'Area Code': 'LAD22CD'}, axis=1, inplace=True)
    return obesity_latest


def get_pop():
    pop = pd.read_csv("data/TS007-2021-3.csv")
    total_pop = (
        pop[["Lower tier local authorities Code", "Observation"]]
        .groupby("Lower tier local authorities Code")
        .sum()
    )
    return total_pop


def get_deprivation():
    imd = pd.read_excel(
        "data/File_10_-_IoD2019_Local_Authority_" +
        "District_Summaries__lower-tier__.xlsx",
        sheet_name="Health",
    )
    imd.rename(
        {
            "Health Deprivation and Disability - Proportion " +
            "of LSOAs in most deprived 10% nationally ": "health_deprivation"
        },
        axis=1,
        inplace=True,
    )
    imd.set_index("Local Authority District code (2019)", inplace=True)
    return imd[["health_deprivation"]]


if __name__ == "__main__":
    bikepoints_json = get_bikepoints_json()
    geog_data = get_bikepoints_locations(bikepoints_json)
    ldn_obesity = get_london_adult_obesity()
    ldn_geog = get_london_las()
    pop = get_pop()
    imd = get_deprivation()
