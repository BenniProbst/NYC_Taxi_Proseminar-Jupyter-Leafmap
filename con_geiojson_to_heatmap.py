import geojson

# give a FeatureCollection with LineStrings and their properties to build a Heatmap with
class Heatmapper:
    def __init__(self, path):
        tmp_list = None
        with open(path, 'r') as in_file:
            tmp_list = geojson.load(in_file)
            in_file.close()

