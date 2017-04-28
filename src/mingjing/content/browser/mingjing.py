# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
import json
from datetime import datetime
from DateTime import DateTime
import transaction
from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from .views import CoverView

LIMIT = 20


class MingjingFolder(BrowserView):

    def __call__(self):
        return self.template()


class MingjingNews(MingjingFolder):
    template = ViewPageTemplateFile('template/mingjing_news.pt')


class SetFeatured(BrowserView):

    def __call__(self):
        portal = api.portal.get()
        request = self.request

        if not request.form.get('uid'):
            return
        brain = api.content.find(context=portal, UID=request.form['uid'])
        try:
            item = brain[0].getObject()
        except:return

        if request.form.has_key('checked'):
            if request.form.get('checked') == 'true':
                item.featured = True
            else:
                item.featured = False
            notify(ObjectModifiedEvent(item))
            item.reindexObject()
        elif request.form.has_key('headWeight'):
            item.headWeight = int(request.form.get('headWeight', 10))
            notify(ObjectModifiedEvent(item))
            item.reindexObject()
        transaction.commit()
        return
