# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
from collective.address.behaviors import IContact
from collective.address.behaviors import ISocial
from collective.address.vocabulary import get_pycountry_name
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView

import json
import pkg_resources


try:
    pkg_resources.get_distribution('collective.geolocationbehavior')
except pkg_resources.DistributionNotFound:
    HAS_GEOLOCATION = False
else:
    from collective.geolocationbehavior.geolocation import IGeolocatable
    HAS_GEOLOCATION = True


class VenueView(BrowserView):

    def __init__(self, context, request):
        venue_uid = request.get('uid', None)
        if venue_uid:
            venue_obj = uuidToObject(venue_uid)
            if venue_obj:
                # Change the context to the one of the uid referenced object.
                # That's the easiest way to render a venue from a different
                # subsite on any context. However, this might lead to broken
                # urls in for the edit bar.
                context = venue_obj

        self.context = context
        self.request = request

    @property
    def title(self):
        title = safe_unicode(getattr(self.context, 'title', u''))
        return title

    @property
    def description(self):
        description = safe_unicode(getattr(self.context, 'description', u''))
        return description

    @property
    def data_coordinates(self):
        if not HAS_GEOLOCATION:
            return
        geo = IGeolocatable(self.context, None)
        if not geo:
            return

        return (
            geo.geolocation.latitude,
            geo.geolocation.longitude
        )

    @property
    def data(self):
        context = self.context

        data = {}

        data['title'] = self.title
        data['description'] = self.description

        coordinates = self.data_coordinates
        if coordinates:
            data['latitude'] = coordinates[0]
            data['longitude'] = coordinates[1]

        acc = IAddress(context, None)
        address = {}
        if acc:
            address['street'] = acc.street
            address['zip_code'] = acc.zip_code
            address['city'] = acc.city
            address['country'] = get_pycountry_name(acc.country) or u''
            address['notes'] = acc.notes and acc.notes.output or u''
        data['address'] = address

        acc = IContact(context, None)
        contact = {}
        if acc:
            contact['email'] = acc.email
            contact['web'] = acc.website
            contact['phone'] = acc.phone
            contact['mobile'] = acc.mobile
            contact['fax'] = acc.fax
        data['contact'] = contact

        acc = ISocial(context, None)
        social = {}
        if acc:
            social['facebook'] = acc.facebook_url
            social['twitter'] = acc.twitter_url
            social['google_plus'] = acc.google_plus_url
            social['instagram'] = acc.instagram_url
        data['social'] = social

        return data

    @property
    def data_geojson(self):
        """Return the geo location as GeoJSON string.
        """
        coordinates = self.data_coordinates
        if not coordinates:
            return

        geo_json = json.dumps({
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'id': IUUID(self.context),
                    'properties': {
                        'popup': u'<h3>{0}</h3><p>{1}</p>'.format(
                            self.title,
                            self.description
                        )
                    },
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [
                            coordinates[1],  # lng
                            coordinates[0]   # lat
                        ]
                    }
                },
            ]
        })
        return geo_json
