import json
from typing import List
from typing import Tuple
import read_taxizone
from Levenshtein import distance


class NeighbourhoodData:

    def __init__(self, path):
        tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
        self.neighbourhoodTuples: List[Tuple[int, str, str, str]] = []
        # multiple neighborhood polynoms for every taxi zone
        self.neighbourhoodPolynoms = []
        tmp_list = json.loads(open(path, 'r').read())
        for features in tmp_list['features']:
            data_tuple: Tuple[int, str, str, str] = \
                tz.get_alike_from_neighborhood_name(features['properties']['NTAName'])
            polygon_list: List[Tuple[float, float]] = []
            if features['geometry']['type'] == 'MultiPolygon':
                for point in features['geometry']['coordinates'][0][0]:
                    polygon_list.append((float(point[0]), float(point[1])))
            else:
                if features['geometry']['type'] == 'Polygon':
                    for point in features['geometry']['coordinates'][0]:
                        polygon_list.append((float(point[0]), float(point[1])))

            if data_tuple in self.neighbourhoodTuples:
                self.neighbourhoodPolynoms[self.neighbourhoodTuples.index(data_tuple)].append(polygon_list)
            else:
                self.neighbourhoodTuples.append(data_tuple)
                self.neighbourhoodPolynoms.append([polygon_list])

        # double join and look for fitting neighborhoods for each taxi zone
        for zone_tup in tz.zones:
            # filter unknown and set them anywhere
            if zone_tup[0] == 264 or zone_tup[0] == 265:
                self.neighbourhoodTuples.append(zone_tup)
                self.neighbourhoodPolynoms.append([[(40.54999, -73.99562)]])
                continue
            if not (zone_tup in self.neighbourhoodTuples):
                min_dist: int = 99999
                polygon_list: List[Tuple[float, float]] = []
                neighborhood_name: str = ''
                loop_breaker: bool = False
                for features in tmp_list['features']:
                    for variants in zone_tup[2].split('/'):
                        if variants == 'Newark Airport':
                            self.neighbourhoodTuples.append(zone_tup)
                            self.neighbourhoodPolynoms.append([[(40.68883, -74.18003)]])
                            loop_breaker = True
                            print('Draw '+variants+' to outer New York.')
                            break
                        cur_polygon_list: List[Tuple[float, float]] = []
                        if features['properties']['NTAName'].find(variants) != -1:
                            if features['geometry']['type'] == 'MultiPolygon':
                                for point in features['geometry']['coordinates'][0][0]:
                                    cur_polygon_list.append((float(point[0]), float(point[1])))
                            else:
                                if features['geometry']['type'] == 'Polygon':
                                    for point in features['geometry']['coordinates'][0]:
                                        cur_polygon_list.append((float(point[0]), float(point[1])))

                            if variants == features['properties']['NTAName']:
                                self.neighbourhoodTuples.append(zone_tup)
                                self.neighbourhoodPolynoms.append([cur_polygon_list])
                                loop_breaker = True
                                print('Double joined missing tuple '+str(zone_tup)+' to the neighborhood '+
                                      features['properties']['NTAName'])
                                break
                            else:
                                cur_dist = abs(len(variants) - len(features['properties']['NTAName']))
                                if cur_dist < min_dist:
                                    min_dist = cur_dist
                                    polygon_list = cur_polygon_list
                                    neighborhood_name = features['properties']['NTAName']

                        cur_dist = distance(variants, features['properties']['NTAName'])
                        if cur_dist < min_dist:
                            min_dist = cur_dist
                            if features['geometry']['type'] == 'MultiPolygon':
                                for point in features['geometry']['coordinates'][0][0]:
                                    cur_polygon_list.append((float(point[0]), float(point[1])))
                            else:
                                if features['geometry']['type'] == 'Polygon':
                                    for point in features['geometry']['coordinates'][0]:
                                        cur_polygon_list.append((float(point[0]), float(point[1])))
                            polygon_list = cur_polygon_list
                            neighborhood_name = features['properties']['NTAName']
                    if loop_breaker:
                        break

                if not loop_breaker:
                    self.neighbourhoodTuples.append(zone_tup)
                    self.neighbourhoodPolynoms.append([polygon_list])
                    print('Double joined missing tuple ' + str(zone_tup) + ' to the neighborhood ' +
                          neighborhood_name)


