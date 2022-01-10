from typing import Tuple
from typing import List


class TaxiZone:



    def __init__(self):
        self.header: Tuple[str, str, str, str]
        self.zones: List[Tuple[int, str, str, str]] = []
