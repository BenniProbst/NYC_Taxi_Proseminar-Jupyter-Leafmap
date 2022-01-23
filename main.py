# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import dave

import read_taxidata
from get_drives_by_time import TaxiTime
from datetime import datetime
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tt = TaxiTime('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/', '/home/benjamin-elias/PycharmProjects'
                                                                           '/Proseminar '
                                                                           'Jupyter-Leafmap/nyc-neighborhoods.geojson')
    """
    # standard range load
    start = datetime(2020, 2, 10)
    end = datetime(2020, 5, 25)
    tt.load_range(start, end)
    print('Analyze time between 10-02-2020 and 25-05-2020')
    print(tt.min_is_loaded)
    print(tt.max_is_loaded)

    # efficient range reload
    start = datetime(2020, 3, 10)
    end = datetime(2020, 6, 25)
    tt.load_range(start, end)
    print('Analyze time between 10-03-2020 and 25-06-2020')
    print(tt.min_is_loaded)
    print(tt.max_is_loaded)
    """

    # speed range resize to smaller subset of current load
    start = datetime(2020, 4, 10)
    end = datetime(2020, 6, 24)
    tt.load_range(start, end)
    print('Analyze time between 10-04-2020 and 24-06-2020')
    print(tt.min_is_loaded)
    print(tt.max_is_loaded)

    # taxi drive connections and neighborhood central points on map
    con = tt.interconnections(start, end, '/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/rides.geojson')
    points = tt.zone_neighborhoods.neighbourhood_points('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/neighborhood_centers.geojson')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
