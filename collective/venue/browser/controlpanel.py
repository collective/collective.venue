# -*- coding: utf-8 -*-
from .. import messageFactory as _
from ..interfaces import IVenueSettings
from plone.app.registry.browser import controlpanel
from ..interfaces import IVenueLayer

class VenueControlPanelForm(controlpanel.RegistryEditForm):

    id = "VenueControlPanel"
    label = _(u"Event Venue Settings")
    description = _("Settings for venues, which are referenced by events.")
    schema = IVenueSettings
    schema_prefix = "collective.venue"


class VenueControlPanel(controlpanel.ControlPanelFormWrapper):
    form = VenueControlPanelForm


from plone.app.widgets.dx import QueryStringWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer


@adapter(getSpecification(IVenueSettings['source_query']), IVenueLayer)
@implementer(IFieldWidget)
def SourceQueryFieldWidget(field, request):
    return FieldWidget(field, QueryStringWidget(request))
