# -*- coding: utf-8 -*-
from plone import api
from zope.component.hooks import getSite
from plone.app.uuid.utils import uuidToPhysicalPath


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
