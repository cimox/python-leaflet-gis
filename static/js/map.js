/**
 * Created by cimo on 16/10/2016.
 */

$(function () {
    // constants
    var DEFAULT_TRACK_HEIGHT = 4.5, DEFAULT_TRACK_OPACITY = 0.75, DEFAULT_TRACK_COLOR = '#e57373';
    var CLICK_TRACK_HEIGHT = 7, CLICK_TRACK_OPACITY = 1, CLICK_TRACK_COLOR = '#ef5350';

    var map, marker, markerRadius;
    var initPosition = [48.7392252, 18.9908871];
    initMap = function () {
        console.log('Map is ready.');
        map = L.map('map-view', {
            center: initPosition,
            zoom: 11
        });

        L.tileLayer(
            'https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2ltb3giLCJhIjoiY2lnMmR5cTViMDBxanZza2hnMW52bnE4cCJ9.69Gz4ubptFwygdY_zA7c3Q'
        ).addTo(map);

        marker = L.marker(initPosition, {draggable: true})
            .addTo(map).bindPopup('Drag me around');

        markerRadius = L.circle(initPosition, 2500)
            .addTo(map);
        marker.on('drag', function (event) {
            markerRadius.setLatLng(marker.getLatLng());
        });

        map.on('locationfound', onLocationFound);
        map.on('locationerror', onLocationError);

        return map;
    };

    updateMarker = function (radius) {
        markerRadius.setRadius(radius);
    };

    var elemLocation = null;
    locate = function (e) {
        elemLocation = e;
        elemLocation.find('i').text('loop');
        elemLocation.toggleClass('enabled disabled');
        map.locate({setView: true, maxZoom: 16});
    };

    function onLocationFound(e) {
        var radius = e.accuracy / 2;

        L.marker(e.latlng).addTo(map)
            .bindPopup("You're within " + radius + " meters from this point").openPopup();
        L.circle(e.latlng, radius).addTo(map);

        if (elemLocation != null) {
            elemLocation.find('i').text('done');
            elemLocation.toggleClass('enabled disabled');
        }
    }

    function onLocationError(e) {
        alert("Couldn't get your location!");
    }

    getShelters = function (map) {
        console.log('Loading shelters');

        var geoJsonMarker = function (title) {
            var LeafIcon = L.Icon.extend({
                iconSize: [25, 25],
                iconAnchor: [25, 25],
                popupAnchor: [25, 25]
            });
            if (title == null) return new LeafIcon({iconUrl: '../static/img/hut-icon-grey.png'});
            else return new LeafIcon({iconUrl: '../static/img/hut-icon.png'});
        };

        L.icon = function (options) {
            return new L.Icon(options);
        };

        $.getJSON('/shelters/', function (geojson) {
            sheltersLayer = L.geoJson(geojson, {
                pointToLayer: function (feature, latlng) {
                    hutIcon = geoJsonMarker(feature.properties.title);
                    return L.marker(latlng, {icon: hutIcon});
                },
                onEachFeature: function (feature, layer) {
                    layer.bindPopup(feature.properties.title || 'Unknown');
                }
            });
            sheltersLayer.addTo(map);

            return sheltersLayer;
        });
    };

    var nearbyTracksLayer = null;
    var springsLayer = null;
    findNearby = function (radius) {
        console.log('Tracks nearby you in radius: ' + radius);
        if (nearbyTracksLayer != null) map.removeLayer(nearbyTracksLayer);
        if (springsLayer != null) map.removeLayer(springsLayer);

        $.getJSON('/nearby/' + marker.getLatLng().lat + '/' + marker.getLatLng().lng + '/' + radius + '/',
            function (geojson) {
                console.log(geojson);
                nearbyTracksLayer = L.geoJson(geojson, {
                    onEachFeature: function (feature, layer) {
                        var title = feature.properties.title || 'Unknown name';
                        layer.setStyle({
                            color: DEFAULT_TRACK_COLOR,
                            opacity: DEFAULT_TRACK_OPACITY,
                            weight: DEFAULT_TRACK_HEIGHT
                        });
                        layer.bindPopup(title + ' | Length ' + feature.properties.length / 1000 + 'km'
                            + ' | ' + feature.properties.distance / 1000 + 'km from you');

                        layer.on('click', function (event) {
                            layer.setStyle({
                                color: CLICK_TRACK_COLOR,
                                opacity: CLICK_TRACK_OPACITY,
                                weight: CLICK_TRACK_HEIGHT
                            });
                        });

                        layer.on('popupclose', function () {
                            layer.setStyle({
                                color: DEFAULT_TRACK_COLOR,
                                opacity: DEFAULT_TRACK_OPACITY,
                                weight: DEFAULT_TRACK_HEIGHT
                            });
                        });
                    }
                });
                nearbyTracksLayer.addTo(map);

                return nearbyTracksLayer;
            });
    };

    findNearbyCity = function (radius) {
        console.log('Finding track nearby city in radius: ' + radius);
        if (nearbyTracksLayer != null) map.removeLayer(nearbyTracksLayer);
        if (springsLayer != null) map.removeLayer(springsLayer);

        $.getJSON('/nearby-city/' + radius + '/' + marker.getLatLng().lat + '/' + marker.getLatLng().lng + '/',
            function (geojson) {
                nearbyTracksLayer = L.geoJson(geojson, {
                    onEachFeature: function (feature, layer) {
                        var title = feature.properties.title || 'Unknown track name';
                        layer.setStyle({
                            color: DEFAULT_TRACK_COLOR,
                            opacity: DEFAULT_TRACK_OPACITY,
                            weight: DEFAULT_TRACK_HEIGHT
                        });
                        layer.bindPopup(title + ' | ' + feature.properties.length / 1000 + 'km' +
                            ' | Near to city: ' + feature.properties.city);

                        layer.on('click', function (event) {
                            layer.setStyle({
                                color: CLICK_TRACK_COLOR,
                                opacity: CLICK_TRACK_OPACITY,
                                weight: CLICK_TRACK_HEIGHT
                            });
                        });

                        layer.on('popupclose', function () {
                            layer.setStyle({
                                color: DEFAULT_TRACK_COLOR,
                                opacity: DEFAULT_TRACK_OPACITY,
                                weight: DEFAULT_TRACK_HEIGHT
                            });
                        });
                    }
                });
                nearbyTracksLayer.addTo(map);

                return nearbyTracksLayer;
            });
    };

    findSpringOnWay = function (radius) {
        console.log('Tracks with springs on the way in radius: ' + radius);
        if (nearbyTracksLayer != null) map.removeLayer(nearbyTracksLayer);
        if (springsLayer != null) map.removeLayer(springsLayer); // TODO: fix this, it doesn't remove old layer

        // add tracks
        $.getJSON('/spring-onway/' + radius + '/' + marker.getLatLng().lat + '/' + marker.getLatLng().lng + '/500/',
            function (geojson) {
                nearbyTracksLayer = L.geoJson(geojson['tracks'], {
                    onEachFeature: function (feature, layer) {
                        var title = feature.properties.title || 'Unknown track name';
                        layer.setStyle({
                            color: DEFAULT_TRACK_COLOR,
                            opacity: DEFAULT_TRACK_OPACITY,
                            weight: DEFAULT_TRACK_HEIGHT
                        });
                        layer.bindPopup(title + ' | ' + feature.properties.length / 1000 + 'km');

                        layer.on('click', function (event) {
                            layer.setStyle({
                                color: CLICK_TRACK_COLOR,
                                opacity: CLICK_TRACK_OPACITY,
                                weight: CLICK_TRACK_HEIGHT
                            });
                        });

                        layer.on('popupclose', function () {
                            layer.setStyle({
                                color: DEFAULT_TRACK_COLOR,
                                opacity: DEFAULT_TRACK_OPACITY,
                                weight: DEFAULT_TRACK_HEIGHT
                            });
                        });
                    }
                });
                nearbyTracksLayer.addTo(map);

                var geoJsonMarker = function (title) {
                    var LeafIcon = L.Icon.extend({
                        iconSize: [25, 25],
                        iconAnchor: [25, 25],
                        popupAnchor: [25, 25]
                    });
                    if (title == null) return new LeafIcon({iconUrl: '../static/img/spring-icon-grey.png'});
                    else return new LeafIcon({iconUrl: '../static/img/spring-icon.png'});
                };

                L.icon = function (options) {
                    return new L.Icon(options);
                };
                springsLayer = L.geoJson(geojson['springs'], {
                    pointToLayer: function (feature, latlng) {
                        hutIcon = geoJsonMarker(feature.properties.title);
                        return L.marker(latlng, {icon: hutIcon});
                    }
                    ,
                    onEachFeature: function (feature, layer) {
                        layer.bindPopup(feature.properties.title || 'Unknown');
                    }
                });
                springsLayer.addTo(map);
            });
    };
});