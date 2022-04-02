import scrapy


class fcSpider(scrapy.Spider):
    name = 'boomCrawler-v1'

    start_urls = ['https://www.boomlive.in/fact-check/1']
    article_urls = []

    def start_requests(self):
        urls = [
            'https://www.boomlive.in/fact-check/',
            'https://www.boomlive.in/world/',
            'https://www.boomlive.in/law/',
            'https://www.boomlive.in/news',
            'https://www.boomlive.in/explainers'

        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        allHorizontalDivs = response.css("div.horizontal-card")
        article_urls = []
        base_url = "https://www.boomlive.in"

        for div in allHorizontalDivs:
            url = div.css("a").attrib["href"]
            article_urls.append(url)

        for url in article_urls:
            url_modified = base_url + url
            yield scrapy.Request(url_modified, callback=self.parseArticle)

    def parseArticle(self, response):
        source_url = response.url
        article_heading = response.css("header h1.is-custom-title::text").get()
        short_context = response.css("div h2::text").get()
        short_intro = response.css("div p::text").get()
        author = response.css("div a.icon-link::text").get()
        date = response.css("span span.convert-to-localtime::text").get()
        image_set1 = response.css(
            "div.single-featured-thumb-container img::attr(src)").getall()
        image_set2 = response.css(
            "div.image-and-caption-wrapper img::attr(src)").getall()

        article_metadata_dic = {
            "source_url": source_url,
            "article_heading": article_heading,
            "short_context": short_context,
            "short_into": short_intro,
            "author": author,
            "date": date,
            "image_set1": image_set1,
            "image_set2": image_set2
        }

        yield article_metadata_dic
