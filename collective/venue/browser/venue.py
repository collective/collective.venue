from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from collective.address.behaviors import IAddress
from collective.address.behaviors import ISocial
from collective.address.vocabulary import get_pycountry_name
from plone.app.uuid.utils import uuidToObject
import pkg_resources
import json

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
    def data(self):
        context = self.context
        address_data = {}
        add = IAddress(context, None)
        social = ISocial(context, None)
        geo = None
        if HAS_GEOLOCATION:
            geo = IGeolocatable(context, None)

        title = safe_unicode(getattr(self.context, 'title', u''))
        description = safe_unicode(getattr(self.context, 'description', u''))

        address_data['title'] = title
        address_data['description'] = description
        address_data['street'] = add.street
        address_data['zip_code'] = add.zip_code
        address_data['city'] = add.city
        address_data['country'] = get_pycountry_name(add.country) or ''
        address_data['geopoints'] = ''
        address_data['latitude'] = ''
        address_data['longitude'] = ''
        address_data['facebook'] = ''
        address_data['twitter'] = ''
        address_data['google_plus'] = ''
        address_data['instagram'] = ''
        address_data['notes'] = add.notes and add.notes.output or ''

        if social:
            address_data['facebook'] = social.get('facebook_url', '')
            address_data['twitter'] = social.get('twitter_url', '')
            address_data['google_plus'] = social.get('google_plus_url', '')
            address_data['instagram'] = social.get('instagram_url', '')

        if geo:
            latitude = geo.geolocation.get('latitude', '')
            longitude = geo.geolocation.get('longitude', '')
            geo_json = json.dumps([{
                'lat': latitude,
                'lng': longitude,
                'popup': u'<h3>{0}</h3><p>{1}</p>'.format(title, description)
            }])
            address_data['geopoints'] = geo_json
            address_data['latitude'] = latitude
            address_data['longitude'] = longitude

        return address_data
