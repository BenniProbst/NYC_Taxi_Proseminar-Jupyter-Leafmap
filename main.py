# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from read_neighbourhoods import NeighbourhoodTaxiData
import read_taxidata
import leafmap
from typing import List
import random
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    nd = NeighbourhoodTaxiData('/home/benjamin-elias/PycharmProjects/Proseminar '
                                'Jupyter-Leafmap/nyc-neighborhoods.geo.json')
    print(nd.central_points())
    nd.to_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/taxi_zones.geo.json')
    # center to New York at 41 degrees north and 74 degrees west
    m = leafmap.Map(google_map="HYBRID", center=[40.702557, -74.012318], zoom=12, height="600px", width="1200px",
                    max_zoom="20")  # center=[lat, lon]
    # show
    print('Showing current layer names before adding neighbourhoods:')
    print(m.get_layer_names())
    print('Random color hex list:')
    r = lambda: random.randint(0, 255)
    color_list: List[str] = []
    for i in range(0, len(nd.input_geojson['features'])):
        color_list.append('#%02X%02X%02X' % (r(), r(), r()))
    print('Add geojson layer neighbourhoods, color is sorted by geojson polygon order:')
    m.add_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/taxi_zones.geo.json',
                  layer_name='taxi_zones', style={}, hover_style={}, style_callback=None, fill_colors=color_list,
                  info_mode='on_hover')
    m.layer_opacity('taxi_zones', 0.8)
    print(m.get_layer_names())
    m
    pass


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
