import pyproj
from shapely.ops import transform
from shapely.geometry import Point, LineString

class GeometryHelper:

    @staticmethod
    def get_distance(obj_one, obj_two):
        """
        Return distance in meters between linestring and a position/bearing tuplet
        """
        obj_one_95 = GeometryHelper.__wgs84ToLv95(obj_one)
        obj_two_95 = GeometryHelper.__wgs84ToLv95(obj_two)
        return obj_one_95.distance(obj_two_95)

    # according to https://gis.stackexchange.com/a/127432
    def __wgs84ToLv95(old):
        project = lambda x, y: pyproj.transform(pyproj.Proj(init='epsg:4326'), pyproj.Proj(init='epsg:2056'), x, y)
        return transform(project,old)


