from plone.api.portal import get_registry_record as getrec
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView

import geopy
import json


class LocationSearch(BrowserView):

    @property
    def google_api_key(self):
        return getrec('geolocation.google_api_key')

    def get_location_info(self, address):
        location = None
        try:
            if self.google_api_key:
                geolocator = geopy.geocoders.GoogleV3(api_key=self.google_api_key)  # noqa
                location = geolocator.geocode(address, exactly_one=True)
            else:
                geolocator = geopy.geocoders.Nominatim()
                location = geolocator.geocode(address, exactly_one=True)
        except:
            pass

        return location

    def __call__(self):

        self.request.response.setHeader(
            'Content-Type', 'application/json; charset=utf-8'
        )

        location = None

        title = safe_unicode(self.request.form.get('title'))
        street = safe_unicode(self.request.form.get('street'))
        city = safe_unicode(self.request.form.get('city'))
        zip_code = safe_unicode(self.request.form.get('zip_code'))
        country = safe_unicode(self.request.form.get('country'))

        address = u", ".join([
            it
            for it in [street, zip_code + " " + city, country]
            if it
        ])

        if address:
            location = self.get_location_info(
                title + ", " + address if title else address
            )

            if title and not location:
                # Try without title now
                location = self.get_location_info(address)

        return json.dumps({
            'latitude': getattr(location, 'latitude', None),
            'longitude': getattr(location, 'longitude', None)
        })
