# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import get_drives_by_time
import read_taxizone
from get_drives_by_time import TaxiTime
from datetime import datetime, time
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
    print('Analyze time between 10-02-2020 01:01 and 25-05-2020 01:02')
    print(tt.min_is_loaded)
    print(tt.max_is_loaded)

    print('Filter daytime:')

    # taxi drive connections and neighborhood central points on map
    con = tt.interconnections(start, end,
                              '/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/rides.geojson')
    points = tt.zone_neighborhoods.neighbourhood_points(
        '/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/neighborhood_centers.geojson')

    print("Daytime filter:")
    # limit to main work time
    tt.daytime_filter(time(8), time(17))
    # limit trip distance
    tt.value_filter(0, 20)
    # limit Pickup to Bloomingdale
    tt.flag_filter('Bloomingdale/Upper West Side North', method=get_drives_by_time.PICKUP_LOCATION,
                   zone_checker=read_taxizone.ZONE)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
