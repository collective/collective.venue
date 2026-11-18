build: Add a webpack module federation build.
Add a webpack build for the JavaScript resources in `resources/`, like
in other Plone 6 add-ons. The compiled module federation bundle is
written to `src/collective/venue/resources/collective-venue-bundle/` and
shares Patternslib with Plone's main bundle. Add a Jest configuration
for the JavaScript tests.
@thet
