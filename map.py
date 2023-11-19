import folium

from get_data import get_bikepoints_json, get_bikepoints_locations



if __name__ == '__main__':
    bikepoints_json = get_bikepoints_json()
    locations = get_bikepoints_locations(bikepoints_json)
    m = folium.Map(location=(51.51, 0.13))
    for l in locations.keys():
        folium.Marker(
                location=[locations[l]['lat'], locations[l]['lon']],
                tooltip=l,
                icon=folium.Icon(icon='person-biking', prefix='fa'),
            ).add_to(m)
    m.save('outputs/map.html')