# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from get_drives_by_time import TaxiTime
from datetime import datetime, time
import leafmap
import random
from typing import List
import read_taxizone
import get_drives_by_time
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tt = TaxiTime('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/', '/home/benjamin-elias/PycharmProjects'
                                                                           '/Proseminar '
                                                                           'Jupyter-Leafmap/nyc-neighborhoods.geojson')
    # standard range load with hours and minutes
    start = datetime(2020, 3, 10, 1, 1)
    end = datetime(2020, 3, 12, 1, 2)
    tt.load_range(start, end)
    print('Analyze time between 10-02-2020 01:01 and 25-05-2020 01:02')
    print(tt.min_is_loaded)
    print(tt.max_is_loaded)

    print('Filters:')
    # limit to main work time
    tt.daytime_filter(time(8), time(17))
    # limit trip distance
    tt.value_filter(0, 20)
    # limit Pickup to Bloomingdale
    tt.flag_filter('Bloomingdale/Upper West Side North', method=get_drives_by_time.PICKUP_LOCATION,
                   zone_checker=read_taxizone.ZONE)

    # taxi drive connections and neighborhood central points on map
    con = tt.interconnections('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/rides.geojson')
    points = tt.zone_neighborhoods.neighbourhood_points(
        '/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/neighborhood_centers.geojson')

    # center to New York at 41 degrees north and 74 degrees west
    m = leafmap.Map(google_map="HYBRID", center=[40.702557, -74.012318], zoom=12, height="600px", width="1200px",
                    max_zoom="20")  # center=[lat, lon]
    # show
    print('Showing current layer names before adding neighbourhoods:')
    print(m.get_layer_names())
    print('Random color hex list:')
    r = lambda: random.randint(0, 255)
    color_list: List[str] = []
    for i in range(0, len(tt.zone_neighborhoods.taxi_zone.zones)):
        color_list.append('#%02X%02X%02X' % (r(), r(), r()))

    print('Add geojson layer neighbourhoods, color is sorted by geojson polygon order:')
    m.add_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/nyc-neighborhoods.geojson',
                  layer_name='neighbourhoods', style={}, hover_style={}, style_callback=None, fill_colors=color_list,
                  info_mode='on_hover')
    m.layer_opacity('neighbourhoods', 0.5)
    color_list: List[str] = []
    for i in range(0, len(tt.zone_neighborhoods.feature_collection.features)):
        color_list.append('#%02X%02X%02X' % (r(), r(), r()))

    print('Add geojson layer taxi_zones, color is sorted by geojson polygon order:')
    m.add_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/taxi_zones.geojson',
                  layer_name='taxi_zones', style={}, hover_style={}, style_callback=None, fill_colors=color_list,
                  info_mode='on_hover')
    m.layer_opacity('taxi_zones', 0.3)
    print(m.get_layer_names())

    print('Add csv layer heatmap for pickups:')
    from con_geojson_to_heatmap import Heatmapper

    h = Heatmapper('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/rides.geojson',
                   '/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/heat_of_april.csv')
    # there is a bug in heatmap swapping longitude and latitude, changing the csv will else continue the bug
    m.add_heatmap('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/heat_of_april.csv',
                  latitude='longitude', longitude='latitude', value='heat_property_val', name='Heat map', radius=40)
    m.layer_opacity('Heat map', 0.9)
    print(m.get_layer_names())

    print('Add geojson layer rides:')
    m.add_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/rides.geojson', layer_name='rides',
                  style={}, hover_style={}, style_callback=None, fill_colors=color_list, info_mode='on_hover')
    m.layer_opacity('rides', 0.1)
    print(m.get_layer_names())

    print('Add geojson layer neighborhood_centers:')
    m.add_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/neighborhood_centers.geojson',
                  layer_name='neighborhood_centers', style={}, hover_style={}, style_callback=None,
                  fill_colors=color_list, info_mode='on_hover')
    m.layer_opacity('neighborhood_centers', 0.1)
    print(m.get_layer_names())
    m

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
