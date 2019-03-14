# -*- coding: utf-8 -*-
from collective.geolocationbehavior.geolocation import IGeolocatable
from collective.venue.behaviors import ILocation
from plone.app.uuid.utils import uuidToObject
from plone.indexer.decorator import indexer
from zope.interface import Interface


def get_geoobject(obj):
    geo = IGeolocatable(obj, None)
    if not geo:
        location_ref = ILocation(obj, None)
        geo = uuidToObject(location_ref.location_uid) if location_ref else None
    return geo


@indexer(Interface)
def latitude(obj):
    geo = get_geoobject(obj)
    return geo.geolocation.latitude


@indexer(Interface)
def longitude(obj):
    geo = get_geoobject(obj)
    return geo.geolocation.longitude
