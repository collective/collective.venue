# -*- coding: utf-8 -*-
from plone.app.widgets.dx import IQueryStringWidget
from z3c.form.converter import BaseDataConverter
from zope.component import adapts
from zope.schema.interfaces import ITextLine


class QueryStringJSONDataConverter(BaseDataConverter):
    """Data converter for IList."""

    adapts(ITextLine, IQueryStringWidget)

    def toWidgetValue(self, value):
        """Converts from field value to widget.

        :param value: Query string.
        :type value: list

        :returns: Query string converted to JSON.
        :rtype: string
        """
        if not value:
            value = '[]'
        return value

    def toFieldValue(self, value):
        """Converts from widget value to field.

        :param value: Query string.
        :type value: string

        :returns: Query string.
        :rtype: list
        """
        if not value:
            value = self.field.missing_value
        return value
