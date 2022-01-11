import json
from typing import Dict
from typing import List
from typing import Tuple


class NeighbourhoodData:

    def __init__(self, path):
        self.neighbourhoodPolynoms: Dict[str: List[Tuple[float, float]]] = []
        tmp_list = json.load(path)
