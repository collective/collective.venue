locationsearch: Rewrite the location search pattern without jQuery.
Rewrite the location search pattern as a Patternslib `BasePattern`
without jQuery and RequireJS, using `fetch` and a small i18n helper,
which loads the `collective.venue` catalog from `@@plonejsi18n`.
The search button now has a translated label, is disabled while
searching and is only added to forms with address fields.
@thet
