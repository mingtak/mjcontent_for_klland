# -*- coding: utf-8 -*-
from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.app.vocabularies.catalog import CatalogSource
from zope.interface import implements
import pickle
from mingjing.content import _


class IHot(IPortletDataProvider):
    """  """


class Assignment(base.Assignment):
    implements(IHot)


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('hot_listing.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return xhtml_compress(self._template())

    def loadFile(self, filename):
        try:
            with open('/tmp/%s' % filename) as file:
                return pickle.load(file)
        except:
            return None

    def getUidList(self, sortedList):
        result = []
        for item in sortedList:
            result.append(item[0])
        return result

    def update(self):
        today = self.loadFile('statToday')
        week = self.loadFile('statWeek')
        month = self.loadFile('statMonth')

        self.monthList = self.getUidList(month)


class AddForm(base.AddForm):
    schema = IHot
    label = _(u"Add Hot Listing Portlet")
    description = _(u"This portlet rendering Hot Listing.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    schema = IHot
    label = _(u"Edit Hot Listing Portlet")
    description = _(u"This portlet rendering Hot Listing.")

