import read_taxizone
from read_taxidata import TaxiData
from read_neighbourhoods import NeighbourhoodTaxiData
from datetime import datetime, time
import time
from geojson import Feature, FeatureCollection, LineString, dump
from typing import List

VENDOR_ID = 0
PICKUP_TIME = 1
DROPOFF_TIME = 2
PASSENGER_COUNT = 3
TRIP_DISTANCE = 4
RATECODE_ID = 5
PICKUP_LOCATION = 6
STORE_AND_FORWARD = 7
DROPOFF_LOCATION = 8
PAYMENT_TYPE = 9
FARE_AMOUNT = 10
EXTRA = 11
MTA_TAX = 12
TIP_AMOUNT = 13
TOLLS_AMOUNT = 14
IMPROVEMENT_SURCHARGE = 15
TOTAL_AMOUNT = 16
CONGESTION_SURCHARGE = 17
TAXI_COLOR = 18


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
        outfile.close()
        return self.connections

    # PICKUP_TIME, DROPOFF_TIME
    def daytime_filter(self, start: time, end: time, method=PICKUP_TIME):
        new_data = []
        for d in self.data:
            t = d[method].time()
            if start <= t <= end:
                new_data.append(d)
        self.data = new_data

    # VENDOR_ID, PASSENGER_COUNT, TRIP_DISTANCE, RATECODE_ID, FARE_AMOUNT, EXTRA, MTA_TAX, TIP_AMOUNT, TOLLS_AMOUNT,
    # IMPROVEMENT_SURCHARGE, TOTAL_AMOUNT, CONGESTION_SURCHARGE
    def value_filter(self, val_min, val_max, method=TRIP_DISTANCE):
        new_data = []
        for d in self.data:
            t = d[method].time()
            if val_min <= t <= val_max:
                new_data.append(d)
        self.data = new_data

    def flag_filter(self, flag, method=PICKUP_LOCATION, zone_checker=read_taxizone.ZONE):
        if not (method == PICKUP_LOCATION or method == DROPOFF_LOCATION):
            # here the flag is text that may fit a name in the taxi_zone csv
            flag_tuple_translation_list = self.zone_neighborhoods.taxi_zone.get_from_csv_val(flag, zone_checker)
            flag_list = []
            for f in flag_tuple_translation_list:
                # get location ids
                flag_list.append(f[0])

            new_data = []
            for d in self.data:
                if d[method] in flag_list:
                    new_data.append(d)
            self.data = new_data
        else:
            new_data = []
            for d in self.data:
                if flag == d[method]:
                    new_data.append(d)
            self.data = new_data

    def __init__(self, base: str, zone_output: str):
        self.connections = None
        super().__init__(base)
        self.zone_neighborhoods = NeighbourhoodTaxiData(zone_output)
