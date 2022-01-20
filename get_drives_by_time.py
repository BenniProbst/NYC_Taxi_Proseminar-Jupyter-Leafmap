from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData
import datetime


class TaxiTime(TaxiData):
    def __init__(self, base: str, zone_output: str):
        super().__init__(base)
        self.zone_neighborhoods = NeighbourhoodTaxiData(zone_output)
