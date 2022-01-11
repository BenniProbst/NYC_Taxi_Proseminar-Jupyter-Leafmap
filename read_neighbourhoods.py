import json
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
import read_taxizone


class NeighbourhoodData:

    def __init__(self, path):
        tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
        self.neighbourhoodPolynoms: Dict[Tuple[int, str, str, str]: List[Tuple[float, float]]] = []
        tmp_list = json.loads(open(path, 'r').read())
        for features in tmp_list['features']:
            polygon_list: List[Tuple[float, float]] = []
            for point in features['geometry']['coordinates'][0][0]:
                polygon_list.append((float(point[0]), float(point[1])))
            data_tuple: Tuple[int, str, str, str] = tz.get_from_location_id(features['properties']['cartodb_id'])
            new_data_tuple: Tuple[int, str, str, str]
            if features['properties']['cartodb_id'] != data_tuple[2]:
                new_data_tuple = (data_tuple[0], data_tuple[1], features['properties']['cartodb_id'], data_tuple[3])
            else:
                new_data_tuple = data_tuple
            neighbourhood_data: Union[Tuple[int, str, str, str], None] = new_data_tuple

            if neighbourhood_data is None:
                continue

            self.neighbourhoodPolynoms[neighbourhood_data] = polygon_list
