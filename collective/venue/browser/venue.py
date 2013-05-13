from plone.app.dexterity.behaviors.metadata import IDublinCore
from collective.geolocationbehavior.geolocation import IGeolocatable
from collective.address.behaviors import IAddress
from Products.Five.browser import BrowserView

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
        meta = IDublinCore(context)
        geo = IGeolocatable(context)
        add = IAddress(context)

        title = self.cleanup(meta.title)
        description = self.cleanup(meta.description)
        popup = '<h3>%s</h3><p>%s</p>' % (
            title,
            description and description or '')

        return {
            'title': meta.title,
            'description': meta.description,
            'popup': popup,
            'has_geo': geo.geolocation.latitude and geo.geolocation.longitude,
            'latitude': geo.geolocation.latitude,
            'longitude': geo.geolocation.longitude,
            'street': add.street,
            'zip_code': add.zip_code,
            'city': add.city,
            'country': add.country,
            'notes': add.notes,
        }

    @property
    def get_brefs(self):
        ref = IReferenceable(self.context)
        return ref.getBRefs()
