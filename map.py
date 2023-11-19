import folium

from get_data import (get_bikepoints_json, get_bikepoints_locations, get_london_las, 
                      get_london_adult_obesity, get_joined_obesity_geog_data, get_pop)



def gen_map(locations, ldn_geog, ldn_obesity, pop):
    m = folium.Map(location=(51.51, 0.13))
    cp = folium.Choropleth(geo_data=ldn_geog, name='choropleth', data=ldn_obesity, columns=['LAD22CD', 'Value'], key_on='feature.properties.LAD22CD',
                      fill_color="YlGnBu", fill_opacity=0.7, line_opacity=0.2, legend_name="Percentage of adults living with obesity",).add_to(m)
    ldn_obesity_indexed = ldn_obesity.set_index('LAD22CD')
    for s in cp.geojson.data['features']:
        s['properties']['obesity'] = round(ldn_obesity_indexed.loc[s['properties']['LAD22CD'], 'Value'], 2)
        s['properties']['pop'] = f"{int(pop.loc[s['properties']['LAD22CD'], 'Observation']):,}"   
    folium.GeoJsonTooltip(['LAD22NM', 'obesity', 'pop'], aliases=['Local Authority', r'% adults overweight or obese', 'Population']).add_to(cp.geojson)
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
    pop = get_pop()
    gen_map(locations, ldn_geog, ldn_obesity, pop)