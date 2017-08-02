# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from datetime import datetime
from DateTime import DateTime
import json
#from plone.memoize import ram
from time import time
from Products.CMFPlone.utils import safe_unicode
import logging
import pickle
import MySQLdb
import operator


logger = logging.getLogger('mingjing.content')


class SiteMap(BrowserView):

    template = ViewPageTemplateFile("template/site_map.pt")

    def __call__(self):
        request = self.request

        if api.user.is_anonymous():
            portal = api.portal.get()
            return request.response.redirect(portal.absolute_url())

        return self.template()
