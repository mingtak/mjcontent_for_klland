# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from DateTime import DateTime
from datetime import datetime

LIMIT = 10


class RwdMenu(base.ViewletBase):
    """  """


class ScriptToFooter(base.ViewletBase):
    """  """


class AboveContentInfo(base.ViewletBase):
    """  """


class SocialList(base.ViewletBase):
    """  """


class CustomInfoInHeader(base.ViewletBase):
    """  """

    """
    def render(self):
        portal = api.portal.get()
        request = self.request
        context = self.context
        to_folder_contents = True if ('edit' in request.get('HTTP_REFERER') and context.Type() not in ['Folder', 'Plone Site']) else False

        if to_folder_contents:
            return '<meta http-equiv="refresh" content="0;url=%s/folder_contents" />' % context.getParentNode().absolute_url()
        return ''
    """
