# open file in read mode
from csv import reader
from typing import Tuple

#TODO create loading class with type hints

# open file in read mode
with open('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/yellow_tripdata_2021-07.csv', 'r') as read_obj:
    # pass the file object to reader() to get the reader object
    csv_reader = reader(read_obj)
    # Get all rows of csv from csv_reader object as list of tuples
    # list_of_tuples = list(map(tuple, csv_reader))
    list_of_tuples = list(map(tuple, csv_reader))

    # display all rows of csv
    # print(list_of_tuples)