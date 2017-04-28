# -*- coding: utf-8 -*-
from plone.indexer.decorator import indexer
from zope.interface import Interface
from Products.CMFPlone.utils import safe_unicode

from plone.app.contenttypes.interfaces import INewsItem
from mingjing.content.interfaces import IAd


@indexer(Interface)
def featured_indexer(obj):
    if hasattr(obj, 'featured'):
        return obj.featured


@indexer(Interface)
def headWeight_indexer(obj):
    if hasattr(obj, 'headWeight'):
        return obj.headWeight


@indexer(IAd)
def category_indexer(obj):
    if hasattr(obj, 'category'):
        return obj.category

"""
@indexer(Interface)
def hasOldPicture_indexer(obj):
    if getattr(obj, 'oldPicturePath', False):
        return True
    else:
        return False

"""
