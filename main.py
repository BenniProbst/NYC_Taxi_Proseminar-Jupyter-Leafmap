# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from get_drives_by_time import TaxiTime
from con_geojson_to_heatmap import Heatmapper
from datetime import datetime
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    h = Heatmapper('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/rides.geojson',
                   '/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/heat_of_april.csv')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
