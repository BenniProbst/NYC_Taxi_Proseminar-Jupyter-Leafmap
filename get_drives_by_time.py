from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData


class TaxiTime:
    def __init__(self):
        self.zone_neighborhoods = NeighbourhoodTaxiData('/home/benjamin-elias/PycharmProjects/Proseminar '
                                                        'Jupyter-Leafmap/nyc-neighborhoods.geo.json')
        self.zone_neighborhoods.to_geojson('/home/benjamin-elias/PycharmProjects/Proseminar '
                                           'Jupyter-Leafmap/taxi_zones.geo.json')
        self.big_taxi_data = TaxiData('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/')
