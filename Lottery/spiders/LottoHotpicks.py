# -*- coding: utf-8 -*-
import scrapy
from ..items import hotpicks
import datetime


class LottohotpicksSpider(scrapy.Spider):
    name = 'LottoHotpicks'
    allowed_domains = ['www.results.co.uk']
    start_urls = ['http://www.results.co.uk/lotto-hotpicks-results']
    custom_settings = {
        # 'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'ITEM_PIPELINES': { 'Lottery.pipelines.LottoHotpicks': 300 }
    }

    def parse(self, response):
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
                date = final_date
                request = response.follow(date_link, callback=self.lotteryDetail, cb_kwargs=dict(date=date))
                yield request

    def lotteryDetail(self, response, date):
        item = hotpicks()
        item['date'] = datetime.datetime.strptime(date, "%d %B %Y").date()
        match = []
        winner  = []
        prize   = []
        total   = []
        all_table = response.css('table')

        # PrizeBreakdown
        prize_table = all_table[1]
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
                    if(i==1):
                        winner.append(cell.css('td::text')[0].extract().strip())
                    if(i==2):
                        prize_row =  cell.css('td::text')[0].extract()
                        prize_value = prize_row[1:].strip()
                        try:
                            dem = int(prize_value.replace(',',''))
                            prize.append(prize_value)
                        except ValueError:
                            prize.append(0)

                    if(i==3):
                        total_text = cell.css('td::text')[0].extract()
                        total_value = total_text[1:].strip()
                        try:
                            num = int(total_value.replace(',', ''))
                            total.append(total_value)
                        except ValueError:
                            total.append(0)

        item['match'] = match
        item['winner'] = winner
        item['prize'] = prize
        item['total'] = total
        yield item
