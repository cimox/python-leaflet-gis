# Matus cimerman
#### Faculty of informatics and information technologies
###### Slovak university of technology in Bratislava
###### Advanced database technologies

### My project
School coursework. GIS web app for finding tourist tracks and areas of interest. Using Postgis DB, Python Flask as webserver in backend and Leaflet for frontend, e.g. map.

##### Application description
Web and mobile application where you can find hiking tracks nearby your current position. Or you can drag-and-drop pointer and find tracks somewhere else on the map. You can show all hiking shelters in Slovakia. You can find tracks going nearby city which is in your radius. You can find tracks with water source in the way. All the searched tracks are fetched within radius (can be adjusted) within your current position.

##### Functions overview
- [x] find all shelters
- [x] find nearby hiking tracks in selected radius
- [x] find hiking tracks going near to any city on the way
- [x] find hiking tracks with water source on the way

##### Data source 
- Map: openstreemap.org, exported whole Slovakia
I've used _osm2pgsql_ to import data to Postgis DB. So, as a DB is used Postgres DB with Postigs extension. All necessary columns used to query data are indexed.

##### Technologies
- Web server: python Flask, simple micro webframework
- Map: Leaflet with Mapbox tiles
- DB: Postgres with Postgis extension
Data queried from DB are afterwards transformed to geojson format. Geojson format is then used to show lines/points on map using Leaflet.js

##### App screenshot
![App screenshot](http://oi63.tinypic.com/2mzhu1.jpg)