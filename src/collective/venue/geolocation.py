from collective.geolocationbehavior.interfaces import IGeoJSONProperties
from collective.venue.behaviors import ILocation
from plone.app.uuid.utils import uuidToObject
from plone.indexer.decorator import indexer
from plone.uuid.interfaces import IUUID
from zope.component import adapter
from zope.interface import implementer


def get_location_ref(obj):
    location_ref = ILocation(obj, None)
    if location_ref:
        location_uid = location_ref.location_uid
        return uuidToObject(location_uid)


@indexer(ILocation)
def latitude(obj):
    loc = get_location_ref(obj)
    return loc and loc.geolocation.latitude or None


@indexer(ILocation)
def longitude(obj):
    loc = get_location_ref(obj)
    return loc and loc.geolocation.longitude or None


@adapter(ILocation)
@implementer(IGeoJSONProperties)
class GeoJSONProperties:

    def __init__(self, context):
        self.context = context

    @property
    def popup(self):
        location = get_location_ref(self.context)
        if location is None:
            location = self.context

        return """
<header><a href="{}">{}</a></header>
<p>{}</p>
            """.format(
            self.context.absolute_url(),
            self.context.title,
            location.title,
        )

    @property
    def extraClasses(self):
        return f"uuid-{IUUID(self.context)}"
