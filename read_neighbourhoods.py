import json
from typing import Dict
from typing import List
from typing import Tuple
import read_taxizone


class NeighbourhoodData:

    def __init__(self, path):
        tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
        self.neighbourhoodPolynoms: Dict[Tuple[int, str, str, str]: List[Tuple[float, float]]] = []
        tmp_list = json.load(path)
