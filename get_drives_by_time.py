from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData
import datetime
from geojson import Feature, FeatureCollection, LineString, dump
from typing import List


class TaxiTime(TaxiData):

    def interconnections(self, start: datetime, end: datetime, path_out: str) -> FeatureCollection:
        self.load_range(start, end)
        features: List[Feature] = []
        line_count: int = 0
        for d in self.data:
            start_feature: Feature = self.zone_neighborhoods.get_feature(d[7])
            end_feature: Feature = self.zone_neighborhoods.get_feature(d[8])
            output_data = []
            count: int = 0
            for item in list(d):
                if count == 1 or count == 2:
                    output_data.append(str(item))
                else:
                    output_data.append(item)
                count += 1
            prop = {'start': start_feature['properties'], 'end': end_feature['properties'], 'data': output_data}
            start_point: tuple = (start_feature['properties']['center'][0], start_feature['properties']['center'][1])
            end_point: tuple = (end_feature['properties']['center'][0], end_feature['properties']['center'][1])
            features.append(Feature(id=line_count, geometry=LineString([start_point, end_point]), properties=prop))
            line_count += 1
        self.connections = FeatureCollection(features)
        with open(path_out, 'w') as outfile:
            dump(self.connections, outfile)
        return self.connections

    def __init__(self, base: str, zone_output: str):
        self.connections = None
        super().__init__(base)
        self.zone_neighborhoods = NeighbourhoodTaxiData(zone_output)
