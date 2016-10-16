/**
 * Created by cimo on 16/10/2016.
 */

$(function () {
    initMap = function () {
        console.log('Map is ready.');
        var map = L.map('map-view', {
            center: [48.7392252, 18.9908871],
            zoom: 10
        });

        L.tileLayer(
            'https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2ltb3giLCJhIjoiY2lnMmR5cTViMDBxanZza2hnMW52bnE4cCJ9.69Gz4ubptFwygdY_zA7c3Q'
        ).addTo(map);

        return map;
    };

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
                    layer.bindPopup(feature.properties.title || 'Neznámy');
                }
            });
            sheltersLayer.addTo(map);

            return sheltersLayer;
        });
    };

});