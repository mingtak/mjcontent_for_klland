# -*- coding: utf-8 -*-

import sys
from Testing import makerequest
from AccessControl.SecurityManagement import newSecurityManager
from zope.site.hooks import setHooks
from zope.site.hooks import setSite

from plone import api
from DateTime import DateTime
import transaction
import csv
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides
from bs4 import BeautifulSoup
from Products.CMFPlone.utils import safe_unicode
from plone.app.textfield.value import RichTextValue
from plone import namedfile
import random
#import html2text
import urllib2
import logging

# howto: bin/client1 run pathtofile/import_news.py portal_name admin_id news_site_code(ex. bbc)
# mapping: sys.argv[3] is portal_name, sys.argv[4] is admin_id, sys.argv[5] is news_site_code


logger = logging.getLogger('Import News')



class ToPublished:

    def __init__(self, portal, admin):
        root = makerequest.makerequest(app)
        self.portal = getattr(root, portal, None)

        admin = root.acl_users.getUserById(admin)
        admin = admin.__of__(self.portal.acl_users)
        newSecurityManager(None, admin)
        setHooks()
        setSite(self.portal)
        self.portal.setupCurrentSkin(self.portal.REQUEST)


    def publishPages(self):
        portal = self.portal
        request = self.portal.REQUEST
        catalog = portal.portal_catalog
        alsoProvides(request, IDisableCSRFProtection)


        brain = api.content.find(context=portal, Type="Page", review_state="private")
        for item in brain:
            print item.getURL()
            api.content.transition(obj=item.getObject(), transition='publish')
            transaction.commit()



instance = ToPublished(sys.argv[3], sys.argv[4])
#instance.addKeywords(sys.argv[5])
#instance.copyContents(sys.argv[5])
instance.publishPages()
