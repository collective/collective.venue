/*
$(document).ready(function() {
  function createCheckbox(category) {
    return $(
      '<div class="checkbox"><label><input type="checkbox" value="' + category + '" name="' + category + '" checked>' +
      category +
      "</label></div>",
    );
  }

  function changeIconsColor() {
    $('.leaflet-map .awesome-marker').removeClass('awesome-marker-icon-green').addClass('awesome-marker-icon-red');
  }

  function toggleLoading() {
    $('.leaflet-wrapper').toggleClass('loading');
  }

  function destroyMap() {
    $('.leaflet-map').remove();
  }

  function createMap() {
    if ($('.leaflet-map').length === 0) {
      $('.leaflet-wrapper').prepend('<div class="leaflet-map"></div>');
      $('.leaflet-map').attr('data-geojson', window.localStorage.getItem('geoJson'));
    }
    else if ([undefined, ''].indexOf($('.leaflet-map').attr('data-geojson')) > -1) {
      $('.leaflet-map').attr('data-geojson', window.localStorage.getItem('geoJson'));
    }
  }

  function initMap() {
    createMap();

    try {
      console.log('start: init map without errors');
      new Leaflet($('.leaflet-map'));
      console.log('start: init map without errors');
    }
    catch (e) {
      if (e.message === 'Map container is already initialized.' || e.message === 'L.Control.Fullscreen is not a constructor') {
        destroyMap();
        createMap();
      }

      setTimeout(function() {
        console.log('start: init map after error');
        new Leaflet($('.leaflet-map'));
        console.log('end: init map after error');
      }, 200);
    }

    changeIconsColor();
  }

  $('body').append(
    '<style> .leaflet-map { height: 400px; } .leaflet-map.empty-map .leaflet-objects-pane { display: none; } </style>'
  );

  toggleLoading();
  var geoJson = JSON.parse($('.leaflet-map').attr('data-geojson'));
  var geoJsonAll = JSON.parse($('.leaflet-map').attr('data-geojson'));
  window.localStorage.setItem('geoJson', JSON.stringify(geoJson));
  window.localStorage.setItem('geoJsonAll', JSON.stringify(geoJsonAll));

  var categories = new Set();
  geoJson.features.forEach(function(feature) {
    feature.properties.categories.forEach(function(cat) {
      categories.add(cat);
    });
  });

  categories.forEach(function(cat) {
    $('.leaflet-filters').append(createCheckbox(cat));
  });

  initMap();
  toggleLoading();

  $('.leaflet-filters').on('change', function(e) {
    var isEmpty = false;
    toggleLoading();

    var activeCategories = $.grep(
      $('.leaflet-filters input[type="checkbox"]'),
      function(i) {
        return i.checked;
      },
    ).map(function(el) {
      return el.name;
    });

    if (!geoJsonAll) {
      geoJsonAll = JSON.parse(window.localStorage.getItem('geoJsonAll'));
    }
    if (!geoJson) {
      geoJson = JSON.parse(window.localStorage.getItem('geoJson'));
    }

    var features = geoJsonAll.features.filter(function(feature) {
      var hasActiveCategories = false;
      feature.properties.categories.forEach(function(cat) {
        if (activeCategories.indexOf(cat) > -1) {
          hasActiveCategories = true;
        }
      });

      return hasActiveCategories;
    })

    if (features.length > 0) {
      geoJson.features = features;
    }
    else {
      isEmpty = true;
      geoJson.features = [{
        'type': 'Feature',
        'id': 'empty',
        'properties': {'categories': 'empty'},
        'geometry': {
          'type': 'Point',
          'coordinates': [
            11.36337,
            44.50861,
          ]
        }
      }];
    }

    window.localStorage.setItem('geoJson', JSON.stringify(geoJson));

    destroyMap();
    createMap();

    if (isEmpty) {
      $('.leaflet-map').addClass('empty-map');
    }

    initMap();

    toggleLoading();
  });
});
*/

$(function() {
  var geoJson = JSON.parse(document.querySelector('.leaflet-map').getAttribute('data-geojson'));
  var categoriesLayers = {};

  geoJson.features.forEach(function(feature) {
    var coordinates = feature.geometry.coordinates;
    var popupContent = feature.properties.popup;
    var marker = L.marker(coordinates).bindPopup(popupContent);

    feature.properties.categories.forEach(function(cat) {
      if (!categoriesLayers[cat]) {
        categoriesLayers[cat] = L.layerGroup();
      }

      marker.addTo(categoriesLayers[cat]);
    });
  });

  var tileLayer = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  });

  var layers = [tileLayer];
  for (var cat in categoriesLayers) {
    layers.push(categoriesLayers[cat]);
  }

  var map = L.map(document.querySelector('.leaflet-map'), {
    center: [],
    zoom: 13,
    layers: layers,
  });

  L.control.layers({'OpenStreetMap': tileLayer}, categoriesLayers).addTo(map);
});
