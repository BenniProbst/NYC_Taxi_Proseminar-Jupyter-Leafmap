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
        for taxi_colors, taxi_times in self.taxi_color_types_times:
            for taxi_color_times in taxi_times:
                if datetime(year, month, 0) == taxi_color_times:
                    taxi_color_types_filter[taxi_colors].append(taxi_color_times)
        return taxi_color_types_filter

    def load_available(self, available: Dict[str, List[datetime]]) -> bool:
        for taxi_color_request, times_request in available:
            if taxi_color_request in self.taxi_color_types_times.keys():
                if set(times_request).issubset(self.taxi_color_types_times.get(taxi_color_request)):
                    for time in times_request:
                        with open(self.base_folder + taxi_color_request + '_tripdata_' + time.year + '-' + time.month +
                                  '.csv', 'r') as read_obj:
                            # pass the file object to reader() to get the reader object
                            csv_reader = reader(read_obj)
                            # Get all rows of csv from csv_reader object as list of tuples
                            # list_of_tuples = list(map(tuple, csv_reader))
                            list_of_tuples_load = list(map(tuple, csv_reader))
                            list_of_tuples_load_typed: List[Tuple[int, datetime, datetime, int, float, int, str, int,
                                                                  int, int, float, float, float, float, float, float,
                                                                  float, float]] = []
                            for tup in list_of_tuples_load:
                                list_of_tuples_load_typed.append((int(tup[0]),
                                                                  datetime.strptime(tup[1], "%Y-%m-%d %H:%M:%S"),
                                                                  datetime.strptime(tup[2], "%Y-%m-%d %H:%M:%S"),
                                                                  int(tup[3]),
                                                                  float(tup[4]),
                                                                  int(tup[5]),
                                                                  str(tup[6]),
                                                                  int(tup[7]),
                                                                  int(tup[8]),
                                                                  int(tup[9]),
                                                                  float(tup[10]),
                                                                  float(tup[11]),
                                                                  float(tup[12]),
                                                                  float(tup[13]),
                                                                  float(tup[14]),
                                                                  float(tup[15]),
                                                                  float(tup[16]),
                                                                  float(tup[17]),))

                else:
                    return False
            else:
                return False
        return True

    def __init__(self, base: str):
        self.base_folder: str = base
        self.data: List[Tuple[int, datetime, datetime, int, float, int, str, int, int, int,
                              float, float, float, float, float, float, float, float]] = []
        # get available files
        self.taxi_files: List[str] = list_taxi_files(self.base_folder)
        # read available month to be read instantly
        self.taxi_color_types_times: Dict[str, List[datetime]] = {'yellow': list_taxi_month(self.taxi_files, 'yellow'),
                                                                  'green': list_taxi_month(self.taxi_files, 'green')}
