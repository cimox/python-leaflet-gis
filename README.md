# Matus Cimerman
## Faculty of informatics and information technologies
##### Slovak university of technology in Bratislava, Advanced database technologies

### My project
School coursework. GIS web app for finding tourist tracks and areas of interest. Using Postgis DB, Python Flask as webserver in backend and Leaflet for frontend, e.g. map.

##### Application description
Web and mobile application where you can find hiking tracks nearby your current position. Or you can drag-and-drop pointer and find tracks somewhere else on the map. You can show all hiking shelters in Slovakia. You can find tracks going nearby city which is in your radius. You can find tracks with water source in the way. All the searched tracks are fetched within radius (can be adjusted) within your current position.

Data queried from DB are returned as geojson using Postgis function _ST_AsGeojson_. If returned data is not a single geojson record, its need to be transformed to geojson _FeatureCollection_, this is done on backend. Through api then application frontend can request desired data, e.g. _FeatureCollection_ of all hiking shelters in Slovakia.

##### Functions overview
- [x] find all shelters
- [x] find nearby hiking tracks in selected radius
- [x] find hiking tracks going near to any city on the way
- [x] find hiking tracks with water source on the way

##### Data source and DB
- Map: openstreemap.org, exported whole Slovakia from geofabrik.de
- Loading data to Postgres (with Postgis extension) has been done using _osm2pgsql_, command: `osm2pgsql slovakia-latest.osm.bz2 -U postgres -d postgres -P 5432 -W -H localhost -l -s`. 
- All necessary columns used to query data are indexed.

##### Technologies
- Web server: python Flask micro webframework,
- DB: Postgres with Postgis extension,
- Map visualization: Leaflet.js with Mapbox tiles (+ jQuery and Materialize for UI).

##### App screenshot
![App screenshot](http://oi63.tinypic.com/2mzhu1.jpg)
