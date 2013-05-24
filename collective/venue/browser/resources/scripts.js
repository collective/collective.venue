(function($) {

    function initialize_map() {
        // Initialize the map

        if ($('#map').length === 0) { return; }

        var editable = $('div.geolocation_wrapper.edit').length && true || false;

        var map = new L.Map("map", {});

        L.tileLayer.provider('OpenStreetMap.DE').addTo(map);
        var baseLayers = ['OpenStreetMap.DE', 'Esri.WorldImagery', 'Esri.WorldStreetMap', 'OpenCycleMap'];
        var layerControl = L.control.layers.provided(baseLayers).addTo(map);

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
                provider: new L.GeoSearch.Provider.Google()
                //provider: new L.GeoSearch.Provider.OpenStreetMap()
            }).addTo(map);
        }

    }

    $(document).ready(function () {
        initialize_map();
        // Open location view in popup.
        $('.template-event_view td.location a').prepOverlay({
            subtype: 'ajax',
            filter: common_content_filter,
            cssclass: 'overlay-venue',
            config: { onLoad: initialize_map }
        });
    });

})(jQuery);
