from collective.venue import _
from plone.api.portal import get_registry_record as getrec
from Products.Five.browser import BrowserView

import geopy
import json


# Messages of the collective-venue-locationsearch JavaScript pattern.
# Listed here for i18n extraction, translated client side via @@plonejsi18n.
_("Search location")
_("Could not find an address.")


class LocationSearch(BrowserView):
    @property
    def google_api_key(self):
        return getrec("geolocation.google_api_key")

    def get_location_info(self, address):
        location = None
        try:
            if self.google_api_key:
                geolocator = geopy.geocoders.GoogleV3(
                    user_agent="collective.venue",
                    api_key=self.google_api_key,
                )
                location = geolocator.geocode(address, exactly_one=True)
            else:
                geolocator = geopy.geocoders.Nominatim(
                    user_agent="collective.venue",
                )
                location = geolocator.geocode(address, exactly_one=True)
        except:  # noqa: E722
            return location

        return location

    def __call__(self):

        self.request.response.setHeader(
            "Content-Type", "application/json; charset=utf-8"
        )

        location = None

        title = self.request.form.get("title")
        street = self.request.form.get("street")
        city = self.request.form.get("city")
        zip_code = self.request.form.get("zip_code")
        country = self.request.form.get("country")

        address = ", ".join([
            it for it in [street, zip_code + " " + city, country] if it
        ])

        if address:
            location = self.get_location_info(
                title + ", " + address if title else address
            )

            if title and not location:
                # Try without title now
                location = self.get_location_info(address)

        return json.dumps({
            "latitude": getattr(location, "latitude", None),
            "longitude": getattr(location, "longitude", None),
        })
