$(function() {
  var geoJson = JSON.parse(document.querySelector('.collection-leaflet-map').getAttribute('data-geojson'));
  var categoriesLayers = {};

  var map = L.map(document.querySelector('.collection-leaflet-map'), {
    fullscreenControl: true,
    zoomControl: true,
    sleep: false,
    sleepNote: false,
    hoverToWake: false,
    sleepOpacity: 1
  });

  var tileLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  var markerCluster = new L.MarkerClusterGroup();
  var markerLayer = L.geoJson(geoJson, {
    pointToLayer: function(feature, latlng) {
      var marker = L.marker(latlng, {
        icon: L.AwesomeMarkers.icon({
          markerColor: 'red',
          prefix: 'fa',
          icon: 'circle',
        }),
        draggable: false,
      }).bindPopup(feature.properties.popup).addTo(map);

      feature.properties.categories.forEach(function(cat) {
        if (!categoriesLayers[cat]) {
          categoriesLayers[cat] = L.layerGroup();
        }

        marker.addTo(categoriesLayers[cat]);
      });

      return marker;
    },
  });

  for (var cat in categoriesLayers) {
    map.addLayer(categoriesLayers[cat]);
  }

  markerCluster.addLayer(markerLayer);
  map.fitBounds(markerCluster.getBounds());

  if (Object.values(categoriesLayers).length > 0) {
    L.control.layers({}, categoriesLayers, { collapsed: false }).addTo(map);
  }
});
