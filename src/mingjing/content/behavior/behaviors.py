# -*- coding: utf-8 -*-
from mingjing.content import _
# from plone.autoform import directives
from plone.supermodel import directives
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope.component import adapts
from zope.interface import alsoProvides, implements
from zope.interface import provider
from z3c.relationfield.schema import RelationList, RelationChoice
from plone.app.vocabularies.catalog import CatalogSource
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import dexterity
from plone.app.textfield import RichText
from plone.app.content.interfaces import INameFromTitle
from DateTime import DateTime
import random
from plone.directives import form
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone import api


class INamedBlob(model.Schema):
    """ Add NamedBlobImage, and NamedBlobFile """

    model.fieldset(
        'Files',
        label=_(u"Files"),
        fields=['file_1', 'file_2', 'file_3', 'file_4', 'file_5']
    )

    model.fieldset(
        'Images',
        label=_(u"Images"),
        fields=['image_1', 'desc_1', 'image_2', 'desc_2', 'image_3', 'desc_3', 'image_4', 'desc_4', 'image_5', 'desc_5']
    )

    file_1 = NamedBlobFile(
        title=_(u"File"),
        required=False,
    )

    file_2 = NamedBlobFile(
        title=_(u"File"),
        required=False,
    )

    file_3 = NamedBlobFile(
        title=_(u"File"),
        required=False,
    )

    file_4 = NamedBlobFile(
        title=_(u"File"),
        required=False,
    )

    file_5 = NamedBlobFile(
        title=_(u"File"),
        required=False,
    )

    image_1 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    desc_1 = schema.TextLine(
        title=_(u"Image description"),
        required=False,
    )

    image_2 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    desc_2 = schema.TextLine(
        title=_(u"Image description"),
        required=False,
    )

    image_3 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    desc_3 = schema.TextLine(
        title=_(u"Image description"),
        required=False,
    )

    image_4 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    desc_4 = schema.TextLine(
        title=_(u"Image description"),
        required=False,
    )

    image_5 = NamedBlobImage(
        title=_(u"Image"),
        required=False,
    )

    desc_5 = schema.TextLine(
        title=_(u"Image description"),
        required=False,
    )


class IContentLog(model.Schema):
    """ Add Content Log Field """

    form.mode(contentLog='hidden')
    contentLog = schema.List(
        title=_(u"Content Log"),
        value_type=schema.TextLine(title=_("Content Log")),
        required=False,
    )


class ICateTable(model.Schema):
    """ Add Category Table """

    model.fieldset(
        'Category Table',
        label=_(u"Category Table"),
        fields=['cateTable']
    )

    cateTable = schema.Text(
        title=_(u"Category Table"),
        required=False,
    )


class IKlMeta(model.Schema):
    """ Add KL land Metadata field """

    """
    cateL1 = schema.TextLine(
        title=_(u"Main Category"),
        required=False,
    )

    cateL2 = schema.TextLine(
        title=_(u"Sub Category"),
        required=False,
    )
    """

    pubUnit = schema.TextLine(
        title=_(u"Publish Unit"),
#        default=api.user.get_current().id,
        required=False,
    )

    form.mode(dfilesString='hidden')
    dexterity.write_permission(dfilesString='cmf.ManagePortal')
    dfilesString = schema.Text(
        title=(u"Download file string(href, json string)"),
        required=False,
    )


class IFeatured(model.Schema):
    """ Add featured field """

    form.mode(featured='hidden')
    featured = schema.Bool(
        title=_(u"Featured"),
        description=_(u"Checked it for featured."),
        default=False,
        required=False,
    )

#    form.mode(headWeight='hidden')
    headWeight = schema.Int(
        title=_(u"Head Weight"),
        description=_(u"Please set Head Weight value, default:10."),
        default=10,
        required=True,
    )


class IKeywords(model.Schema):
    """ Add keywords for Article """

    keywords = schema.TextLine(
        title=_(u"Keywords"),
        description=_(u"Keywords for article, separate use ','"),
        required=False,
    )


class IFreeContent(model.Schema):
    """ Add RichText for Free Content """
    freeContent = RichText(
        title=_(u"Free Content"),
        required=False,
    )


class IOriginalUrl(model.Schema):
    """ Add url field for News Original URL """

    dexterity.write_permission(originalUrl='cmf.ManagePortal')
#    form.mode(originalUrl='hidden')
    originalUrl = schema.URI(
        title=_(u"Original URL"),
        required=False,
    )


class IOldFields(model.Schema):
    """ Add Old Fields """
#    form.mode(oldPicturePath='hidden')
    oldPicturePath = schema.TextLine(
        title=_(u"Old Picture Path"),
        required=False,
    )

    form.mode(oldKeywords='hidden')
    oldKeywords = schema.TextLine(
        title=_(u"Old Keywords"),
        required=False,
    )

    form.mode(oldCreateTime='hidden')
    oldCreateTime = schema.Datetime(
        title=_(u"Old Create Time"),
        required=False,
    )

    form.mode(oldEbookURL='hidden')
    oldEbookURL = schema.TextLine(
        title=_(u"Old Ebook URL"),
        required=False,
    )


alsoProvides(IFreeContent, IFormFieldProvider)
alsoProvides(IOriginalUrl, IFormFieldProvider)
alsoProvides(IOldFields, IFormFieldProvider)
alsoProvides(IKeywords, IFormFieldProvider)
alsoProvides(IFeatured, IFormFieldProvider)
alsoProvides(IContentLog, IFormFieldProvider)
alsoProvides(IKlMeta, IFormFieldProvider)
alsoProvides(ICateTable, IFormFieldProvider)
alsoProvides(INamedBlob, IFormFieldProvider)


def context_property(name):
    def getter(self):
        return getattr(self.context, name)
    def setter(self, value):
        setattr(self.context, name, value)
    def deleter(self):
        delattr(self.context, name)
    return property(getter, setter, deleter)


class OldFields(object):
    implements(IOldFields)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    oldPicturePath = context_property("oldPicturePath")
    oldKeywords = context_property("oldKeywords")
    oldCreateTime = context_property("oldCreateTime")
    oldEbookURL = context_property("oldEbookURL")


class Featured(object):
    implements(IFeatured)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    featured = context_property("featured")
    headWeight = context_property("headWeight")


class ContentLog(object):
    implements(IContentLog)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    contentLog = context_property("contentLog")


class FreeContent(object):
    implements(IFreeContent)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    freeContent = context_property("freeContent")


class CateTable(object):
    implements(ICateTable)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    cateTable = context_property("cateTable")


class Keywords(object):
    implements(IKeywords)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    keywords = context_property("keywords")


class OriginalUrl(object):
    implements(IOriginalUrl)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    originalUrl = context_property("originalUrl")


class KlMeta(object):
    implements(IKlMeta)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    cateL1 = context_property("cateL1")
    cateL2 = context_property("cateL2")
    pubUnit = context_property("pubUnit")
    dfilesString = context_property("dfilesString")


class INamedFromTimeStamp(INameFromTitle):
    """ Marker/Form interface for namedFromTimeStamp
    """


class NamedBlob(object):
    implements(INamedBlob)
    adapts(IDexterityContent)

    def __init__(self,context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    file_1 = context_property("file_1")
    file_2 = context_property("file_2")
    file_3 = context_property("file_3")
    file_4 = context_property("file_4")
    file_5 = context_property("file_5")
    image_1 = context_property("image_1")
    image_2 = context_property("image_2")
    image_3 = context_property("image_3")
    image_4 = context_property("image_4")
    image_5 = context_property("image_5")
    desc_1 = context_property("desc_1")
    desc_2 = context_property("desc_2")
    desc_3 = context_property("desc_3")
    desc_4 = context_property("desc_4")
    desc_5 = context_property("desc_5")


class NamedFromTimeStamp(object):
    """ Adapter for NamedFromTimeStamp
    """
    implements(INamedFromTimeStamp)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context

    # -*- Your behavior property setters & getters here ... -*-
    @property
    def title(self):
        timeString = '%s%s' % (DateTime().strftime("%Y%m%d%H%M"), random.randint(100000, 999999))
        return timeString
