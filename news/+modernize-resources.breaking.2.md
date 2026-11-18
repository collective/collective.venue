registry: Register the webpack bundle and the Venue icon.
Register the webpack bundle and the CSS file instead of the Plone 5
resources and the compiled RequireJS/LESS bundle. Register a
`plone.icon.contenttype/venue` icon. Add an upgrade step, which removes
the obsolete resource and bundle registry records.
@thet
