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
#import html2text
import urllib2
import logging
import json

# howto: bin/client1 run pathtofile/import_news.py portal_name admin_id news_site_code(ex. bbc)
# mapping: sys.argv[3] is portal_name, sys.argv[4] is admin_id, sys.argv[5] is news_site_code
#          sys.argv[6] is dataType, 'xml', 'html' ...

news_site_code = {
    'bbc':'http://feeds.bbci.co.uk/zhongwen/trad/rss.xml',
    'youtube_radio':'https://www.youtube.com/playlist?list=PL7rBJWuEBrPYJCcxbTI-qTzuEEmiCCDXX',
    'liveProgram_1':'http://tv.mingjingnet.com/playlist_svr1.json',
    'liveProgram_2':'http://tv.mingjingnet.com/playlist_svr2.json',
}

logger = logging.getLogger('Import News')



class ImportNews:

    def __init__(self, portal, admin, type):
        root = makerequest.makerequest(app)
        self.portal = getattr(root, portal, None)

        admin = root.acl_users.getUserById(admin)
        admin = admin.__of__(self.portal.acl_users)
        newSecurityManager(None, admin)
        setHooks()
        setSite(self.portal)
        self.portal.setupCurrentSkin(self.portal.REQUEST)

        self.type = type


    def remove_oldnews(self):
        portal = self.portal
        request = self.portal.REQUEST
        catalog = portal.portal_catalog
        alsoProvides(request, IDisableCSRFProtection)

#        if self.type == 'news':
        self.type = 'News Item'

        brain = api.content.find(container=portal, Type=self.type)
#        import pdb; pdb.set_trace()
        count = 0
        for item in brain:
            api.content.delete(obj=item.getObject())
#            import pdb; pdb.set_trace()
            count += 1
            if count % 10 == 0:
                transaction.commit()
                print 'delete: %s' % count
#        import pdb; pdb.set_trace()
        transaction.commit()




instance = ImportNews(sys.argv[3], sys.argv[4], sys.argv[5])
instance.remove_oldnews()
