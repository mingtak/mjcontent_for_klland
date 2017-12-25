# -*- coding: utf-8 -*-
import sys
import random
#import html2text
import MySQLdb
import operator
from datetime import datetime, date, timedelta
import pickle


class StatSql:

    def __init__(self):

        self.db = MySQLdb.connect(host='localhost', user='klland', passwd='klland', db='klland')


    def statSql(self):
        today = date.today().strftime('%Y/%m/%d')
        yesterday = (date.today() - timedelta(1)).strftime('%Y/%m/%d')
        weekAgo = (date.today() - timedelta(7)).strftime('%Y/%m/%d')
        monthAgo = (date.today() - timedelta(30)).strftime('%Y/%m/%d')

        cursor = self.db.cursor()
        cursor.execute("SET NAMES utf8")
        statToday = "SELECT url, postTitle, sum(count) as count \
                     FROM `kl_counter` \
                     WHERE date >= '%s' \
                     GROUP BY url, postTitle \
                     ORDER BY count DESC" % today

        statWeek = "SELECT url, postTitle, sum(count) as count \
                    FROM `kl_counter` \
                    WHERE date >= '%s' \
                    GROUP BY url, postTitle \
                    ORDER BY count DESC" % weekAgo

        statMonth = "SELECT url, postTitle, sum(count) as count \
                     FROM `kl_counter` \
                     WHERE date >= '%s' \
                     GROUP BY url, postTitle \
                     ORDER BY count DESC" % monthAgo

        cursor.execute(statToday)
        todayResult = cursor.fetchall()
        cursor.execute(statWeek)
        weekResult = cursor.fetchall()
        cursor.execute(statMonth)
        monthResult = cursor.fetchall()

        if todayResult:
            self.statResult(todayResult, 'statToday')
        if weekResult:
            self.statResult(weekResult, 'statWeek')
        if monthResult:
            self.statResult(monthResult, 'statMonth')


    def statResult(self, result, filename):
        """
        rank = {}
        for item in result:
            if rank.has_key(item[0]):
                rank[item[0]] += item[1]
            else:
                rank[item[0]] = item[1]
        """

#        sortedRank = sorted(rank.items(), key=operator.itemgetter(1))
#        sortedRank.reverse()

        with open('/tmp/%s' % filename, 'w') as file:
#            pickle.dump(sortedRank, file)
            pickle.dump(result, file)


instance = StatSql()
instance.statSql()
