import psycopg2
import json


connection = psycopg2.connect(database='postgres', user='postgres', password='postgres',
                              port='32770', host='localhost')
cursor = connection.cursor()

def get_shelters() -> dict:
    cursor.execute("""\
SELECT name, ST_AsGeoJSON(way) AS geometry
FROM planet_osm_point
WHERE tourism LIKE 'wilderness_hut';""")
    result = {} # type: dict

    for row in cursor.fetchall():
        result[row[0]] = json.loads(row[1])

    return result