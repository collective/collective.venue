/*jslint browser: true*/
/*global $, jQuery, L, common_content_filter*/

function initialize_map() {
    // Initialize the map
    var editable,
        map,
        baseLayers,
        fullScreen,
        markers,
        bounds,
        update_inputs,
        geosearch;

    if ($('#map').length === 0) {
        return;
    }

    editable = ($('div.geolocation_wrapper.edit').length && true) || false;

    map = new L.Map("map", {});

    L.tileLayer.provider('OpenStreetMap.DE').addTo(map);
    baseLayers = ['OpenStreetMap.DE', 'Esri.WorldImagery', 'Esri.WorldStreetMap', 'OpenCycleMap'];
    L.control.layers.provided(baseLayers).addTo(map);

    fullScreen = new L.Control.FullScreen();
    map.addControl(fullScreen);

    // ADD MARKERS
    markers = new L.MarkerClusterGroup();
    $('div.geolocation').each(function() {
        var geo, marker;
        geo = $(this).data();
        marker = new L.Marker([geo.latitude, geo.longitude], {
            draggable: editable
        });
        marker.bindPopup(geo.description);
        if (editable) {
            marker.on('dragend', function(e) {
                var coords = e.target.getLatLng();
                update_inputs(coords.lat, coords.lng);
            });
        }
        markers.addLayer(marker);
    });
    map.addLayer(markers);

    // autozoom
    bounds = markers.getBounds();
    map.fitBounds(bounds);

    if (editable) {
        update_inputs = function(lat, lng) {
            var map_wrap = $('#map').closest('div.geolocation_wrapper.edit');
            map_wrap.find('input.latitude').attr('value', lat);
            map_wrap.find('input.longitude').attr('value', lng);
        };
        map.on('geosearch_showlocation', function(e) {
            var coords = e.Location;
            update_inputs(coords.Y, coords.X);
        });

        // GEOSEARCH
        geosearch = new L.Control.GeoSearch({
            draggable: editable,
            provider: new L.GeoSearch.Provider.Google()
            //provider: new L.GeoSearch.Provider.OpenStreetMap()
        });
        geosearch.addTo(map);
    }

}


(function($) {

    $(document).ready(function() {
        initialize_map();
        // Open location view in popup.
        if (common_content_filter !== undefined && $('body').prepOverlay !== undefined) {
            var overlay_opts = {
                subtype: 'ajax',
                filter: common_content_filter,
                cssclass: 'overlay-venue',
                config: {
                    onLoad: initialize_map
                }
            };
            $('a.venue_ref_popup').prepOverlay(overlay_opts);
        }
    });

}(jQuery));
