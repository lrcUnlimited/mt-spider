# -*- coding: utf-8 -*-

import logging
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import logging
import MySQLdb
import MySQLdb.cursors


class FilterWordsPipeline(object):
    """a pipline to drop item whose point<4"""

    def process_item(self, item, spider):
        point = item.get('point')
        if point < 4:
            raise DropItem("point is: %s and drop it" % point)
        else:
            return item



class MySQLStorePipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect(db='mtdb',
                                    user='root', passwd='19901023', cursorclass=MySQLdb.cursors.DictCursor,
                                    charset='utf8', use_unicode=False)
        self.cursor = self.conn.cursor()



    def process_item(self, item, spider):
        try:
            sql = "insert into shopdetail(point,shopName,address,shoptype,consume_num,judge_num,url)values (%s, %s,%s,%s, %s,%s,%s)"
            self.cursor.execute(sql,
                                (item['point'], item['shopName'], item['address'], item['type'], item['consume_num'],
                                 item['judge_num'],
                                 item['url']))
            self.conn.commit()


        except MySQLdb.Error, e:
            print '!!!!!!!!!!!!!!!!!!DB Write failure!!!!!!!!!!!!'
            print "Error %d: %s" % (e.args[0], e.args[1])

        return item


"""


class MySQLStorePipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb', db='mtdb',
                                            user='root', passwd='19901023', cursorclass=MySQLdb.cursors.DictCursor,
                                            charset='utf8', use_unicode=False)


    def process_item(self, item, spider):
        # run db query in thread pool
        query = self.dbpool.runInteraction(self._conditional_insert, item)

        query.addErrback(self.handle_error)

        return item


    def _conditional_insert(self, tx, item):
        sql = "insert into shopdetail(point,shopName,address,shoptype,consume_num,judge_num,url)values (%s, %s,%s,%s, %s,%s,%s)"
        tx.execute(sql,
                   (item['point'], item['shopName'], item['address'], item['type'], item['consume_num'],
                    item['judge_num'],
                    item['url']))

        logging.msg("Item stored in db: %s" % item, level=logging.DEBUG)


    def handle_error(self, e):
        logging.err(e)

"""

