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
LIMIT=20


class GetHot(BrowserView):

    def __call__(self):

        db = MySQLdb.connect(host='localhost', user='klland', passwd='klland', db='klland')

        startDayStr = (DateTime()-30).strftime('%Y-%m-%d')

        cursor = db.cursor()
#編碼
        cursor.execute("SET NAMES utf8")
        statSql = "SELECT postTitle, url \
                   FROM kl_counter \
                   WHERE date > '%s' \
                   ORDER BY count DESC LIMIT 5" % (startDayStr)
        cursor.execute(statSql)
        result = cursor.fetchall()

#        import pdb; pdb.set_trace()

        try:
            pass
#            logger.info(result)
        except:
            logger.info('result type: %s' % type(result))
        jsonStr = json.dumps(result)
        self.request.RESPONSE.setHeader('Content-Type', 'application/json')
        self.request.RESPONSE.setHeader('X-Content-Type-Options', '')
        return 'jsonStr(%s)' % jsonStr


class Rank(BrowserView):

    template = ViewPageTemplateFile("template/rank.pt")

    def loadFile(self, filename):
        try:
            with open('/tmp/%s' % filename) as file:
                return pickle.load(file)
        except:
            return None


    def statResult(self, result):
        rank = {}
        for item in result:
            if rank.has_key(item[0]):
                rank[item[0]] += item[1]
            else:
                rank[item[0]] = item[1]

        sortedRank = sorted(rank.items(), key=operator.itemgetter(1))
        sortedRank.reverse()
        return sortedRank


    def __call__(self):

        request = self.request
        range = request.get('range', 'Today')
        todayStr = DateTime().strftime('%Y-%m-%d')

        if range in ['Today', 'Week', 'Month'] and not request.form.has_key('start'):
            self.result = self.loadFile('stat%s' % range)[:20]
            self.end = todayStr
            if range == 'Today':
                self.start = todayStr
            if range == 'Week':
                self.start = (DateTime() - 7).strftime('%Y-%m-%d')
            if range == 'Month':
                self.start = (DateTime() - 30).strftime('%Y-%m-%d')
            return self.template()

        db = MySQLdb.connect(host='localhost', user='klland', passwd='klland', db='klland')
        self.start = request.get('start', todayStr)
        self.end = request.get('end', todayStr)

        if not self.start:
            self.start = todayStr
        if not self.end:
            self.end = todayStr

        cursor = db.cursor()
#        statSql = "SELECT `uid`, `count` FROM `kl_counter` WHERE `date` BETWEEN '%s' AND '%s' ORDER BY `uid` LIMIT 20" % (self.start, self.end)
        statSql = "SELECT url, postTitle, count \
                   FROM kl_counter \
                   WHERE date BETWEEN '%s' AND '%s' \
                   ORDER BY count DESC LIMIT 20" % (self.start, self.end)
        cursor.execute(statSql)
        self.result = cursor.fetchall()
#        import pdb;pdb.set_trace()
#        self.result = self.statResult(self.result)

        db.close()
#        self.request.RESPONSE.setHeader('Content-Type', 'text/html; charset=utf-8')
#        self.request.RESPONSE.setHeader('X-Content-Type-Options', '')
#        self.request.RESPONSE.setHeader('X-Frame-Options', 'ALLOW-FROM http://218.161.124.132/')

        return self.template()


class ShowFeatured(BrowserView):

    template = ViewPageTemplateFile("template/show_featured.pt")

    def __call__(self):
        portal = api.portal.get()
        self.brain = api.content.find(context=portal, featured=True, sort_on='created', sort_order='reverse', sort_limit=LIMIT)[:LIMIT]
        return self.template()


class NewestContents(BrowserView):

    template = ViewPageTemplateFile("template/newest_contents.pt")

    def __call__(self):
        return self.template()


class ToYoutube(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        request.response.redirect(context.youtubeURL)
        return


class YoutubeView(BrowserView):

    template = ViewPageTemplateFile("template/youtube_view.pt")

    def __call__(self):
        return self.template()


class BlogView(BrowserView):

    template = ViewPageTemplateFile("template/blog_view.pt")

    def __call__(self):
        return self.template()


class EbookView(BrowserView):

    template = ViewPageTemplateFile("template/ebook_view.pt")

    def __call__(self):
        return self.template()


class CoverView(BrowserView):

    template = ViewPageTemplateFile("template/cover_view.pt")
    date_range = {
        'query': (
            DateTime()-1,
        ),
        'range': 'min',
    }

#    @ram.cache(lambda *args: time() // (120))
    def mainSliders(self):
        context = self.context
        portal = api.portal.get()
#        items = context.getChildNodes()
        brain = portal['resource']['headimage'].restrictedTraverse('@@contentlisting')(portal_type='Image')
#        brain = api.content.find(Type=['News Item'], review_state='published',
#                                featured=True, sort_on='headWeight', sort_order='reverse')
#        import pdb; pdb.set_trace()
        return brain


    #@ram.cache(lambda *args: time() // (120))
    def youtubes(self):
        portal = api.portal.get()
        return api.content.find(context=portal, Type='Youtube', featured=True, review_state='published', sort_on='created', sort_order='reverse', sort_limit=LIMIT)[:LIMIT]


    def externalAd(self):
        portal = api.portal.get()
        return portal['resource']['ad'].restrictedTraverse('@@contentlisting')(Type='Ad', category='external')


    #@ram.cache(lambda *args: time() // (120))
    def todayNews(self):
        portal = api.portal.get()
        brain = api.content.find(context=portal, Type='News Item', hasOldPicture=True, featured=True, review_state='published', sort_on='created', sort_order='reverse', sort_limit=LIMIT)[:LIMIT]
        return brain

    #@ram.cache(lambda *args: time() // (120))
    def tabsNameLists(self):
        portal = api.portal.get()
        context = self.context

        tabsNameList_1 = ['最新消息', '法令新訊'] #, '線上查詢', '線上申辦']
        tabsNameList_2 = ['不動產經紀 仲介專區', '基隆市實價登錄專區', '徵收案件專區']
        tabsNameList_3 = ['none']

        tabsBrain_1, tabsBrain_2 ,tabsBrain_3 = [], [], []

        # 最新消息
        brain_news = api.content.find( context=portal['news']['1'], Type='Page', review_state='published',
            sort_on='headWeight', sort_order='reverse', sort_limit=5)[:5]

        # 法令新訊
        brain_law = api.content.find( context=portal['inquiry']['1'], Type='Page', review_state='published',
            sort_on='headWeight', sort_order='reverse', sort_limit=5)[:5]

        # 線上查詢
#        brain_inquery = api.content.find( context=portal['3'], Type='Page', review_state='published', featured=True,
#            sort_on='headWeight', sort_order='reverse', sort_limit=10)[:10]

        # 線上申辦
#        brain_bid = api.content.find( context=portal['4'], Type='Link', review_state='published', featured=True,
#            sort_on='headWeight', sort_order='reverse', sort_limit=10)[:10]

        # 不動產經紀 仲介專區
        brain_broker = api.content.find( context=portal['business']['8'], Type='Page', review_state='published',
            sort_on='headWeight', sort_order='reverse', sort_limit=10)[:10]

        # 基隆市實價登錄專區
        brain_realprice = api.content.find( context=portal['business']['6'], Type='Page', review_state='published',
            sort_on='headWeight', sort_order='reverse', sort_limit=10)[:10]

        # 徵收案件專區
        brain_buy = api.content.find( context=portal['business']['9'], Type='Page', review_state='published',
            sort_on='headWeight', sort_order='reverse', sort_limit=10)[:10]

        # 合併 brain
        tabsBrain_1 = [brain_news, brain_law] #, brain_inquery, brain_bid]
        tabsBrain_2 = [brain_broker, brain_realprice, brain_buy]
        tabsBrain_3 = []

        return [tabsNameList_1, tabsBrain_1, tabsNameList_2, tabsBrain_2, tabsNameList_3, tabsBrain_3]


    #@ram.cache(lambda *args: time() // (120))
    def ebooks(self):
        portal = api.portal.get()
        context = self.context
        newestBook = api.content.find(context=portal, Type='Ebook', id=context.ebooks.split()[0])[0]
        hotestBook = api.content.find(context=portal, Type='Ebook', id=context.ebooks.split()[1])[0]
        eBook = api.content.find(context=portal, Type='Ebook', id=context.ebooks.split()[2])[0]
        return [newestBook, hotestBook, eBook]


    #@ram.cache(lambda *args: time() // (120))
    def rankingNews(self):
        portal = api.portal.get()
        context = self.context
        brain = api.content.find(context=portal, Type='News Item', featured=True, sort_on='created', sort_order='reverse', sort_limit=LIMIT)[:LIMIT]
        return brain


    #@ram.cache(lambda *args: time() // (120))
    def liveProgram(self, jsonString):
        context = self.context
        liveProgram = json.loads(jsonString)
        startTime = int(liveProgram['startTime'])

        while True:
            endTime = startTime
            for item in liveProgram['pl']:
                endTime += item['during']
            if datetime.fromtimestamp(endTime) < datetime.now():
                startTime = endTime + 1
            else:
                break

        for item in liveProgram['pl']:
            item['start'] = datetime.fromtimestamp(startTime)
            item['end'] = datetime.fromtimestamp(startTime+item['during'])
            startTime += item['during']

        while True:
            if liveProgram['pl'][0]['end'] < datetime.now():
                tmp = liveProgram['pl'].pop(0)
                liveProgram['pl'].append(tmp)
            else:
                break

        return liveProgram['pl']


    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()

        return self.template()


class TransState(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
#        import pdb; pdb.set_trace()
        uid = request.form.get('uid')
        if not uid:
            return

        obj = api.content.find(UID=uid)[0].getObject()
        state = api.content.get_state(obj=obj)
        if state == 'published':
            api.content.transition(obj=obj, transition='reject')
        else:
            api.content.transition(obj=obj, transition='publish')


class DeleteObj(BrowserView):

    def __call__(self):
        context = self.context
        request = self.request
        portal = api.portal.get()
#        import pdb; pdb.set_trace()
        uid = request.form.get('uid')
        if not uid:
            return

        obj = api.content.find(UID=uid)[0].getObject()
        api.content.delete(obj=obj)


class NormalView(BrowserView):

    template = ViewPageTemplateFile("template/normal_view.pt")

    def __call__(self):
        return self.template()
