# -*- coding: utf-8 -*-
import scrapy
from ..items import GushiwenItem
import re


class TangshiSpider(scrapy.Spider):
    name = 'tangshi'
    allowed_domains = ['so.gushiwen.org']
    start_urls = ['https://so.gushiwen.org/authors/Default.aspx?p=1&c=%e5%94%90%e4%bb%a3']

    def parse(self, response):
        divs = response.xpath('//div[@class="left"]/div')

        for div in divs:
            a = div.xpath('./div[1]/p[2]/a')
            if not a:
                pass
            else:
                author = div.xpath('./div[1]/p[1]//b/text()').get()
                link = a.xpath('./@href').get()  # link=/authors/authorvsw_b90660e3e492A1.aspx
                link = response.urljoin(link)  # https://so.gushiwen.org/authors/authorvsw_b90660e3e492A1.aspx

                request = scrapy.Request(
                    url=link,
                    callback=self.parse_detail,
                    meta={'info': (author)}

                )
                yield request

        # 翻页
        next_url=response.xpath('//a[@class="amore"]/@href').get()
        next_url=response.urljoin(next_url)
        yield scrapy.Request(
            url=next_url,
            callback=self.parse
        )

    def parse_detail(self, response):
        author = response.meta.get('info')

        divs = response.xpath('//div[@class="sons"]')
        for div in divs:
            title = div.xpath('./div[1]/p/a/b/text()').get()
            content = div.xpath('.//div[@class="contson"]//text()').getall()
            content = list(map(lambda x: re.sub(r"[\s]", "", x), content))
            content = "".join(content)
            item = GushiwenItem(author=author, title=title, content=content)
            yield  item

        # 翻页
        a_link = response.xpath('//*[@id="FromPage"]/div/a[1]/@href').get()
        a_link = response.urljoin(a_link)
        if a_link:
            request=scrapy.Request(
                url=a_link,
                callback=self.parse_detail,
                meta={"info": (author)}
            )
            yield request

            print(a_link)
        else:
            pass
