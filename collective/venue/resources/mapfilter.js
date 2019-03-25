define([
    'jquery',
    'pat-base',
], function($, Base) {
    'use strict';

    var LocationSearch = Base.extend({
        name: 'collective-venue-mapfilter',
        trigger: '.pat-venue-mapfilter',
        parser: 'mockup',

        init: function() {

            this.$el.on('leaflet.moveend leaflet.zoomend', function (e) {

                  $(this.trigger).trigger(
                      'collectionfilter:reload',
                      {
                          collectionUUID: this.options.collectionUUID,
                          targetFilterURL: collectionURL,
                          noReloadSearch: true
                      }
                  );
            
            });

        }

    });

    return LocationSearch;

});
