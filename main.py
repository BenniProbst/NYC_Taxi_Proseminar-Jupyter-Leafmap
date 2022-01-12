# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from read_neighbourhoods import NeighbourhoodTaxiData

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    ntd = NeighbourhoodTaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/nyc-neighborhoods.geo.json')
    print(ntd.central_points())
    ntd.to_geojson('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_zones.geo.json')
    pass


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
