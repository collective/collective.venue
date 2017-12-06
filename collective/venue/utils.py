# -*- coding: utf-8 -*-
from collective.address.behaviors import IAddress
from collective.address.behaviors import IContact
from collective.address.vocabulary import get_pycountry_name
from plone import api
from plone.app.uuid.utils import uuidToPhysicalPath
from plone.uuid.interfaces import IUUID
from zope.component.hooks import getSite


try:
    from collective.geolocationbehavior.geolocation import IGeolocatable
except ImportError:
    IGeolocatable = None


def join_nonempty(items, sep=u'/'):
    return sep.join([it for it in items if it])


def get_site(context=None):
    return '/'.join(getSite().getPhysicalPath())


def get_base_path(context=None):
    search_base = api.portal.get_registry_record('collective.venue.search_base')  # noqa
    path = get_site(context)
    if search_base:
        path = uuidToPhysicalPath(search_base)
    return path


def get_venue_url(venue):
    """Get URL to venue.
    We explicitly support here venues defined in other subsites. If so, URL is
    specially constructed, so that we can show the venue in our own site.
    """
    # construct url to location
    site = getSite()
    venue_url = venue.absolute_url()
    site_path = u'/'.join(site.getPhysicalPath())
    venue_path = u'/'.join(venue.getPhysicalPath())
    if site_path not in venue_path:
        # venue in different site - cannot directly open it
        venue_url = u'{0}/@@venue_view?uid={1}'.format(
            site.absolute_url(),
            IUUID(venue)
        )
    return venue_url


def get_venue_address_string(venue):
    address = IAddress(venue, None)
    if not address:
        return

    country = get_pycountry_name(address.country)
    ret = join_nonempty((
        address.street,
        join_nonempty((address.zip_code, address.city), sep=u' '),
        country
    ), sep=u', ')

    return ret


def get_venue_contact_string(venue):
    contact = IContact(venue, None)
    if not contact:
        return

    ret = join_nonempty((
        contact.email,
        contact.website,
        contact.phone or contact.mobile
    ), sep=u', ')

    return ret
