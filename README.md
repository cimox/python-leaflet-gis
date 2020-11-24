# Matus Cimerman
## Faculty of informatics and information technologies
##### Slovak university of technology in Bratislava, Advanced database technologies

### My project
School coursework. GIS web app for finding tourist tracks and areas of interest. Using Postgis DB, Python Flask as webserver in backend and Leaflet for frontend, e.g. map.

#### Application description
Web and mobile application where you can find hiking tracks nearby your current position. Or you can drag-and-drop pointer and find tracks somewhere else on the map. You can show all hiking shelters in Slovakia. You can find tracks going nearby city which is in your radius. You can find tracks with water source in the way. All the searched tracks are fetched within radius (can be adjusted) within your current position.

Data queried from DB are returned as geojson using Postgis function _ST_AsGeojson_. If returned data is not a single geojson record, it needs to be transformed to geojson _FeatureCollection_, this is done on backend. Application frontend can then through api request desired data, e.g. _FeatureCollection_ of all hiking shelters in Slovakia. Response (e.g. geojson _FeatureCollection_) from api route is then visualized on map using _Leaflet.js_ methods.

#### Functions overview
- [x] find all shelters
- [x] find nearby hiking tracks in selected radius
- [x] find hiking tracks going near to any city on the way
- [x] find hiking tracks with water source on the way

#### Installation instructions
1. Download latest slovakia OSM bz2 file from https://download.geofabrik.de/europe/slovakia.html
1. Install Postgres 11+ and Postgis extension.
1. Load downloaded slovakia data into the DB by running `osm2pgsql slovakia-latest.osm.bz2 -U postgres -d postgres -P 5432 -W -H localhost -l -s`
1. Create python virtual env, activate and install requirements `pip install -r requirements.txt`
1. Start the application `python app.py`
1. Visit website GUI: http://0.0.0.0:5000/ (see screenshots below)

##### Data source and DB
- Map: openstreemap.org, exported whole Slovakia from geofabrik.de
- Loading data to Postgres (with Postgis extension) has been done using _osm2pgsql_, command: `osm2pgsql slovakia-latest.osm.bz2 -U postgres -d postgres -P 5432 -W -H localhost -l -s`. 
- All necessary columns used to query data are indexed.

##### Technologies
- Web server: python Flask micro webframework,
- DB: Postgres with Postgis extension,
- Map visualization: Leaflet.js with Mapbox tiles (+ jQuery and Materialize for UI).

##### App screenshot

