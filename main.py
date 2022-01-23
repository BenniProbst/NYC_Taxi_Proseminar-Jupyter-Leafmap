# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from get_drives_by_time import TaxiTime
from datetime import datetime
import leafmap
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tt = TaxiTime('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/', '/home/benjamin-elias/PycharmProjects'
                                                                           '/Proseminar '
                                                                           'Jupyter-Leafmap/nyc-neighborhoods.geojson')
    # standard range load with hours and minutes
    start = datetime(2020, 3, 10, 1, 1)
    end = datetime(2020, 3, 12, 1, 2)
    tt.load_range(start, end)
    print('Analyze time between 10-02-2020 and 25-05-2020')
    print(tt.min_is_loaded)
    print(tt.max_is_loaded)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
