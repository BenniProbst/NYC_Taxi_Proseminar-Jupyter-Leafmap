from typing import Tuple
from typing import List
from csv import reader
import operator


class TaxiZone:

    def get_from_location_id(self, loc_id: int) -> Tuple[int, str, str, str]:
        for tup in self.zones:
            if tup[0] == loc_id:
                return tup

    def get_from_neighbourhood_name(self, n_name: str) -> Tuple[int, str, str, str]:
        for tup in self.zones:
            if tup[3] == n_name:
                return tup

    def __init__(self, target_path: str):
        self.header: Tuple[str, str, str, str]
        self.zones: List[Tuple[int, str, str, str]] = []

        with open(target_path, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Get all rows of csv from csv_reader object as list of tuples
            list_of_tuples_load = list(map(tuple, csv_reader))
            count: int = 0
            for tup in list_of_tuples_load:
                if count == 0:
                    self.header = (str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]))
                else:
                    self.zones.append((int(tup[0]), str(tup[1]), str(tup[2]), str(tup[3])))
                count += 1
            self.zones.sort(key=operator.itemgetter(0))
