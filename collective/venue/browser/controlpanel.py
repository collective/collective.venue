# -*- coding: utf-8 -*-
from .. import messageFactory as _
from ..interfaces import IVenueLayer
from ..interfaces import IVenueSettings
from plone.app.registry.browser import controlpanel
from plone.app.widgets.dx import AjaxSelectWidget
from z3c.form.interfaces import IFieldWidget
from z3c.form.util import getSpecification
from z3c.form.widget import FieldWidget
from zope.component import adapter
from zope.interface import implementer


class VenueControlPanelForm(controlpanel.RegistryEditForm):

    id = "VenueControlPanel"
    label = _(u"Event Venue Settings")
    description = _("Settings for venues, which are referenced by events.")
    schema = IVenueSettings
    schema_prefix = "collective.venue"


class VenueControlPanel(controlpanel.ControlPanelFormWrapper):
    form = VenueControlPanelForm


@adapter(getSpecification(IVenueSettings['search_base']), IVenueLayer)
@implementer(IFieldWidget)
def SearchBaseFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    return widget


@adapter(getSpecification(IVenueSettings['default_venue']), IVenueLayer)
@implementer(IFieldWidget)
def DefaultVenueFieldWidget(field, request):
    widget = FieldWidget(field, AjaxSelectWidget(request))
    return widget
