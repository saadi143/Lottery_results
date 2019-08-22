# -*- coding: utf-8 -*-
import scrapy
from ..items import LotteryItem
import datetime

class EuromillionSpider(scrapy.Spider):
    name = 'Euromillion'
    allowed_domains = ['www.results.co.uk']
    start_urls = ['http://www.results.co.uk/euromillions-results']
    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'ITEM_PIPELINES': { 'Lottery.pipelines.LotteryPipeline': 300}
    }

    def parse(self, response):
        # html = response.body
        # soup = BeautifulSoup(html, 'lxml')
        # table = soup.table
        # row = soup.select("table > tr:nth-of-type(2)")
        # print(row)
        table = response.css('table')
        all_rows = table.css('tr')
        for row in all_rows[1:5]:
            if (not (row.css('.dateHeader') or row.css('.compHeader'))):
                date = row.css('td a ::text').extract()
                # print(row)
                date_link = row.css('td a::attr(href)').get()
                final_date = date[1].split()
                day = final_date[0]
                final_date[0] = day[:-2]
                final_date = " ".join(final_date)
                date = datetime.datetime.strptime(final_date, "%d %B %Y").date()
                #print("parse : ", self.date)
                # item['date_link'] = date_link
                request = response.follow(date_link, callback= self.lotteryDetail, cb_kwargs=dict(date = date))
                yield request

    def lotteryDetail(self, response, date):
        item = LotteryItem()
        #print(date)
        item['date'] = date
        match   = []
        star    = []
        winner  = []
        prize   = []
        total   = []
        all_table = response.css('table')
        #Lottery Draw
        # date = lottery_number_table.css('.dateHeader::text').extract()
        lottery_draw = all_table[0]
        all_rows = lottery_draw.css('tr')
        draw_number_row = all_rows[2]
        draw_number_text = lottery_draw.css('.compHeader th::text').extract()
        item['draw_number'] = draw_number_text[0].split()[-1]
        draw_number_list = draw_number_row.css('td span::text').extract()
        item['draw_1'] = draw_number_list[0]
        item['draw_2'] = draw_number_list[1]
        item['draw_3'] = draw_number_list[2]
        item['draw_4'] = draw_number_list[3]
        item['draw_5'] = draw_number_list[4]
        item['draw_6'] = draw_number_list[5]
        item['draw_7'] = draw_number_list[6]

       #Result Maker
        result_maker_table = all_table[1]
        maker_list = result_maker_table.css('tr td span::text').extract()
        #print(draw_number_list)
        #print(maker_list[0])
        try:

            item['maker_result'] = maker_list[0]
        except IndexError:
            return

        #PrizeBreakdown
        prize_table = all_table[2]
        all_rows = prize_table.css('tr')
        for row in all_rows:
            if (not (row.css('.dateHeader') or row.css('.compHeader'))):
                columns = row.css('td')
                for i, cell in enumerate(columns):
                    if(i == 0):
                        try:
                            td_1 = cell.css('strong::text')[0].extract()
                        except IndexError:
                            return
                        match.append(td_1.split()[1])
                        try:
                            star.append( td_1.split()[3])
                        except IndexError:
                            star.append(0)
                    if(i==1):
                        winner.append(cell.css('td::text')[0].extract().strip())
                    if(i==2):
                        prize_row =  cell.css('td::text')[0].extract()
                        prize.append(prize_row[1:].strip())
                    if(i==3):
                        total_text = cell.css('td::text')[0].extract()
                        total.append(total_text[1:].strip())

        item['match'] = match
        item['star'] = star
        item['winner'] = winner
        item['prize'] = prize
        item['total'] = total
        #print(item['maker_result'])
        yield item

