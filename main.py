# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from read_neighbourhoods import NeighbourhoodTaxiData
import read_taxidata
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Starting first leafmap test...')
    td = read_taxidata.TaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
    here_files = td.get_date_files(2021, 3)
    print(here_files)
    td.load_add_available(here_files)
    print('Minimum time available:')
    print(td.get_minimum_available_pickup_time())
    print('Maximum time available:')
    print(td.get_maximum_available_pickup_time())
    ntd = NeighbourhoodTaxiData('/home/benjamin-elias/PycharmProjects/Proseminar '
                                'Jupyter-Leafmap/nyc-neighborhoods.geo.json')
    print(ntd.central_points())
    ntd.to_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/taxi_zones.geo.json')
    pass


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
