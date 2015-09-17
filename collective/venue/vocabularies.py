from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.querystring import queryparser
from plone.uuid.interfaces import IUUID
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import ISource
import json


@implementer(ISource)
class VenueSource(object):
    """Catalog source for listing venues for use with Choice fields.
    """

    def __init__(self, context=None, **query):
        self.query = query

    def __contains__(self, value):
        if isinstance(value, basestring):
            uid = value
        else:
            uid = IUUID(value)
        if self.search_catalog({'UID': uid}):
            return True

    def search_catalog(self, user_query):
        site = getSite()
        source_query = api.portal.get_registry_record('collective.venue.source_query')  # noqa
        parsed_source_query = {}
        if source_query:
            parsed_source_query = queryparser.parseFormquery(site, json.loads(source_query))  # noqa

        query = user_query.copy()
        if parsed_source_query:
            query.update(parsed_source_query)
        else:
            query.update(self.query)

        catalog = getToolByName(site, 'portal_catalog')
        return catalog(query)
