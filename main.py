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
    tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
    print('Printing neighbourhood Williamsburg:')
    print(tz.get_from_neighbourhood_name('Williamsburg (North Side)'))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
