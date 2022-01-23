import geojson
import csv

PASSENGER = 3
TRIP = 4
RATECODEID = 5
PICKUP = 7
DROPOFF = 8
PAYMENT = 9
FAREAMOUNT = 10
EXTRA = 11
MTA_TAX = 12
TIP = 13
TOLLS = 14
IMPROVEMENT_SURCHARGE = 15
TOTAL_AMOUNT = 16
CONGESTION_SURCHARGE = 17


# give a FeatureCollection with LineStrings and their properties to build a Heatmap with the method as data to show
# and a reference if that should be projected into the pickup location or dropoff location
class Heatmapper:
    def __init__(self, path_in_geojson_con, path_csv_out, method=PICKUP, reference=PICKUP):
        self.loaded_connections = None
        with open(path_in_geojson_con, 'r') as in_file:
            self.loaded_connections = geojson.load(in_file)
            in_file.close()
        pass
        out_dict = {}
        for f in self.loaded_connections['features']:
            val = f['properties']['data'][method]
            if method == PICKUP or method == DROPOFF:
                if not (val in out_dict.keys()):
                    out_dict[val] = 0
                out_dict[val] += 1
            else:
                if not (reference in out_dict.keys()):
                    out_dict[reference] = [val, 1]
                out_dict[reference][0] += val
                out_dict[reference][1] += 1

        if not (method == PICKUP or method == DROPOFF):
            for it_key, it_val in out_dict.items():
                out_dict[it_key] = it_val[0] / it_val[1]

        # from out_dict we now have the output values for every key that is usually the PICKUP location
        self.to_csv = [['Zone', 'Borough', 'latitude', 'longitude', 'heat_property_val']]
        for it_key, it_val in out_dict.items():
            data_dict = None
            for f in self.loaded_connections['features']:
                if reference == PICKUP:
                    if f['properties']['start']['LocationID'] == it_key:
                        data_dict = f['properties']['start']
                        break
                else:
                    if f['properties']['end']['LocationID'] == it_key:
                        data_dict = f['properties']['end']
                        break
            # from the data_dict we get Zone, Borough, latitude, longitude and add the it_val to the end
            self.to_csv.append([data_dict['Zone'], data_dict['Borough'], data_dict['center'][0], data_dict['center'][1],
                                it_val])

        with open(path_csv_out, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(self.to_csv)
            outfile.close()
