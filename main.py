# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import read_taxizone
import read_taxidata
import random
from typing import List
from leafmap import leafmap

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Starting first leafmap test...')
    tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
    print(tz.get_location(29))
    print('Random color hex:')
    r = lambda: random.randint(0, 255)
    print('#%02X%02X%02X' % (r(), r(), r()))
    color_list: List[str] = []
    for i in range(0, len(tz.zones)):
        color_list.append('#%02X%02X%02X' % (r(), r(), r()))
    td = read_taxidata.TaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
    td.load_add_available(td.get_date_files(2021, 3))
    print(td.get_minimum_available_pickup_time())
    print(td.get_maximum_available_pickup_time())

    # m = leafmap.Map(google_map="HYBRID", center=[40.702557, -74.012318], zoom=12, height="600px", width="1200px",
    #                 max_zoom="20")  # center=[lat, lon]
    # show
    # print('Showing current layer names before adding neighbourhoods:')
    # print(m.get_layer_names())
    # print('Add geojson layer neighbourhoods:')
    # m.add_geojson('/home/benjamin-elias/Proseminar/Jupyterlab/nyc_neighborhoods.geo.json', layer_name='neighbourhoods',
    #               style={}, hover_style={}, style_callback=None, fill_colors=['red'], info_mode='on_hover')
    # print(m.get_layer_names())
    # m

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
