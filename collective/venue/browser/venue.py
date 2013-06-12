from Products.Five.browser import BrowserView
from collective.address.behaviors import IAddress
from collective.address.vocabulary import get_pycountry_name
from collective.geolocationbehavior.geolocation import IGeolocatable
from plone.app.dexterity.behaviors.metadata import IBasic

try:
    from Products.Archetypes.interfaces.referenceable import IReferenceable
except ImportError:
    from plone.app.referenceablebehavior.referenceable import IReferenceable


class VenueView(BrowserView):

    def cleanup(self, txt):
        if not txt:
            return
        return txt.replace('"', "'")

    @property
    def data(self):
        context = self.context
        meta_basic = IBasic(context)
        geo = IGeolocatable(context)
        add = IAddress(context)

        title = self.cleanup(meta_basic.title)
        description = self.cleanup(meta_basic.description)
        popup = '<h3>%s</h3><p>%s</p>' % (
            title,
            description and description or '')

        return {
            'title': meta_basic.title,
            'description': meta_basic.description,
            'popup': popup,
            'has_geo': geo.geolocation.latitude and geo.geolocation.longitude,
            'latitude': geo.geolocation.latitude,
            'longitude': geo.geolocation.longitude,
            'street': add.street,
            'zip_code': add.zip_code,
            'city': add.city,
            'country': get_pycountry_name(add.country) or '',
            'notes': add.notes and add.notes.output or '',
        }

    @property
    def get_brefs(self):
        ref = IReferenceable(self.context)
        return ref.getBRefs(relationship='isVenueForEvent')
