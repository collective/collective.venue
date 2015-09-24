from Products.CMFCore.utils import getToolByName
from collective.venue.interfaces import IVenue
from plone import api
from plone.app.uuid.utils import uuidToPhysicalPath
from plone.app.widgets.browser.vocabulary import _permissions
from plone.uuid.interfaces import IUUID
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import ISource
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


_permissions['collective.venue.VenueVocabulary'] = 'View'
_permissions['collective.venue.DefaultVenueVocabulary'] = 'View'


@provider(IVocabularyFactory)
def VenueVocabulary(context, query=None):
    """Vocabulary for venues.
    """
    cat = getToolByName(getSite(), 'portal_catalog')
    res = cat(is_folderish=True, path='/')
    # TODO: implement batching
    items = [
        SimpleTerm(
            title='{0} ({1})'.format(it.Title, it.getURL()),
            value=it.UID
        ) for it in res
        if query is None or query.lower() in
        '{0} ({1})'.format(it.Title, it.getURL()).lower()
    ]
    return SimpleVocabulary(items)


@provider(IVocabularyFactory)
def DefaultVenueVocabulary(context, query=None):
    """Vocabulary for default venues.
    """
    search_base = api.portal.get_registry_record('collective.venue.search_base')  # noqa
    cat_query = {'object_provides': IVenue.__identifier__, 'path': '/'}
    if search_base:
        path = uuidToPhysicalPath(search_base)
        if path:
            cat_query['path'] = path
        # else - path might be deleted

    cat = getToolByName(getSite(), 'portal_catalog')
    res = cat(**cat_query)

    items = [
        SimpleTerm(
            title='{0} ({1})'.format(it.Title, it.getURL()),
            value=it.UID
        ) for it in res
        if query is None or query.lower() in
        '{0} ({1})'.format(it.Title, it.getURL()).lower()
    ]
    return SimpleVocabulary(items)


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
        search_base = api.portal.get_registry_record('collective.venue.search_base')  # noqa
        settings_query = {}
        if search_base:
            path = uuidToPhysicalPath(search_base)
            if path:
                settings_query['path'] = path
            # else - path might be deleted

        query = user_query.copy()
        query.update(self.query)
        query.update(settings_query)

        catalog = getToolByName(site, 'portal_catalog')
        return catalog(query)
