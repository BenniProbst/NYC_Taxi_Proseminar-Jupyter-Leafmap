import geojson

# give a FeatureCollection with LineStrings and their properties to build a Heatmap with
class Heatmapper:
    def __init__(self, path_in_geojson_con):
        self.loaded_connections = None
        with open(path_in_geojson_con, 'r') as in_file:
            self.loaded_connections = geojson.load(in_file)
            in_file.close()

