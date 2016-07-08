# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
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

        address_data = {}

        address_data['title'] = self.title
        address_data['description'] = self.description

        add = IAddress(context, None)
        if add:
            address_data['street'] = add.street
            address_data['zip_code'] = add.zip_code
            address_data['city'] = add.city
            address_data['country'] = get_pycountry_name(add.country) or ''
            address_data['notes'] = add.notes and add.notes.output or ''

        contact = IAddress(context, None)
        if contact:
            address_data['email'] = contact.email
            address_data['web'] = contact.website
            address_data['phone'] = contact.phone
            address_data['mobile'] = contact.mobile
            address_data['fax'] = contact.fax

        coordinates = self.data_coordinates
        if coordinates:
            address_data['latitude'] = coordinates[0]
            address_data['longitude'] = coordinates[1]

        return address_data

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
                            coordinates[0],
                            coordinates[1]
                        ]
                    }
                },
            ]
        })
        return geo_json
