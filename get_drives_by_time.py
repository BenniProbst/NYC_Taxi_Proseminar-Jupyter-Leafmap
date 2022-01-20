from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData
import datetime


class TaxiTime(TaxiData):
    def __init__(self, base: str):
        super().__init__(base)
        self.zone_neighborhoods = NeighbourhoodTaxiData('/home/benjamin-elias/PycharmProjects/Proseminar '
                                                        'Jupyter-Leafmap/nyc-neighborhoods.geojson')
