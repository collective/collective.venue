try:
    from plone.app.event.at.interfaces import IATEvent
except ImportError:
    from Products.ATContentTypes.interfaces import IATEvent


class IATEventWithVenue(IATEvent):
    """Marker interface for schema extended ATEvents with Venue information."""
