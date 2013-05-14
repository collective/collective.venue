$(document).ready(function () {

    if ($('#map').length === 0) { return; }

    var editable = $('div.geolocation_wrapper.edit').length && true || false;
    
    var map = new L.Map("map", {});
    
    // add an OpenStreetMap tile layer
    var layer = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    });
    map.addLayer(layer);

    var fullScreen = new L.Control.FullScreen();
    map.addControl(fullScreen);

    // ADD MARKERS
    var markers = new L.MarkerClusterGroup();
    $('div.geolocation').each(function() {
        var geo = $(this).data();
        var marker = new L.Marker([geo.latitude, geo.longitude],
                              {draggable: editable});
        marker.bindPopup(geo.description);
        if (editable) {
            marker.on('dragend', function (e) {
                var coords = e.target.getLatLng();
                update_inputs(coords.lat, coords.lng);
            });
        }
        markers.addLayer(marker);
    });
    map.addLayer(markers);

    // autozoom
    var bounds = markers.getBounds();
    map.fitBounds(bounds);

    if (editable) {
        var update_inputs = function(lat, lng) {
            var map_wrap = $('#map').closest('div.geolocation_wrapper.edit');
            map_wrap.find('input.latitude').attr('value', lat);
            map_wrap.find('input.longitude').attr('value', lng);
        }
        map.on('geosearch_showlocation', function (e) {
            var coords = e.Location;
            update_inputs(coords.Y, coords.X);
        });

        // GEOSEARCH
        var geosearch = new L.Control.GeoSearch({
            draggable: editable,
            provider: new L.GeoSearch.Provider.OpenStreetMap()
        }).addTo(map);
    }

});
