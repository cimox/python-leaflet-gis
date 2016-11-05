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
                             "SELECT name, ST_Distance(ST_SetSRID(ST_MakePoint({}, {}), 4326)::geography, way::geography) as distance,\n"
                             "ST_AsGeoJSON(way) as geometry, ST_Length(way::geography) as length, tracktype\n"
                             "FROM planet_osm_line\n"
                             "WHERE ST_DWithin(ST_SetSRID(ST_MakePoint({}, {}), 4326)::geography, way::geography, {})\n"
                             "AND ST_Length(way:: GEOGRAPHY) >= 510\n"
                             "AND planet_osm_line.route = 'hiking'\n"
                             "ORDER BY distance\n"
                             "").format(lng, lat, lng, lat, radius))
        features = []  # type: list

        for row in self.cursor.fetchall():
            features.append(Feature(
                properties={
                    'title': row[0],
                    'distance': int(row[1]),
                    'length': int(row[3])
                },
                geometry=loads(row[2])
            )
            )

        return FeatureCollection(features)

    def get_nearby_city(self, position: dict, radius: int, min_length=2500) -> FeatureCollection:
        """
        Returns hiking tracks going nearby city which is closest to position.
        :param position: lat, lng of current position
        :param min_length: minimal length of tracks to find in meters
        :param radius: radius in meters
        :return: geojson FeatureCollection with tracks nearby city
        """
        self.cursor.execute((
            "SELECT line.name, st_asgeojson(line.way) AS geometry, point.name, ST_Length(line.way::geography) as length"
            " FROM planet_osm_line line "
            "JOIN planet_osm_point point ON st_dwithin(point.way :: GEOGRAPHY, line.way :: GEOGRAPHY, {}) = TRUE "
            "WHERE line.route = 'hiking' "
            "AND point.way = "
            "  (SELECT way FROM (SELECT p.way, st_distance(st_setsrid(st_makepoint({}, {}), 4326), p.way :: GEOGRAPHY ) "
            "  AS dist FROM planet_osm_point p "
            "  WHERE p.place = 'city' OR p.place = 'town' ORDER BY dist LIMIT 1) AS closest_town) "
            "AND st_length(line.way :: GEOGRAPHY) >= {} "
            "AND ( point.place = 'city' OR point.place = 'town' )  "
            "AND line.name IS NOT NULL").format(radius, position['lng'], position['lat'], min_length))
        features = []  # type: list

        for row in self.cursor.fetchall():
            features.append(Feature(
                properties={
                    'title': row[0],
                    'city': row[2],
                    'length': int(row[3])
                },
                geometry=loads(row[1])
            ))
        return FeatureCollection(features)

    def get_track_with_spring_onway(self, position: dict, radius: int, radius_water: int) -> list:
        """
        Finds hiking tracks with water source on the way.
        :param position: you current position in lng/lat
        :param radius: radius within which you want to find hiking tracks around position
        :param radius_water: how far from found track water source can be
        :return: geojson FeatureCollection with tracks with water source on the way
        """

        self.cursor.execute((
            "SELECT l.name, st_asgeojson(l.way), ST_Length(l.way::geography), p.name, st_asgeojson(p.way) "
            "FROM planet_osm_line l, planet_osm_point p "
            "WHERE l.route = 'hiking' "
            " AND (p.amenity = 'drinking_water' or p.amenity = 'spring')"
            " AND st_dwithin(l.way :: GEOGRAPHY , p.way :: GEOGRAPHY , {})"
            " AND ST_DWithin(ST_SetSRID(ST_MakePoint({}, {}), 4326)::geography, l.way::geography, {})"
            ).format(radius_water, position['lng'], position['lat'], radius))

        features_tracks = []  # type: list
        features_springs = []  # type: list

        for row in self.cursor.fetchall():
            features_tracks.append(Feature(
                properties={
                    'title': row[0],
                    'length': int(row[2])
                },
                geometry=loads(row[1])
            ))
            features_springs.append(Feature(
                properties={
                    'title': row[3]
                },
                geometry=loads(row[4])
            ))

        return [FeatureCollection(features_tracks), FeatureCollection(features_springs)]