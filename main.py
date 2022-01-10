# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import read_taxizone
import read_taxidata
from leafmap import leafmap

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Starting first leafmap test...')
    tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
    print(tz.get_location(29))
    td = read_taxidata.TaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
    td.load_add_available(td.get_date_files(2021, 3))
    print(td.get_minimum_available_pickup_time())
    print(td.get_maximum_available_pickup_time())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
