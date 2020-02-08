from scrapy import Spider
from scrapy.http import Request
import requests 
from uuid import uuid4

class WallsSpider(Spider):
    name = 'walls'
    allowed_domains = ['pexels.com']

    def __init__(self, q):
        self.start_urls = ['http://pexels.com/search/' + q]

    def parse(self, response):
        urls = response.xpath('//a[@class="js-photo-link photo-item__link"]/@href').extract()
        absolute_url = [response.urljoin(i) for i in urls]
        tags = [i.split('-')[-1][:-1] for i in absolute_url]  # main
        for i in tags:
            image_url = 'https://www.pexels.com/photo/'+ str(i) +'/download/'
            r = requests.get(image_url)
            file_name = str(uuid4()) + '.jpg'
            with open(file_name,'wb') as f: 
                f.write(r.content)

        try:
            next_page_url = response.xpath('//a[@rel="next"]/@href')[0].extract()
            abs_next_page_url = response.urljoin(next_page_url) # main
            return Request(abs_next_page_url)
        except IndexError:
            pass
        