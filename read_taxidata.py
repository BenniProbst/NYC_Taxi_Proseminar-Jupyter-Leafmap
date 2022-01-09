# open file in read mode
from csv import reader
from typing import Tuple
from typing import List
from typing import Dict
from datetime import *
import os
import os.path
import operator
from heapq import merge


def list_taxi_files(folder: str) -> List[str]:
    taxi_files_raw: List[str] = os.listdir(folder)
    taxi_files: List[str] = []
    for file_name in taxi_files_raw:
        if 'tripdata' in os.path.basename(file_name).split('.')[0]:
            taxi_files.append(file_name)
    return taxi_files


def list_taxi_month(files: List[str], taxi_type: str) -> List[datetime]:
    taxi_type_month: List[datetime] = []
    for file in files:
        if file.startswith(taxi_type):
            datestring_csv: str = file.split('_')[2]
            datestring: str = datestring_csv.split('.')[0]
            output_datetime: datetime = datetime.strptime(datestring, "%Y-%m")
            taxi_type_month.append(output_datetime)
    return taxi_type_month


class TaxiData:

    def get_date_files(self, year: int, month: int) -> Dict[str, List[datetime]]:
        taxi_color_types_filter: Dict[str, List[datetime]] = {}
        request_datetime: datetime = datetime(year, month, 1)
        for taxi_colors, taxi_times in self.taxi_color_types_times.items():
            if request_datetime in taxi_times:
                if not (taxi_colors in taxi_color_types_filter.keys()):
                    taxi_color_types_filter[taxi_colors] = []
                taxi_color_types_filter[taxi_colors].append(request_datetime)

        return taxi_color_types_filter

    def load_available(self, available: Dict[str, List[datetime]]) -> bool:
        self.data = []
        for taxi_color_request, times_request in available.items():
            if taxi_color_request in self.taxi_color_types_times.keys():
                if set(times_request).issubset(self.taxi_color_types_times.get(taxi_color_request)):
                    for times in times_request:
                        build_month: str = str(times.month)
                        while len(build_month) <= 1:
                            build_month = str(0) + build_month
                        build_file_name: str = self.base_folder + taxi_color_request + '_tripdata_' + str(times.year) + str('-') + build_month + '.csv'
                        with open(build_file_name, 'r') as read_obj:
                            # pass the file object to reader() to get the reader object
                            csv_reader = reader(read_obj)
                            # Get all rows of csv from csv_reader object as list of tuples
                            # list_of_tuples = list(map(tuple, csv_reader))
                            list_of_tuples_load = list(map(tuple, csv_reader))
                            list_of_tuples_load_typed: List[Tuple[int, datetime, datetime, int, float, int, str, int,
                                                                  int, int, float, float, float, float, float, float,
                                                                  float, float]] = []

                            count: int = 0
                            for tup in list_of_tuples_load:
                                output_tup: Tuple[int, datetime, datetime, int, float, int, str, int,
                                                  int, int, float, float, float, float, float, float,
                                                  float, float] = (int(tup[0]),
                                                                   datetime.strptime(str(tup[1]), "%Y-%m-%d %H:%M:%S"),
                                                                   datetime.strptime(str(tup[2]), "%Y-%m-%d %H:%M:%S"),
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
                                                                   float(tup[17]))

                                if count == 0:
                                    self.header: Tuple[int, datetime, datetime, int, float, int, str, int,
                                                       int, int, float, float, float, float, float, float,
                                                       float, float] = output_tup
                                else:
                                    list_of_tuples_load_typed.append(output_tup)
                                count += 1
                            # sort to pickup time
                            list_of_tuples_load_typed = sorted(list_of_tuples_load_typed, key=operator.itemgetter(1))
                            self.data = list(merge(self.data, list_of_tuples_load_typed, key=operator.itemgetter(1)))
                else:
                    return False
            else:
                return False
        return True

    def __init__(self, base: str):
        self.header = None
        self.base_folder: str = base
        self.data: List[Tuple[int, datetime, datetime, int, float, int, str, int, int, int,
                              float, float, float, float, float, float, float, float]] = []
        # get available files
        self.taxi_files: List[str] = list_taxi_files(self.base_folder)
        # read available month to be read instantly
        self.taxi_color_types_times: Dict[str, List[datetime]] = {'yellow': list_taxi_month(self.taxi_files, 'yellow'),
                                                                  'green': list_taxi_month(self.taxi_files, 'green')}
