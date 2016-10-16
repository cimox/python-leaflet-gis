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