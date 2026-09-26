from collective.address.behaviors import searchable_text_indexer as address_idx
from collective.venue.behaviors import ILocation
from collective.venue.interfaces import IVenue
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.uuid.utils import uuidToObject
from plone.indexer import indexer
from Products.CMFCore.utils import getToolByName


# Index lat/lng of ILocation behavior providing objects like Events.
# IGeolocatable (which venue objects provide) are already indexed in
# collective.geolocationbehavior


@indexer(ILocation)
def latitude(obj):
    if not obj.location_uid:
        raise AttributeError("no location")
    venue = uuidToObject(obj.location_uid)
    return venue.geolocation.latitude


@indexer(ILocation)
def longitude(obj):
    if not obj.location_uid:
        raise AttributeError("no location")
    venue = uuidToObject(obj.location_uid)
    return venue.geolocation.longitude


# Text indexing
@indexer(IVenue)
def searchable_text_indexer(obj):
    address = address_idx(obj)()  # returns DelegatingIndexer callable
    meta_basic = IBasic(obj)
    venue = IVenue(obj)
    notes = (venue.notes and venue.notes.output_relative_to(obj)) or ""
    if notes:
        transforms = getToolByName(obj, "portal_transforms")
        body_plain = (
            transforms
            .convertTo(
                "text/plain",
                notes,
                mimetype="text/html",
            )
            .getData()
            .strip()
        )
        notes = body_plain

    parts = [
        address,
        meta_basic.title,
        meta_basic.description,
        notes,
    ]
    ret = " ".join([part for part in parts if part])
    return ret
