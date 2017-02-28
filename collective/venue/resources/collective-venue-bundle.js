require([
  'pat-registry',
  'collective-venue'
], function(registry) {
  'use strict';

  // initialize only if we are in top frame
  if (window.parent === window) {
    $(document).ready(function() {
      if (!registry.initialized) {
        registry.init();
      }
    });
  }

});
