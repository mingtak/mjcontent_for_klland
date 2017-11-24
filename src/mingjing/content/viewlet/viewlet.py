# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from DateTime import DateTime
from datetime import datetime
from Products.CMFPlone.utils import safe_unicode
import MySQLdb
import logging

logger = logging.getLogger('mingjing.content')

LIMIT = 10


class RwdMenu(base.ViewletBase):
    """  """


class ScriptToFooter(base.ViewletBase):
    """  """


class AboveContentInfo(base.ViewletBase):
    """  """


class SocialList(base.ViewletBase):
    """  """
    def update(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
#統計
        http_referer = request.get('HTTP_REFERER')
        if not http_referer.startswith('http://land.klcg.gov.tw'):
            return

        url = request.form.get('url')
        postTitle = request.form.get('title')
        if not (url and postTitle):
            return

        today = DateTime().strftime('%Y/%m/%d')
        db = MySQLdb.connect(host='localhost', user='klland', passwd='klland', db='klland')
        cursor = db.cursor()
#編碼
        cursor.execute("SET NAMES utf8")


        sqlStr = "UPDATE kl_counter SET count = count + 1 WHERE date = '%s' AND url = '%s'" % (today, url)

        if cursor.execute(sqlStr) == 0:
            sqlStr = "INSERT INTO kl_counter(url, postTitle, date, count) VALUES ('%s', '%s', '%s', 1) \
                 ON DUPLICATE KEY UPDATE count = count + 1;" % (url, postTitle, today)
            cursor.execute(sqlStr)
        db.commit()
        db.close()


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
