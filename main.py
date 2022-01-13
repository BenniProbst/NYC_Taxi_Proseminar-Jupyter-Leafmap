# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from read_neighbourhoods import NeighbourhoodTaxiData
import read_taxidata
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ntd = NeighbourhoodTaxiData('/home/benjamin-elias/PycharmProjects/Proseminar '
                                'Jupyter-Leafmap/nyc-neighborhoods.geo.json')
    print(ntd.central_points())
    ntd.to_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/taxi_zones.geo.json')
    pass


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
