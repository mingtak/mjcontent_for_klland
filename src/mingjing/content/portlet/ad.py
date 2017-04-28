from plone.app.portlets.portlets import base
from plone.memoize.compress import xhtml_compress
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.app.vocabularies.catalog import CatalogSource
from zope.interface import implements
from mingjing.content import _


class IAd(IPortletDataProvider):
    """  """

class Assignment(base.Assignment):
    implements(IAd)


class Renderer(base.Renderer):

    _template = ViewPageTemplateFile('ad_listing.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)

    def render(self):
        return xhtml_compress(self._template())


class AddForm(base.AddForm):
    schema = IAd
    label = _(u"Add Ad Listing Portlet")
    description = _(u"This portlet rendering Ad Listing.")

    def create(self, data):
        return Assignment()


class EditForm(base.EditForm):
    schema = IAd
    label = _(u"Edit Ad Listing Portlet")
    description = _(u"This portlet rendering Ad Listing.")

