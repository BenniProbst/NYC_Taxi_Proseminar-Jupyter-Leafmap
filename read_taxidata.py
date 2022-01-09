# open file in read mode
from csv import reader
from typing import Tuple
from typing import List
from typing import Dict
from datetime import datetime
import os
import os.path


def list_taxi_files(folder: str) -> List[str]:
    taxi_files_raw: List[str] = os.listdir(folder)
    taxi_files: List[str] = []
    for file_name in taxi_files_raw:
        if 'tripdata' in os.path.basename(file_name):
            taxi_files.append(file_name)
    return taxi_files


def list_taxi_month(files: List[str], taxi_type: str) -> List[datetime]:
    taxi_type_month: List[datetime] = []
    for file in files:
        if file.startswith(taxi_type):
            output_datetime: datetime = datetime.strptime(file.split('_')[2], "%Y-%m")
            taxi_type_month.append(output_datetime)
    return taxi_type_month


class TaxiData:

    def get_date_files(self, year: int, month: int) -> Dict[str, List[datetime]]:
        taxi_color_types_filter: Dict[str, List[datetime]] = {}
        for taxi_colors, taxi_times in self.taxi_color_types:
            for taxi_color_times in taxi_times:
                if datetime(year, month, 0) == taxi_color_times:
                    taxi_color_types_filter[taxi_colors].append(taxi_color_times)
        return taxi_color_types_filter

    def load_available(self, available: Dict[str, List[datetime]]) -> None:
        

    def __init__(self):
        self.data: List[Tuple[int, datetime, datetime, int, float, int, str, int, int, int,
                              float, float, float, float, float, float, float, float]] = []
        # get available files
        self.taxi_files: List[str] = list_taxi_files('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
        # read available month to be read instantly
        self.taxi_color_types: Dict[str, List[datetime]] = {'yellow': list_taxi_month(self.taxi_files, 'yellow'),
                                                            'green': list_taxi_month(self.taxi_files, 'green')}

        """
        with open('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/yellow_tripdata_2021-07.csv', 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Get all rows of csv from csv_reader object as list of tuples
            # list_of_tuples = list(map(tuple, csv_reader))
            list_of_tuples_load = list(map(tuple, csv_reader))
        """
