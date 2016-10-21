import psycopg2
import json

from geojson import Feature, FeatureCollection, loads

connection = psycopg2.connect(database='postgres', user='postgres', password='postgres',
                              port='5432', host='localhost')
cursor = connection.cursor()


def get_shelters() -> object:
    cursor.execute("""\
SELECT name, ST_AsGeoJSON(way) AS geometry
FROM planet_osm_point
WHERE tourism LIKE 'wilderness_hut';""")
    features = []  # type: list

    for row in cursor.fetchall():
        features.append(Feature(properties={'title': row[0]},
                                geometry=loads(row[1])))

    return FeatureCollection(features)


def get_nearby(lat, lng, radius) -> object:
    cursor.execute("""\
    SELECT name, ST_Distance(ST_SetSRID(ST_MakePoint({}, {}), 4326)::geography, way::geography) as distance,
                  ST_AsGeoJSON(way) as geometry, ST_Length(way::geography) as length, tracktype
     FROM planet_osm_line
     WHERE ST_DWithin(ST_SetSRID(ST_MakePoint({}, {}), 4326)::geography, way::geography, {})
     AND ST_Length(way:: GEOGRAPHY) >= 510
     AND planet_osm_line.route = 'hiking'
     ORDER BY distance
    """.format(lng, lat, lng, lat, radius/10))
    features = []  # type: list

    for row in cursor.fetchall():
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