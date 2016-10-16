/**
 * Created by cimo on 16/10/2016.
 */

initMap = function() {
    var map = L.map('mapid').setView([48.685216, 18.63082], 13);

    L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiY2ltb3giLCJhIjoiY2lnMmR5cTViMDBxanZza2hnMW52bnE4cCJ9.69Gz4ubptFwygdY_zA7c3Q'
    ).addTo(map);
};