from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData
import datetime


class TaxiTime:
    def __init__(self):
        self.zone_neighborhoods = NeighbourhoodTaxiData('/home/benjamin-elias/PycharmProjects/Proseminar '
                                                        'Jupyter-Leafmap/nyc-neighborhoods.geo.json')
        self.zone_neighborhoods.to_geojson('/home/benjamin-elias/PycharmProjects/Proseminar '
                                           'Jupyter-Leafmap/taxi_zones.geo.json')
        self.big_taxi_data = TaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
        self.min_time: datetime = self.big_taxi_data.get_minimum_available_pickup_time()
        self.max_time: datetime = self.big_taxi_data.get_maximum_available_pickup_time()
