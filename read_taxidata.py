# open file in read mode
from csv import reader
from typing import NewType
from typing import Tuple
from typing import List
from datetime import datetime
import os
import os.path


# TODO create loading class with type hints


class TaxiData:
    def list_taxi_files(self, folder: str) -> List[str]:
        taxi_files_raw: List[str] = os.listdir(folder)
        taxi_files: List[str] = []
        for file_name in taxi_files_raw:
            if 'tripdata' in os.path.basename(file_name):
                taxi_files.append(file_name)
        return taxi_files

    def __init__(self):
        self.data = NewType('taxi_data', List[Tuple[int, datetime, datetime, int, float, int, str, int, int, int,
                                                    float, float, float, float, float, float, float, float]])
        # open file in read mode
        with open('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/yellow_tripdata_2021-07.csv', 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Get all rows of csv from csv_reader object as list of tuples
            # list_of_tuples = list(map(tuple, csv_reader))
            list_of_tuples_load = list(map(tuple, csv_reader))
