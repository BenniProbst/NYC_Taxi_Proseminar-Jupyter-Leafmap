import json

from geojson import Polygon, MultiPolygon, Point, Feature, FeatureCollection, dump
from typing import List
from typing import Tuple
import read_taxizone
from Levenshtein import distance
import geopy.distance as geo_dist
from pyproj import Geod
from threading import Lock
import concurrent.futures
from shapely.ops import unary_union
from shapely.geometry import Polygon as S_Polygon
from geopandas import GeoSeries


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
    lons = []
    for p in polygon:
        lons.append(p[0])
    lats = []
    for p in polygon:
        lats.append(p[1])
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


def valid_multi_polygon(multi_polygon) -> bool:
    valid: bool = True
    for i1 in range(0, len(multi_polygon)):
        for i2 in range(0, len(multi_polygon)):
            if i1 == i2:
                continue
            i3: int = 0
            i4: int = 0
            while i3 < len(multi_polygon[i1]):
                counter: int = 0
                while i4 < len(multi_polygon[i1]):
                    if multi_polygon[i1][(i3 + counter) % len(multi_polygon[i1])] != \
                            multi_polygon[i2][(i4 + counter) % len(multi_polygon[i2])]:
                        i4 += 1
                        continue
                    counter += 1
                if counter > 1:
                    valid = False
                    break
                i3 += 1
            if not valid:
                break
        if not valid:
            break
    return valid


def create_list(r1, r2):
    # Testing if range r1 and r2
    # are equal
    if r1 == r2:
        return r1

    else:

        # Create empty list
        res = []

        # loop to append successors to
        # list until r2 is reached.
        while r1 < r2 + 1:
            res.append(r1)
            r1 += 1
        return res


class NeighbourhoodTaxiData:

    def to_geojson(self, path_out: str) -> None:
        features = []
        self.central_points()
        for i in range(0, len(self.neighbourhoodTuples)):
            zone_area: float = 0
            for polygon in self.neighbourhoodPolynoms[i]:
                zone_area += geo_polygon_area(polygon)

            prop = {
                'LocationID': self.neighbourhoodTuples[i][0],
                'Borough': self.neighbourhoodTuples[i][1], 'Zone': self.neighbourhoodTuples[i][2],
                'service_zone': self.neighbourhoodTuples[i][3], 'center': [self.centrals[i][0], self.centrals[i][1]],
                'Shape__Length': self.borderline_sizes[i], 'Shape__Area': zone_area
            }

            if len(self.neighbourhoodPolynoms[i]) == 1:
                if len(self.neighbourhoodPolynoms[i][0]) == 1:
                    for p1 in self.neighbourhoodPolynoms[i][0]:
                        feature = Feature(id=i + 1, properties=prop, geometry=Point(p1))
                        features.append(feature)
                else:
                    feature = Feature(id=i + 1, properties=prop, geometry=Polygon(self.neighbourhoodPolynoms[i]))
                    features.append(feature)
            else:
                polygons: List[S_Polygon] = []
                for p1 in self.neighbourhoodPolynoms[i]:
                    polygons.append(S_Polygon(p1))

                for p1 in polygons:
                    df1 = GeoSeries([p1])
                    for p2 in polygons:
                        if p1 == p2:
                            continue
                        df2 = GeoSeries([p2])
                        if any(df1.touches(df2, align=False)) or any(df1.overlaps(df2, align=False)):
                            polygons.append(S_Polygon(list(unary_union([p1, p2]).exterior.coords)))
                            polygons.remove(p1)
                            polygons.remove(p2)

                if len(polygons) == 1:
                    feature = Feature(id=i + 1, properties=prop, geometry=Polygon([list(polygons[0].exterior.coords)]))
                    features.append(feature)
                else:
                    out_polygons = []
                    for p in polygons:
                        out_polygons.append(list(p.exterior.coords))
                    feature = Feature(id=i + 1, properties=prop, geometry=MultiPolygon([out_polygons]))
                    features.append(feature)

        self.feature_collection = FeatureCollection(features)
        with open(path_out, 'w') as outfile:
            dump(self.feature_collection, outfile)
        outfile.close()

    def central_points(self) -> List[Tuple[float, float]]:
        if len(self.centrals):
            return self.centrals
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

    def get_feature(self, id_num: int) -> Feature:
        for f in self.feature_collection.features:
            if f['properties']['LocationID'] == id_num:
                return f
        raise ValueError('The id for the feature was not found.')

    def neighbourhood_points(self, path_out: str):
        features: List[Feature] = []
        line_count: int = 0
        for f in self.feature_collection['features']:
            prop = f['properties']
            start_point: tuple = (prop['center'][0], prop['center'][1])
            features.append(Feature(id=line_count, geometry=Point(start_point), properties=prop))
            line_count += 1
        self.central_points_features = FeatureCollection(features)
        with open(path_out, 'w') as outfile:
            dump(self.central_points_features, outfile)
        outfile.close()
        return self.central_points_features

    def __init__(self, path):
        self.central_points_features = None
        self.feature_collection = None
        self.taxizone_geojson = None
        self.datamutex: Lock() = Lock()
        self.centrals: List[Tuple[float, float]] = []
        self.borderline_sizes: List[float] = []
        tz = read_taxizone.TaxiZone('/home/benjamin-elias/PycharmProjects/Proseminar '
                                    'Jupyter-Leafmap/taxi_data/taxi+_zone_lookup.csv')
        self.neighbourhoodTuples: List[Tuple[int, str, str, str]] = []
        # multiple neighborhood polynoms for every taxi zone
        self.neighbourhoodPolynoms: List[List[List[Tuple[float, float]]]] = []
        in_file = open(path, 'r')
        tmp_list = json.loads(in_file.read())
        in_file.close()
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

        self.to_geojson('/home/benjamin-elias/PycharmProjects/Proseminar Jupyter-Leafmap/taxi_zones.geojson')
