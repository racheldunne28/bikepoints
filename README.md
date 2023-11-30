# bikepoints

## About the project

One of the Government’s key objectives is to improve public health. A senior decision maker wants to encourage people to exercise, and is interested in increasing the number of BikePoints (i.e cycle docking stations) in London’s bike sharing scheme. This code generates a map to provide insight for deciding where to locate new BikePoints.

## Prerequisites
Before you continue, ensure you have met the following requirements:
- Python3 installed locally
- (TFL API account)[https://api-portal.tfl.gov.uk/profile] set up to get an app_key

## How to run the code
1) Clone this repository locally
1) Create a file called .env in the repo folder and save your TFL API primary or secondary key as `APP_KEY = XXXXXXX`
1) Set up your preferred virtual environment and install the requirements in requirements.txt using `pip install -r requirements.txt`
1) In the terminal, run `python3 map.py`. This will generate a map and save it as an html in the outputs folder. 

## How to use the output
The output map shows circle markers where each of the bike points in London is located. You can hover over them to see the name of the bike point. The heatmap shows the percentage of adults 18 or over classified as overweight or obese by local authority. You can hover over each local authority to get more information on the name, the value for the percentage of adults 18 or over classified as overweight or obese, the total population, and the percentage of lower-level super output areas (LSOAs) in that local authority that are in the 10% most health deprived in England. 

## Sources
- Current bike point locations (TFL API)[https://api-portal.tfl.gov.uk/api-details#api=BikePoint&operation=BikePoint_GetAll]
- Percentage of adults classified as overweight or obese by local authority 2021/22 (Office for Health Improvement & Disparities fingertips API)[https://fingertips.phe.org.uk/profile/national-child-measurement-programme/data#page/9/gid/1938133368/pat/6/par/E12000007/ati/501/cid/4/tbm/1/page-options/car-do-0_car-ao-0]
- Total population by local authority 2021 (ONS population data by age and local authority)[https://www.ons.gov.uk/datasets/TS007/editions/2021/versions/3#get-data]
- Health deprivation by local authority 2019 (English indices of deprivation, local authority summary)[https://www.gov.uk/government/statistics/english-indices-of-deprivation-2019]
- Local authority boundaries 2022 (ONS geography portal)[https://geoportal.statistics.gov.uk/datasets/ons::local-authority-districts-december-2022-boundaries-uk-buc-2/explore]
