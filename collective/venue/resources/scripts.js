/* jslint browser: true */
/* global jQuery, common_content_filter, initialize_map */

(function($) {
  "use strict";

  $(document).ready(function() {

    // Open location view in popup.
    if (common_content_filter !== undefined && $('body').prepOverlay !== undefined) {
      var overlay_opts = {
        subtype: 'ajax',
        filter: common_content_filter,
        cssclass: 'overlay-venue',
        config: {
          onLoad: window.plone_formwidget_geolocation__initialize_map
        }
      };
      $('a.venue_ref_popup').prepOverlay(overlay_opts);
    }
  });

}(jQuery));

