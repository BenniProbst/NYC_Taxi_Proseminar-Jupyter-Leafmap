from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData
import datetime


class TaxiTime:
    def __init__(self):
        self.zone_neighborhoods = NeighbourhoodTaxiData('/home/benjamin-elias/PycharmProjects/Proseminar '
                                                        'Jupyter-Leafmap/nyc-neighborhoods.geojson')
        self.big_taxi_data = TaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
        pass
