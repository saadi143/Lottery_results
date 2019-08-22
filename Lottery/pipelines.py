# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from mysql.connector import errorcode
import datetime


#######################################
#       EuroMillion Lottery           #
#######################################

class LotteryPipeline(object):
    def __init__(self):
        self.createconnection()

    def createconnection(self):
        try:
            self.conn = mysql.connector.connect(host = 'giow16.siteground.us', user = 'aliarsha_result',
                                                passwd = 'Burewalla ', database = 'aliarsha_Lottery')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.curr = self.conn.cursor()

    def connectionClose(self):
        if (self.conn.is_connected()):
            self.curr.close()
            self.conn.close()

    def process_item(self, item, spider):
        if (spider.name == 'Euromillion'):
            self.euroResuslt(item)
            return item

    def euroResuslt(self, item):
        # print(item['date'])

        self.curr.execute(
            """Select lottery_date_id from lottery_date where lottery_name_id = %s AND lottery_date = %s""", (
                1,
                item['date']
            ))
        row_data = self.curr.fetchall()
        row_count = self.curr.rowcount
        date_id = None
        # Check if date is not exist in table
        if row_count == 0:
            # print("IN: ", item['date'])

            # Insert the date and draw
            self.curr.execute(
                """INSERT INTO lottery_date(lottery_name_id, lottery_date,lottery_draw_number) VALUES (%s,%s,%s)""", (
                    1,
                    item['date'],
                    item['draw_number'].replace(',', '')
                ))
            date_id = self.curr.lastrowid

            perma = "Euromillions-results-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
            # insert draw_numbers
            self.curr.execute(
                "INSERT INTO lottery_draw(lottery_date_id, lottery_name_id, draw_1,draw_2,draw_3,draw_4,draw_5,draw_6,draw_7,permalinks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    date_id,
                    1,
                    item['draw_1'],
                    item['draw_2'],
                    item['draw_3'],
                    item['draw_4'],
                    item['draw_5'],
                    item['draw_6'],
                    item['draw_7'],
                    perma
                ))
            draw_id = self.curr.lastrowid

            # Insert Maker Result
            self.curr.execute(
                "INSERT INTO maker_results(lottery_draw, maker_results) VALUES (%s,%s)",
                (
                    draw_id,
                    item['maker_result']
                ))
            # Insert the prize breakdown
            for i in range(len(item['match'])):
                self.curr.execute(
                    "INSERT INTO lottery_prize(lottery_draw_id, draw_match, draw_star, winner, prize, total) VALUES (%s,%s,%s,%s,%s,%s)",
                    (
                        draw_id,
                        item['match'][i],
                        item['star'][i],
                        item['winner'][i],
                        item['prize'][i],
                        item['total'][i]
                    ))
            self.curr.execute(
                "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                (
                    datetime.date.today(),
                    2
                ))
            self.conn.commit()
            print("Row Inserted.")
        elif (row_count == 1):
            date_id = row_data[0][0]
            # Insert the date and draw
            self.curr.execute(
                """Select * from lottery_draw where lottery_name_id = %s AND lottery_date_id = %s""", (
                    1,
                    date_id
                ))
            row_data_draw = self.curr.fetchall()
            row_count_draw = self.curr.rowcount

            if row_count_draw == 0:

                perma = "Euromillions-results-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
                # insert draw_numbers
                self.curr.execute(
                    "INSERT INTO lottery_draw(lottery_date_id, lottery_name_id, draw_1,draw_2,draw_3,draw_4,draw_5,draw_6,draw_7,permalinks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        date_id,
                        1,
                        item['draw_1'],
                        item['draw_2'],
                        item['draw_3'],
                        item['draw_4'],
                        item['draw_5'],
                        item['draw_6'],
                        item['draw_7'],
                        perma
                    ))
                draw_id = self.curr.lastrowid

                # Insert Maker Result
                self.curr.execute(
                    "INSERT INTO maker_results(lottery_draw, maker_results) VALUES (%s,%s)",
                    (
                        draw_id,
                        item['maker_result']
                    ))
                # Insert the prize breakdown
                for i in range(len(item['match'])):
                    self.curr.execute(
                        "INSERT INTO lottery_prize(lottery_draw_id, draw_match, draw_star, winner, prize, total) VALUES (%s,%s,%s,%s,%s,%s)",
                        (
                            draw_id,
                            item['match'][i],
                            item['star'][i],
                            item['winner'][i],
                            item['prize'][i],
                            item['total'][i]
                        ))
                self.curr.execute(
                    "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                    (
                        datetime.date.today(),
                        2
                    ))
                self.conn.commit()
                print("Row Inserted.")
            else:
                print("Draw Numbers are exists in table")


#######################################
#       Lotto Lottery                 #
#######################################
class Lotto(object):

    def __init__(self):
        self.createconnection()

    def createconnection(self):
        try:
            self.conn = mysql.connector.connect(host = 'giow16.siteground.us', user = 'aliarsha_result',
                                                passwd = 'Burewalla ', database = 'aliarsha_Lottery')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.curr = self.conn.cursor()

    def connectionClose(self):
        if (self.conn.is_connected()):
            self.curr.close()
            self.conn.close()

    def process_item(self, item, spider):
        if (spider.name == 'Lotto'):
            self.lottoResuslt(item)
            return item

    def lottoResuslt(self, item):

        self.curr.execute("""Select * from lottery_date where lottery_name_id = %s AND lottery_date = %s""", (
            102,
            item['date']
        ))
        row_data = self.curr.fetchall()
        row_count = self.curr.rowcount
        date_id = None
        # Check if date is not exist in table
        if row_count == 0:

            # Insert the date and draw
            self.curr.execute(
                """INSERT INTO lottery_date(lottery_name_id, lottery_date,lottery_draw_number) VALUES (%s,%s,%s)""", (
                    102,
                    item['date'],
                    item['draw_number'].replace(',', '')
                ))
            date_id = self.curr.lastrowid

            perma = "Lotto-results-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
            # insert draw_numbers
            self.curr.execute(
                "INSERT INTO lottery_draw(lottery_date_id, lottery_name_id, draw_1,draw_2,draw_3,draw_4,draw_5,draw_6,draw_7,permalinks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    date_id,
                    102,
                    item['draw_1'],
                    item['draw_2'],
                    item['draw_3'],
                    item['draw_4'],
                    item['draw_5'],
                    item['draw_6'],
                    item['draw_7'],
                    perma
                ))
            draw_id = self.curr.lastrowid

            # Insert the prize breakdown
            for i in range(len(item['match'])):
                self.curr.execute(
                    "INSERT INTO lottery_prize(lottery_draw_id, draw_match, draw_star, winner, prize, total) VALUES (%s,%s,%s,%s,%s,%s)",
                    (
                        draw_id,
                        item['match'][i],
                        item['star'][i],
                        item['winner'][i],
                        item['prize'][i],
                        item['total'][i]
                    ))
            self.curr.execute(
                "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                (
                    datetime.date.today(),
                    3
                ))
            self.conn.commit()
            print("Row Inserted")

        elif row_count == 1:
            date_id = row_data[0][0]
            # Insert the date and draw
            self.curr.execute(
                """Select * from lottery_draw where lottery_name_id = %s AND lottery_date_id = %s""", (
                    102,
                    date_id
                ))
            row_data_draw = self.curr.fetchall()
            row_count_draw = self.curr.rowcount

            if row_count_draw == 0:

                perma = "Lotto-results-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
                # insert draw_numbers
                self.curr.execute(
                    "INSERT INTO lottery_draw(lottery_date_id, lottery_name_id, draw_1,draw_2,draw_3,draw_4,draw_5,draw_6,draw_7,permalinks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (
                        date_id,
                        102,
                        item['draw_1'],
                        item['draw_2'],
                        item['draw_3'],
                        item['draw_4'],
                        item['draw_5'],
                        item['draw_6'],
                        item['draw_7'],
                        perma
                    ))
                draw_id = self.curr.lastrowid

                # Insert the prize breakdown
                for i in range(len(item['match'])):
                    self.curr.execute(
                        "INSERT INTO lottery_prize(lottery_draw_id, draw_match, draw_star, winner, prize, total) VALUES (%s,%s,%s,%s,%s,%s)",
                        (
                            draw_id,
                            item['match'][i],
                            item['star'][i],
                            item['winner'][i],
                            item['prize'][i],
                            item['total'][i]
                        ))
                self.curr.execute(
                    "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                    (
                        datetime.date.today(),
                        3
                    ))
                self.conn.commit()
                print("Row Inserted")
            else:
                print("Draw Numbers are exists in table")


#######################################
#       Health Lottery                #
#######################################

class Health(object):
    def __init__(self):
        self.createconnection()

    def createconnection(self):
        try:
            self.conn = mysql.connector.connect(host = 'giow16.siteground.us', user = 'aliarsha_result',
                                                passwd = 'Burewalla ', database = 'aliarsha_Lottery')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.curr = self.conn.cursor()

    def connectionClose(self):
        if (self.conn.is_connected()):
            self.curr.close()
            self.conn.close()

    def process_item(self, item, spider):
        if (spider.name == 'Health'):
            self.healthResult(item)
            return item

    def healthResult(self, item):
        self.curr.execute("""Select * from lottery_date where lottery_name_id = %s AND lottery_date = %s""", (
            104,
            item['date']
        ))
        row_data = self.curr.fetchall()
        row_count = self.curr.rowcount

        # Check if date is not exist in table
        if row_count == 0:

            # Insert the date and draw
            self.curr.execute(
                """INSERT INTO lottery_date(lottery_name_id, lottery_date,lottery_draw_number) VALUES (%s,%s,%s)""", (
                    104,
                    item['date'],
                    item['draw_number'].replace(',', '')
                ))
            date_id = self.curr.lastrowid

            perma = "Health-results-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
            # insert draw_numbers
            self.curr.execute(
                "INSERT INTO lottery_draw(lottery_date_id, lottery_name_id, draw_1,draw_2,draw_3,draw_4,draw_5,draw_6,draw_7,permalinks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    date_id,
                    104,
                    item['draw_1'],
                    item['draw_2'],
                    item['draw_3'],
                    item['draw_4'],
                    item['draw_5'],
                    item['draw_6'],
                    item['draw_7'],
                    perma
                ))
            draw_id = self.curr.lastrowid

            # Insert the prize breakdown
            for i in range(len(item['match'])):
                self.curr.execute(
                    "INSERT INTO lottery_prize(lottery_draw_id, draw_match, draw_star, winner, prize, total) VALUES (%s,%s,%s,%s,%s,%s)",
                    (
                        draw_id,
                        item['match'][i],
                        item['star'][i],
                        item['winner'][i],
                        item['prize'][i],
                        item['total'][i]
                    ))
            self.curr.execute(
                "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                (
                    datetime.date.today(),
                    6
                ))
            self.conn.commit()
            print("Row Inserted")

        else:
            print("Date Exist in table")


#######################################
#       Set-For-Life Lottery          #
#######################################

class Life(object):
    def __init__(self):
        self.createconnection()

    def createconnection(self):
        try:
            self.conn = mysql.connector.connect(host = 'giow16.siteground.us', user = 'aliarsha_result',
                                                passwd = 'Burewalla ', database = 'aliarsha_Lottery')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.curr = self.conn.cursor()

    def connectionClose(self):
        if (self.conn.is_connected()):
            self.curr.close()
            self.conn.close()

    def process_item(self, item, spider):
        if (spider.name == 'SetForLife'):
            self.lifeResuslt(item)
            return item

    def lifeResuslt(self, item):
        self.curr.execute("""Select * from lottery_date where lottery_name_id = %s AND lottery_date = %s""", (
            105,
            item['date']
        ))
        row_data = self.curr.fetchall()
        row_count = self.curr.rowcount

        # Check if date is not exist in table
        if row_count == 0:

            # Insert the date and draw
            self.curr.execute(
                """INSERT INTO lottery_date(lottery_name_id, lottery_date,lottery_draw_number) VALUES (%s,%s,%s)""", (
                    105,
                    item['date'],
                    item['draw_number'].replace(',', '')
                ))
            date_id = self.curr.lastrowid

            perma = "Set-for-life-results-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
            # insert draw_numbers
            self.curr.execute(
                "INSERT INTO lottery_draw(lottery_date_id, lottery_name_id, draw_1,draw_2,draw_3,draw_4,draw_5,draw_6,draw_7,permalinks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    date_id,
                    105,
                    item['draw_1'],
                    item['draw_2'],
                    item['draw_3'],
                    item['draw_4'],
                    item['draw_5'],
                    item['draw_6'],
                    item['draw_7'],
                    perma
                ))
            draw_id = self.curr.lastrowid

            # Insert the prize breakdown
            for i in range(len(item['match'])):
                self.curr.execute(
                    "INSERT INTO lottery_prize(lottery_draw_id, draw_match, draw_star, winner, prize, total) VALUES (%s,%s,%s,%s,%s,%s)",
                    (
                        draw_id,
                        item['match'][i],
                        item['star'][i],
                        item['winner'][i],
                        item['prize'][i],
                        item['total'][i]
                    ))
            self.curr.execute(
                "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                (
                    datetime.date.today(),
                    5
                ))

            self.conn.commit()

        else:
            print("Date Exist in table")


#######################################
#       Thunderball Lottery           #
#######################################

class Thunderball(object):
    def __init__(self):
        self.createconnection()

    def createconnection(self):
        try:
            self.conn = mysql.connector.connect(host = 'giow16.siteground.us', user = 'aliarsha_result',
                                                passwd = 'Burewalla ', database = 'aliarsha_Lottery')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.curr = self.conn.cursor()

    def connectionClose(self):
        if (self.conn.is_connected()):
            self.curr.close()
            self.conn.close()

    def process_item(self, item, spider):
        if (spider.name == 'Thunderball'):
            self.thunderResuslt(item)
            return item

    def thunderResuslt(self, item):
        self.curr.execute("""Select * from lottery_date where lottery_name_id = %s AND lottery_date = %s""", (
            103,
            item['date']
        ))
        row_data = self.curr.fetchall()
        row_count = self.curr.rowcount

        # Check if date is not exist in table
        if row_count == 0:

            # Insert the date and draw
            self.curr.execute(
                """INSERT INTO lottery_date(lottery_name_id, lottery_date,lottery_draw_number) VALUES (%s,%s,%s)""", (
                    103,
                    item['date'],
                    item['draw_number'].replace(',', '')
                ))
            date_id = self.curr.lastrowid

            perma = "Thunderball-results-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
            # insert draw_numbers
            # print("ID : ", str(date_id))
            # print("perma : ", perma)
            self.curr.execute(
                "INSERT INTO lottery_draw(lottery_date_id, lottery_name_id, draw_1,draw_2,draw_3,draw_4,draw_5,draw_6,draw_7,permalinks) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (
                    date_id,
                    103,
                    item['draw_1'],
                    item['draw_2'],
                    item['draw_3'],
                    item['draw_4'],
                    item['draw_5'],
                    item['draw_6'],
                    item['draw_7'],
                    perma
                ))
            draw_id = self.curr.lastrowid

            # Insert the prize breakdown
            for i in range(len(item['match'])):
                self.curr.execute(
                    "INSERT INTO lottery_prize(lottery_draw_id, draw_match, draw_star, winner, prize, total) VALUES (%s,%s,%s,%s,%s,%s)",
                    (
                        draw_id,
                        item['match'][i],
                        item['star'][i],
                        item['winner'][i],
                        item['prize'][i],
                        item['total'][i]
                    ))
            self.curr.execute(
                "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                (
                    datetime.date.today(),
                    4
                ))
            self.conn.commit()
            print("Row Inserted")

        else:
            print("Date Exist in table")


#######################################
#       Euro Hotpicks Lottery         #
#######################################

class EuroHotpicks(object):
    def __init__(self):
        self.createconnection()

    def __del__(self):
        self.connectionClose()

    def createconnection(self):
        try:
            self.conn = mysql.connector.connect(host = 'giow16.siteground.us', user = 'aliarsha_result',
                                                passwd = 'Burewalla ', database = 'aliarsha_Lottery')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.curr = self.conn.cursor(buffered = True)

    def connectionClose(self):
        if (self.conn.is_connected()):
            # self.curr.close()
            self.conn.close()

    def process_item(self, item, spider):
        if (spider.name == 'EuroHotpicks'):
            # print(item['date'])
            self.euroHotResult(item)
            return item

    def euroHotResult(self, item):

        # (item['date'])
        self.curr.execute(
            """Select lottery_date_id from lottery_date where lottery_name_id = %s AND lottery_date = %s""", (
                1,
                item['date']
            ))
        row_data = self.curr.fetchall()
        row_count = self.curr.rowcount
        # print("Record")
        # for x in row_data[0]:
        #     print(x)
        # print(row_count)
        # Check if date is  exist in table
        if row_count == 1:
            date_id = row_data[0][0]
            # print("DATE" + str(item['date']))
            # print("ID")
            # print(date_id)
            # Check for the prize breakdown is already in table
            self.curr.execute("""Select hottpicks_prize_id from hottpicks_prize where hottpicks_draw_id = %s""", (
                date_id,
            ))
            prize_data = self.curr.fetchone()
            prize_count = self.curr.rowcount

            if prize_count == 0:
                # Insert the permalinks and get their inserted id
                perma = "Euromillions-hotpicks-result-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
                # print(perma)
                self.curr.execute(
                    """Select pm_id from hottpicks_permalinks_meta where draw_id = %s AND hotpicks_permalinks = %s""", (
                        date_id,
                        perma
                    ))
                perma_data = self.curr.fetchall()
                perma_count = self.curr.rowcount
                if perma_count < 1:
                    self.curr.execute(
                        """INSERT INTO hottpicks_permalinks_meta(draw_id, hotpicks_permalinks) VALUES (%s,%s)""", (
                            date_id,
                            perma
                        ))
                    pm_id = self.curr.lastrowid
                else:
                    pm_id = perma_data[0][0]

                # Insert the prize breakdown
                for i in range(len(item['match'])):
                    self.curr.execute(
                        "INSERT INTO hottpicks_prize(hottpicks_draw_id, hottpicks_draw_match, hottpicks_winner, hottpicks_prize, hottpicks_total, permalinks_hotpicks) VALUES (%s,%s,%s,%s,%s,%s)",
                        (
                            date_id,
                            item['match'][i],
                            item['winner'][i],
                            item['prize'][i],
                            item['total'][i],
                            pm_id
                        ))
                self.curr.execute(
                    "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                    (
                        datetime.date.today(),
                        7
                    ))
                self.conn.commit()
                print("Row Inserted")
            else:
                print("Prize Breakdown Exists in Table")

        else:
            print("Date Exist in table")


#######################################
#       Lotto Hotpicks Lottery         #
#######################################

class LottoHotpicks(object):
    def __init__(self):
        self.createconnection()

    def __del__(self):
        self.connectionClose()

    def createconnection(self):
        try:
            self.conn = mysql.connector.connect(host = 'giow16.siteground.us', user = 'aliarsha_result',
                                                passwd = 'Burewalla ', database = 'aliarsha_Lottery')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        self.curr = self.conn.cursor(buffered = True)

    def connectionClose(self):
        if (self.conn.is_connected()):
            self.curr.close()
            self.conn.close()

    def connectionClose(self):
        if (self.conn.is_connected()):
            # self.curr.close()
            self.conn.close()

    def process_item(self, item, spider):
        if (spider.name == 'LottoHotpicks'):
            # print(spider.name)
            self.lottoHotResult(item)
            return item

    def lottoHotResult(self, item):
        d = item['date']
        d = d.strftime("%Y-%m-%d")
        self.curr.execute("Select lottery_date_id from lottery_date where lottery_name_id =%s AND lottery_date =%s", (
            102,
            d
        ))
        row_data = self.curr.fetchall()
        row_count = self.curr.rowcount

        # Check if date is not exist in table
        if row_count == 1:
            date_id = row_data[0][0]
            # Check for the prize breakdown is already in table
            self.curr.execute("""Select hottpicks_prize_id from hottpicks_prize where hottpicks_draw_id = %s """, (
                date_id,
            ))
            prize_data = self.curr.fetchone()
            prize_count = self.curr.rowcount

            if prize_count == 0:
                # Insert the permalinks and get their inserted id
                perma = "Lotto-hotpicks-result-" + datetime.datetime.strftime(item['date'], "%d-%m-%Y")
                self.curr.execute(
                    """Select pm_id from hottpicks_permalinks_meta where draw_id = %s AND hotpicks_permalinks = %s""", (
                        date_id,
                        perma
                    ))
                perma_data = self.curr.fetchall()
                perma_count = self.curr.rowcount

                if perma_count < 1:
                    self.curr.execute(
                        """INSERT INTO hottpicks_permalinks_meta(draw_id, hotpicks_permalinks) VALUES (%s,%s)""", (
                            date_id,
                            perma
                        ))
                    pm_id = self.curr.lastrowid
                else:
                    pm_id = perma_data[0][0]

                # print("Date : ", str(date_id))
                # print("perma : ", str(pm_id))

                # Insert the prize breakdown
                for i in range(len(item['match'])):
                    self.curr.execute(
                        "INSERT INTO hottpicks_prize(hottpicks_draw_id, hottpicks_draw_match, hottpicks_winner, hottpicks_prize, hottpicks_total, permalinks_hotpicks) VALUES (%s,%s,%s,%s,%s,%s)",
                        (
                            date_id,
                            item['match'][i],
                            item['winner'][i],
                            item['prize'][i],
                            item['total'][i],
                            pm_id
                        ))
                self.curr.execute(
                    "UPDATE  table_sitemap SET last_update = %s WHERE page_id = %s",
                    (
                        datetime.date.today(),
                        8
                    ))

                self.conn.commit()
                print("Row Inserted")
            else:
                print("Prize Breakdown Exist")

        else:
            print("Date Exist in table")
