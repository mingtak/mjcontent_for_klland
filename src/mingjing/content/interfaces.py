# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from mingjing.content import _
from zope import schema
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
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
    relatedURL = schema.List(
        title=_(u"Related URL"),
        description=_(u"Filed format: title|||URL"),
        value_type=schema.TextLine(title=u"Related URL"),
        required=False,
    )

    marquee = schema.List(
        title=_(u"Custom Marquee"),
        value_type=schema.TextLine(title=u"Custom Marquee"),
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


class IRelatedLink(Interface):
    """  """

    url = schema.URI(
        title=_(u"URL"),
        required=True,
    )

    color = schema.TextLine(
        title=_(u"Background Color code"),
        required=True,
    )

    textImage = NamedBlobImage(
        title=_(u"Text Image, size: 180X25px"),
        required=True,
    )
