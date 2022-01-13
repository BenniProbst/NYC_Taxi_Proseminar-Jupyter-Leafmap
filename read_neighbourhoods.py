import json
from typing import List
from typing import Tuple
import read_taxizone
from Levenshtein import distance
import geopy.distance as geo_dist
from pyproj import Geod
import multiprocessing
from threading import Lock
import concurrent.futures


def distance_line(p1, p2):
    return geo_dist.distance(p1, p2).mi


def single_central_point(polygon: List[Tuple[float, float]]) -> Tuple[Tuple[float, float], float]:
    if len(polygon) == 0:
        raise ValueError('The polygon list shall not be empty!')
    if len(polygon) == 1:
        tup: Tuple[float, float] = polygon[0]
        dist_len: float = 0
        return tup, dist_len
    if len(polygon) == 2:
        x_tup: float = (polygon[0][0] / 2) + (polygon[1][0] / 2)
        y_tup: float = (polygon[0][1] / 2) + (polygon[1][1] / 2)
        tup: Tuple[float, float] = (x_tup, y_tup)
        dist_len: float = distance_line(polygon[0], polygon[1])
        out_tup: Tuple[Tuple[float, float], float] = (tup, dist_len)
        return out_tup
    # a list containing the to analyse point at the front and the other two connected points
    point_connection_lines: List[Tuple[Tuple[float, float], List[Tuple[float, float]], float]] = [
        (polygon[0], [polygon[-1], polygon[1]],
         distance_line(polygon[0], polygon[-1]) + distance_line(polygon[0], polygon[1]))]

    for i in range(1, len(polygon) - 1):
        point_connection_lines.append((polygon[i], [polygon[i - 1], polygon[i + 1]],
                                       distance_line(polygon[i], polygon[i - 1]) +
                                       distance_line(polygon[i], polygon[i + 1])))

    point_connection_lines.append((polygon[-1], [polygon[-2], polygon[0]],
                                   distance_line(polygon[-1], polygon[-2]) +
                                   distance_line(polygon[-1], polygon[0])))

    relative_distance_add: float = 0
    for p in point_connection_lines:
        relative_distance_add += p[2]

    out_x: float = 0
    out_y: float = 0

    for p in point_connection_lines:
        out_x += (p[0][0] * (p[2] / relative_distance_add))
        out_y += (p[0][1] * (p[2] / relative_distance_add))

    out_tup: Tuple[float, float] = (out_x, out_y)
    out_tup_rel: Tuple[Tuple[float, float], float] = (out_tup, relative_distance_add / 2)
    return out_tup_rel


def geo_polygon_area(polygon: List[Tuple[float, float]]) -> float:
    # TODO: convert tuples to list
    if len(polygon) <= 2:
        return 0
    # Define WGS84 as CRS:
    geod = Geod('+a=6378137 +f=0.0033528106647475126')
    lats = polygon[:, 1]
    lons = polygon[:, 0]
    # Compute:
    area, perim = geod.polygon_area_perimeter(lons, lats)
    return abs(area) * (1 / (1.609344 ** 2))  # area in miles


def polygon_array_central_point(polygon_array: List[List[Tuple[float, float]]]) -> Tuple[Tuple[float, float], float]:
    polygon_center_list: List[Tuple[Tuple[float, float], float]] = []
    for polygon in polygon_array:
        polygon_center_list.append(single_central_point(polygon))
    out_x: float = 0
    out_y: float = 0
    borderline_size: float = 0
    for point in polygon_center_list:
        out_x += (point[0][0] / len(polygon_center_list))
        out_y += (point[0][1] / len(polygon_center_list))
        borderline_size += point[1]
    out_tup: Tuple[float, float] = (out_x, out_y)
    return out_tup, borderline_size


class NeighbourhoodTaxiData:

    def to_geojson(self, path_out: str) -> None:
        output_json = {'type': 'FeatureCollection',
                       'crs': {'type': 'name', 'properties': {'name': 'EPSG:4326/taxi_zone'}},
                       'features': []
                       }
        self.central_points()
        for i in range(0, len(self.neighbourhoodTuples)):
            feature = {'type': 'Feature', 'id': i + 1, 'properties': {
                'OBJECTID': i + 1, 'LocationID': self.neighbourhoodTuples[i][0],
                'Borough': self.neighbourhoodTuples[i][1], 'Zone': self.neighbourhoodTuples[i][2],
                'service_zone': self.neighbourhoodTuples[i][3], 'center': self.centrals[i]
            }, 'geometry': {}}

            feature['properties']['borderline_miles'] = self.borderline_sizes[i]

            zone_area: float = 0
            for polygon in self.neighbourhoodPolynoms[i]:
                zone_area += geo_polygon_area(polygon)
            feature['properties']['zone_area'] = zone_area

            if len(self.neighbourhoodPolynoms[i]) == 1:
                feature['geometry']['type'] = 'Polygon'
                feature['geometry']['coordinates'] = [[self.neighbourhoodPolynoms[i][0]]]
            else:
                feature['geometry']['type'] = 'MultiPolygon'
                feature['geometry']['coordinates'] = [[self.neighbourhoodPolynoms[i]]]

            output_json['features'].append(feature)
        with open(path_out, 'w') as outfile:
            json.dump(output_json, outfile)

    def central_points(self) -> List[Tuple[float, float]]:
        self.centrals = []

        with concurrent.futures.ThreadPoolExecutor() as executor:
            thread_num: int = 0
            thread_list = []
            while thread_num < len(self.neighbourhoodPolynoms):
                while len(self.centrals) <= thread_num:
                    self.centrals.append((0, 0))
                    self.borderline_sizes.append(0)
                thread_list.append((thread_num,
                                    executor.submit(polygon_array_central_point,
                                                    self.neighbourhoodPolynoms[thread_num])))

                thread_num += 1
                if len(thread_list) < multiprocessing.cpu_count()*2 and \
                        not (thread_num == len(self.neighbourhoodPolynoms)):
                    continue
                while True:
                    for t in thread_list:
                        if t[1].done():
                            return_value = t[1].result()
                            self.datamutex.acquire()
                            self.centrals[t[0]] = return_value[0]
                            self.borderline_sizes[t[0]] = return_value[1]
                            self.datamutex.release()
                            thread_list.remove(t)
                    if thread_num < len(self.neighbourhoodPolynoms) or \
                            (thread_num == len(self.neighbourhoodPolynoms) and len(thread_list) == 0):
                        break

        return self.centrals

    def __init__(self, path):
        self.datamutex: Lock() = Lock()
        self.centrals: List[Tuple[float, float]] = []
        self.borderline_sizes: List[float] = []
        tz = read_taxizone.TaxiZone('/home/benjamin-elias/Proseminar/Jupyterlab/taxi_data/taxi+_zone_lookup.csv')
        self.neighbourhoodTuples: List[Tuple[int, str, str, str]] = []
        # multiple neighborhood polynoms for every taxi zone
        self.neighbourhoodPolynoms: List[List[List[Tuple[float, float]]]] = []
        tmp_list = json.loads(open(path, 'r').read())
        self.input_geojson = tmp_list
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
                self.neighbourhoodPolynoms.append([[(-73.99562, 40.54999)]])
                continue
            if not (zone_tup in self.neighbourhoodTuples):
                min_dist: int = 99999
                polygon_list: List[Tuple[float, float]] = []
                neighborhood_name: str = ''
                loop_breaker: bool = False
                for features in tmp_list['features']:
                    neighborhood_name_tmp = features['properties']['NTAName'].replace('-', '/')
                    for neighborhood_name_tmp_i in neighborhood_name_tmp.split('/'):
                        for variants in zone_tup[2].split('/'):
                            if variants == 'Newark Airport':
                                self.neighbourhoodTuples.append(zone_tup)
                                self.neighbourhoodPolynoms.append([[(-74.18003, 40.68883)]])
                                loop_breaker = True
                                print('Draw ' + variants + ' to outer New York.')
                                break
                            cur_polygon_list: List[Tuple[float, float]] = []
                            if neighborhood_name_tmp_i.find(variants) != -1:
                                # alike string name of neighborhood was found in geojson
                                if features['geometry']['type'] == 'MultiPolygon':
                                    for point in features['geometry']['coordinates'][0][0]:
                                        cur_polygon_list.append((float(point[0]), float(point[1])))
                                else:
                                    if features['geometry']['type'] == 'Polygon':
                                        for point in features['geometry']['coordinates'][0]:
                                            cur_polygon_list.append((float(point[0]), float(point[1])))

                                if variants == neighborhood_name_tmp_i or neighborhood_name_tmp_i.startswith(variants):
                                    self.neighbourhoodTuples.append(zone_tup)
                                    self.neighbourhoodPolynoms.append([cur_polygon_list])
                                    loop_breaker = True
                                    print('Double joined missing tuple ' + str(zone_tup) + ' to the neighborhood ' +
                                          neighborhood_name_tmp_i)
                                    break
                                else:
                                    cur_dist = 0
                                    if len(variants) > len(neighborhood_name_tmp_i):
                                        cur_dist = abs(len(variants) - len(neighborhood_name_tmp_i))
                                    else:
                                        cur_dist = len(neighborhood_name_tmp_i) - abs(len(variants))

                                    if cur_dist < min_dist:
                                        min_dist = cur_dist
                                        polygon_list = cur_polygon_list
                                        neighborhood_name = neighborhood_name_tmp_i

                            cur_dist = distance(variants, neighborhood_name_tmp_i)
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
                                neighborhood_name = neighborhood_name_tmp_i
                        if loop_breaker:
                            break
                    if loop_breaker:
                        break

                if not loop_breaker:
                    self.neighbourhoodTuples.append(zone_tup)
                    self.neighbourhoodPolynoms.append([polygon_list])
                    print('Double joined missing tuple ' + str(zone_tup) + ' to the neighborhood ' +
                          neighborhood_name)
