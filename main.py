# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from datetime import datetime
import read_taxidata

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('Starting first leafmap test...')
    td = read_taxidata.TaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
    td.load_available(td.get_date_files(2021, 7))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
