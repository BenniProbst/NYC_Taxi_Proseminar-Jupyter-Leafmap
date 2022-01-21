from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData
import datetime
from geojson import Feature, FeatureCollection, Point, LineString
from typing import List


class TaxiTime(TaxiData):

    def interconnections(self, start: datetime, end: datetime) -> FeatureCollection:
        self.load_range(start, end)
        output: FeatureCollection = FeatureCollection(Feature())
        features: List[Feature] = []
        line_count: int = 0
        for d in self.data:
            start_feature: Feature = self.zone_neighborhoods.get_feature(d[7])
            end_feature: Feature = self.zone_neighborhoods.get_feature(d[8])
            prop = {'start': start_feature['properties'], 'end': end_feature['properties'], 'data': d}
            start_point: tuple = (start_feature['properties']['center'][0], start_feature['properties']['center'][1])
            end_point: tuple = (end_feature['properties']['center'][0], end_feature['properties']['center'][1])
            features.append(Feature(id=line_count, geometry=LineString([start_point, end_point]), properties=prop))
            line_count += 1

        return FeatureCollection(features)

    def __init__(self, base: str, zone_output: str):
        super().__init__(base)
        self.zone_neighborhoods = NeighbourhoodTaxiData(zone_output)
        pass