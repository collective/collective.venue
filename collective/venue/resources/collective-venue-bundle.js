require(["pat-registry", "pat-leaflet", "collective-venue"], function(
  registry,
  Leaflet,
) {
  "use strict";

  // initialize only if we are in top frame
  if (window.parent === window) {
    $(document).ready(function() {
      if (!registry.initialized) {
        registry.init();
      }
    });
  }
})
