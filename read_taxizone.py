from typing import Tuple
from typing import List
from typing import Union
from csv import reader
import operator
from Levenshtein import distance

LOCATION_ID = 0
BOROUGH = 1
ZONE = 2
SERVICE_ZONE = 3


def filter_brackets(input_string: str) -> str:
    return input_string.replace('(', '').replace(')', '')


class TaxiZone:

    def get_from_csv_val(self, val: int, method=LOCATION_ID) -> Union[List[Tuple[int, str, str, str]], None]:
        if method == LOCATION_ID:
            for tup in self.zones:
                if tup[method] == val:
                    return [tup]
        else:
            output = []
            for tup in self.zones:
                if tup[method] == val:
                    output.append(tup)
            return output
        return None

    def get_alike_from_neighborhood_name(self, n_name: str) -> Tuple[int, str, str, str]:
        # find maximum alike taxi zone to the neighborhood name
        n_name.replace('-', '/')
        candidates = set()
        for neighborhood_tup in self.zones:
            for name_variants in neighborhood_tup[2].split('/'):
                if n_name.find(name_variants) != -1 or name_variants.find(n_name) != -1 or \
                        n_name.find(filter_brackets(name_variants)) != -1 or \
                        name_variants.find(filter_brackets(n_name)) != -1:
                    if not set(neighborhood_tup).issubset(candidates):
                        candidates.add(neighborhood_tup)

        if len(candidates) == 1:
            for c in candidates:
                return c

        if len(candidates) == 0:
            print('Not really found: ' + n_name)
        else:
            print('Multiple found: ' + n_name)
            print(candidates)

        # find min dist
        dist_lev: int = 999999
        most_likely_tup: Tuple[int, str, str, str] = self.zones[0]
        if len(candidates) == 0:
            for neighborhood_tup in self.zones:
                for name_variants in neighborhood_tup[2].split('/'):
                    dist_cur = min(distance(n_name, name_variants),
                                   distance(filter_brackets(n_name), filter_brackets(name_variants)))
                    if dist_cur < dist_lev:
                        dist_lev = dist_cur
                        most_likely_tup = neighborhood_tup
        else:
            for neighborhood_tup in candidates:
                for name_variants in neighborhood_tup[2].split('/'):
                    if len(name_variants) == len(n_name) and name_variants == n_name:
                        print('Length analysis showed that this should be correct on the input taxi lookup table:')
                        print(neighborhood_tup)
                        print('')
                        return neighborhood_tup
                    dist_cur = min(distance(n_name, name_variants),
                                   distance(filter_brackets(n_name), filter_brackets(name_variants)))
                    if dist_cur < dist_lev:
                        dist_lev = dist_cur
                        most_likely_tup = neighborhood_tup

        print('Estimated this very alike information instead on the taxi lookup table:')
        print(most_likely_tup)
        print('')

        return most_likely_tup

    def __init__(self, target_path: str):
        self.header: Tuple[str, str, str, str]
        self.zones: List[Tuple[int, str, str, str]] = []
        list_of_tuples_load = None
        with open(target_path, 'r') as read_obj:
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Get all rows of csv from csv_reader object as list of tuples
            list_of_tuples_load = list(map(tuple, csv_reader))
        read_obj.close()
        count: int = 0
        for tup in list_of_tuples_load:
            if count == 0:
                self.header = (str(tup[0]), str(tup[1]), str(tup[2]), str(tup[3]))
            else:
                self.zones.append((int(tup[0]), str(tup[1]), str(tup[2]), str(tup[3])))
            count += 1
        self.zones.sort(key=operator.itemgetter(0))
