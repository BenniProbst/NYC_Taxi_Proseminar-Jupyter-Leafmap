import json
from typing import Dict
from typing import List
from typing import Tuple
from typing import Union
import read_taxizone


class NeighbourhoodData:

    def __init__(self, path):
        tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
        self.neighbourhoodTuples: List[Tuple[int, str, str, str]] = []
        self.neighbourhoodPolynoms: List[List[Tuple[float, float]]] = []
        tmp_list = json.loads(open(path, 'r').read())
        for features in tmp_list['features']:
            data_tuple: Tuple[int, str, str, str] = tz.get_alike_from_neighborhood_name(features['properties']['neighborhood'])
            if data_tuple is None:
                continue
            polygon_list: List[Tuple[float, float]] = []
            for point in features['geometry']['coordinates'][0][0]:
                polygon_list.append((float(point[0]), float(point[1])))
            new_data_tuple: Tuple[int, str, str, str]
            if features['properties']['cartodb_id'] != data_tuple[2]:
                new_data_tuple = (data_tuple[0], data_tuple[1], features['properties']['cartodb_id'], data_tuple[3])
            else:
                new_data_tuple = data_tuple

            self.neighbourhoodTuples.append(new_data_tuple)
            self.neighbourhoodPolynoms.append(polygon_list)
