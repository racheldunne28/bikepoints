import folium

from get_data import (get_bikepoints_json, get_bikepoints_locations, get_london_las, 
                      get_london_adult_obesity, get_joined_obesity_geog_data)



def gen_map(locations, ldn_geog, ldn_obesity):
    m = folium.Map(location=(51.51, 0.13))
    folium.Choropleth(geo_data=ldn_geog, name='choropleth', data=ldn_obesity, columns=['LAD22CD', 'Value'], key_on='feature.properties.LAD22CD',
                      fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Percentage of adults living with obesity",).add_to(m)
    for l in locations.keys():
        folium.CircleMarker(location=[locations[l]['lat'], locations[l]['lon']], radius=4, tooltip=l, fill_color="blue", fill_opacity=0.8, color="black", weight=1).add_to(m)
    folium.LayerControl().add_to(m)
    m.save('outputs/map.html')
    return m


if __name__ == '__main__':
    bikepoints_json = get_bikepoints_json()
    locations = get_bikepoints_locations(bikepoints_json)
    ldn_geog = get_london_las()
    ldn_obesity = get_london_adult_obesity()
    obesity_geog = get_joined_obesity_geog_data(ldn_obesity, ldn_geog)
    gen_map(locations, ldn_geog, ldn_obesity)