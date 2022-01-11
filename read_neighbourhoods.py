import json
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
import read_taxizone
from decimal import Decimal


class NeighbourhoodData:

    def __init__(self, path):
        tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
        self.neighbourhoodPolynoms: Dict[Tuple[int, str, str, str]: List[Tuple[Decimal, Decimal]]] = []
        tmp_list = json.loads(open(path, 'r').read())
        for features in tmp_list['features']:
            polygon_list: List[Tuple[Decimal, Decimal]] = []
            for point in features['geometry']['coordinates'][0][0]:
                polygon_list.append((Decimal(point[0]), Decimal(point[1])))
            neighbourhood_data: Union[Tuple[int, str, str, str], None] = \
                tz.get_from_neighbourhood_name(features['properties']['neighborhood'])

            if neighbourhood_data is None:
                continue

            self.neighbourhoodPolynoms[neighbourhood_data] = polygon_list
