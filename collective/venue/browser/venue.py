# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
from collective.address.behaviors import IContact
from collective.address.behaviors import ISocial
from collective.address.vocabulary import get_pycountry_name
from collective.venue import messageFactory as _
from plone.api.portal import get_registry_record as getrec
from plone.app.uuid.utils import uuidToObject
from plone.uuid.interfaces import IUUID
from Products.CMFPlone.resources import add_bundle_on_request
from Products.CMFPlone.utils import get_top_request
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

        top_request = get_top_request(request)
        # Just add the bundle from plone.patternslib.
        # If it's not available, it wont't hurt.
        add_bundle_on_request(top_request, 'bundle-leaflet')

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
    def google_maps_link(self):
        coordinates = self.data_coordinates
        show_link = getrec('geolocation.show_google_maps_link')
        if not coordinates or not show_link:
            return

        maps_link = "https://www.google.com/maps/place/{0}+{1}/@{0},{1},17z".format(  # noqa
            coordinates[0],
            coordinates[1]
        )
        return maps_link

    @property
    def map_configuration(self):
        map_layers = getrec('geolocation.map_layers') or []
        config = {
            "minimap": True,
            "default_map_layer": getrec('geolocation.default_map_layer'),
            "map_layers": [
                {"title": _(it), "id": it}
                for it in map_layers
            ],
        }
        return json.dumps(config)

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
        if getattr(self, '_data', False):
            return self._data

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
            address['notes'] = acc.notes.output if acc.notes else u''
        data['address'] = {
            key: value for key, value in address.items() if value
        }

        acc = IContact(context, None)
        contact = {}
        if acc:
            contact['email'] = acc.email
            contact['web'] = acc.website
            contact['phone'] = acc.phone
            contact['mobile'] = acc.mobile
            contact['fax'] = acc.fax
        data['contact'] = {
            key: value for key, value in contact.items() if value
        }

        acc = ISocial(context, None)
        social = {}
        if acc:
            social['facebook'] = acc.facebook_url
            social['twitter'] = acc.twitter_url
            social['google_plus'] = acc.google_plus_url
            social['instagram'] = acc.instagram_url
        data['social'] = {
            key: value for key, value in social.items() if value
        }

        self._data = data
        return data

    @property
    def data_geojson(self):
        """Return the geo location as GeoJSON string.
        """
        data = self.data

        address = data.get('address')
        address_str = u', '.join([
            it.strip() for it in
            [
                address.get('street'),
                address.get('zip_code', '') + ' ' + address.get('city', ''),
                address.get('country')
            ] if it
        ])

        def _wrap_text(text):
            return u'<p>{0}</p>'.format(text) if text else None

        popup_text = u''.join([_wrap_text(it) for it in [
            data.get('description'),
            address_str
        ] if it])
        popup_text = u'<h3>' + data.get('title') + u'</h3>' + popup_text

        geo_json = json.dumps({
            'type': 'FeatureCollection',
            'features': [
                {
                    'type': 'Feature',
                    'id': IUUID(self.context),
                    'properties': {'popup': popup_text},
                    'geometry': {
                        'type': 'Point',
                        'coordinates': [
                            data['longitude'],
                            data['latitude']
                        ]
                    }
                },
            ]
        })
        return geo_json
