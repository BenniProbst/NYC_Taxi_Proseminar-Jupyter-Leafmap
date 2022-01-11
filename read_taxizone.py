from typing import Tuple
from typing import List
from typing import Union
from csv import reader
import operator
from Levenshtein import distance


class TaxiZone:

    def get_from_location_id(self, loc_id: int) -> Union[Tuple[int, str, str, str], None]:
        for tup in self.zones:
            if tup[0] == loc_id:
                return tup
        return None

    def get_from_neighborhood_name(self, n_name: str) -> Union[Tuple[int, str, str, str], None]:
        for tup in self.zones:
            if tup[2] == n_name:
                return tup
        return None

    def get_alike_from_neighborhood_name(self, n_name: str) -> Tuple[int, str, str, str]:
        # find max alikeness
        candidates: List[Tuple[int, str, str, str]] = []
        for neighborhood_tup in self.zones:
            if n_name.find(neighborhood_tup[2]) != -1 or neighborhood_tup[2].find(n_name) != -1:
                candidates.append(neighborhood_tup)

        if len(candidates) == 1:
            return candidates[0]

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
                dist_cur = distance(n_name, neighborhood_tup[2])
                if dist_cur < dist_lev:
                    dist_lev = dist_cur
                    most_likely_tup = neighborhood_tup
        else:
            for neighborhood_tup in candidates:
                if len(neighborhood_tup[2]) == len(n_name):
                    print('Length analysis showed that this should be correct on the input taxi lookup table:')
                    print(neighborhood_tup)
                    print('')
                    return neighborhood_tup
                dist_cur = distance(n_name, neighborhood_tup[2])
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
