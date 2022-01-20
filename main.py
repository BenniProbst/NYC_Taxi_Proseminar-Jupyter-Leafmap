# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from get_drives_by_time import TaxiTime
from datetime import datetime
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tt = TaxiTime('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
    pass
    start = datetime(2020, 2, 10)
    end = datetime(2020, 5, 25)
    tt.load_range(start, end)
    start = datetime(2020, 3, 10)
    end = datetime(2020, 6, 25)
    tt.load_range(start, end)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
