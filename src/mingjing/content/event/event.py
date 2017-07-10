# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from plone import api
from DateTime import DateTime
import transaction
import MySQLdb


"""
def editFinished(item, event):
    item.cateL1 = item.REQUEST.form['cate_l1']
    item.cateL2 = item.REQUEST.form['cate_l2']
#    import pdb; pdb.set_trace()
"""

def toFolderContents(item, event):
    try:
        portal = api.portal.get()
    except:return
    try:
        parent = item.getParentNode()
    except:
        portal.REQUEST.response.redirect('%s/folder_contents' % portal.absolute_url())

    try:
        if item.Type() in ['Image', 'File']:
            return
        if item.Type() == 'Folder':
            item.REQUEST.response.redirect('%s/folder_contents' % item.absolute_url())
        else:
            item.REQUEST.response.redirect('%s/folder_contents' % parent.absolute_url())
    except:
        portal.REQUEST.response.redirect('%s/folder_contents' % portal.absolute_url())


def moveContentToTop(item, event):
    """ Moves Item to the top of its folder """
    try:
        folder = item.getParentNode()
    except:
        return
    if not hasattr(folder, 'moveObjectsToTop'):
        return

    if item.portal_type not in ['File', 'Image']:
        try:
            folder.moveObjectsToTop(item.id)
        except:pass


def userLoginToFolderContents(event):
    portal = api.portal.get()
    current = api.user.get_current()
#    if api.user.has_permission('Modify portal content', user=current):
    portal.REQUEST.response.redirect('%s/folder_contents' % portal.absolute_url())


def addCancelToFolderContents(item, event):
    item.REQUEST.response.redirect('%s/folder_contents' % item.absolute_url())


def willBeRemoved(event):
    try:
        item = event.object
        uid = item.UID()
        db = MySQLdb.connect(host='localhost', user='klland', passwd='klland', db='klland')
        cursor = db.cursor()
        sqlStr = "DELETE FROM `kl_counter` WHERE uid='%s'" % uid
        cursor.execute(sqlStr)
        db.commit()
        db.close()
    except:pass


def logToContent(item, event):

    if hasattr(item, 'contentLog'):
        if 'EditFinished' in str(event):
            eventName = safe_unicode('編輯')
        else:
            eventName = safe_unicode('新增')
        logStr = '%s,%s,%s' % (DateTime().strftime('%Y/%m/%d %H:%M:%S'), api.user.get_current().id, eventName)
        if item.contentLog is None:
            item.contentLog = []
        item.contentLog.insert(0, logStr)
