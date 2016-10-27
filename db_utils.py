import psycopg2
import json

from geojson import Feature, FeatureCollection, loads


class Postis(object):
    def __init__(self, user, passw, port, host):
        self.connection = psycopg2.connect(database='postgres', user=user, password=passw, port=port, host=host)
        self.cursor = self.connection.cursor()

    def get_shelters(self) -> FeatureCollection:
        """
        Finds all shelters
        :rtype: FeatureCollection
        :return: shelters with names (title)
        """
        self.cursor.execute(""
                            "        SELECT name, ST_AsGeoJSON(way) AS geometry\n"
                            "        FROM planet_osm_point\n"
                            "        WHERE tourism LIKE 'wilderness_hut';")
        features = []  # type: list

        for row in self.cursor.fetchall():
            features.append(Feature(properties={'title': row[0]},
                                    geometry=loads(row[1])))

        return FeatureCollection(features)

    def get_nearby(self, lat: float, lng: float, radius: int) -> FeatureCollection:
        """
        Return hiking tracks nearby [lat, lng] point within defined radius
        :rtype: FeatureCollection
        :param lat: latitude of desired point
        :param lng: longitude of desired point
        :param radius: within which hiking tracks will be found
        :return: geojson standard FeatureCollection with geometry of track, title, distance from [lat, lng] and length of track
        """
        self.cursor.execute((""
                             "        SELECT name, ST_Distance(ST_SetSRID(ST_MakePoint({}, {}), 4326)::geography, way::geography) as distance,\n"
                             "                      ST_AsGeoJSON(way) as geometry, ST_Length(way::geography) as length, tracktype\n"
                             "         FROM planet_osm_line\n"
                             "         WHERE ST_DWithin(ST_SetSRID(ST_MakePoint({}, {}), 4326)::geography, way::geography, {})\n"
                             "         AND ST_Length(way:: GEOGRAPHY) >= 510\n"
                             "         AND planet_osm_line.route = 'hiking'\n"
                             "         ORDER BY distance\n"
                             # "         LIMIT 25"
                             "        ").format(lng, lat, lng, lat, radius))
        features = []  # type: list

        for row in self.cursor.fetchall():
            features.append(Feature(
                properties={
                    'title': row[0],
                    'distance': row[1],
                    'length': int(row[3])
                },
                geometry=loads(row[2])
            )
            )

        return FeatureCollection(features)

    def get_nearby_city(self, radius) -> FeatureCollection:
        self.cursor.execute((
            "SELECT line.name, st_asgeojson(line.way) AS geometry, point.name FROM planet_osm_line line JOIN planet_osm_point point ON st_dwithin(point.way :: GEOGRAPHY, line.way :: GEOGRAPHY, {}) = TRUE WHERE line.route = 'hiking' AND st_length(line.way :: GEOGRAPHY) >= 2500 AND ( point.place = 'city' OR point.place = 'town' ) AND line.name IS NOT NULL").format(
            radius))
        features = []  # type: list

        for row in self.cursor.fetchall():
            features.append(Feature(
                properties={
                    'title': row[0],
                    'city': row[2]
                },
                geometry=loads(row[1])
            ))
        return FeatureCollection(features)
