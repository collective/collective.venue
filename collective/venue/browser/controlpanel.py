# -*- coding: utf-8 -*-
from collective.venue import messageFactory as _
from collective.venue.interfaces import IVenueSettings
from plone.app.registry.browser import controlpanel


class VenueControlPanelForm(controlpanel.RegistryEditForm):

    id = "VenueControlPanel"
    schema = IVenueSettings
    schema_prefix = "collective.venue"

    label = _(u"Event Venue Settings")
    description = _("Settings for venues, which are referenced by events.")


class VenueControlPanel(controlpanel.ControlPanelFormWrapper):
    form = VenueControlPanelForm
