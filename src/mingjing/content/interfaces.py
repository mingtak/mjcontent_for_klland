# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from mingjing.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.app.vocabularies.catalog import CatalogSource
#from plone.supermodel import model
from plone.directives import form
from DateTime import DateTime
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

date_range = {
    'query': (DateTime()-1, DateTime()), 
    'range': 'min:max',
}


class IMingjingContentLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IYoutube(Interface):
    """  """

    youtubeURL = schema.URI(
        title=_(u"Youtube URL"),
        required=True,
    )

class ICover(Interface):
    """  """

    rankingNews = schema.Text(
        title=_(u"Ranking News"),
        description=_(u"Please input ranking news id, per line one id, sorted on modified, max 6 news."),
        required=False,
    )


classification = SimpleVocabulary(
    [SimpleTerm(value=u'related', title=_(u'Related')),
     SimpleTerm(value=u'external', title=_(u'External'))]
)

class IAd(Interface):
    """  """

    category = schema.Choice(
        title=_(u"Category"),
        vocabulary=classification,
        required=True,
    )

    url = schema.URI(
        title=_(u"URL"),
        required=True,
    )
