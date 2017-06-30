# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import common as base
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from DateTime import DateTime
from datetime import datetime
import MySQLdb

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

        # 順便統計
        if context.Type() in ['Plone Site', 'Cover', 'Folder', 'Image', 'File']:
            return

        uid = context.UID()
        today = DateTime().strftime('%Y/%m/%d')
        db = MySQLdb.connect(host='localhost', user='klland', passwd='klland', db='klland')
        cursor = db.cursor()

        sqlStr = "UPDATE `kl_counter` SET `count` = count + 1 WHERE date = '%s' AND uid = '%s'" % (today, uid)

        if cursor.execute(sqlStr) == 0:
            sqlStr = "INSERT INTO kl_counter(uid, date, count) VALUES ('%s', '%s', 1) \
                 ON DUPLICATE KEY UPDATE count = count + 1;" % (uid, today)
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
