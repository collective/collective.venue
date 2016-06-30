# -*- coding: utf-8 -*-
from .. import messageFactory as _
from ..interfaces import IVenueSettings
from plone.app.registry.browser import controlpanel


class VenueControlPanelForm(controlpanel.RegistryEditForm):

    id = "VenueControlPanel"
    label = _(u"Event Venue Settings")
    description = _("Settings for venues, which are referenced by events.")
    schema = IVenueSettings
    schema_prefix = "collective.venue"
    ignoreContext = True


class VenueControlPanel(controlpanel.ControlPanelFormWrapper):
    form = VenueControlPanelForm
