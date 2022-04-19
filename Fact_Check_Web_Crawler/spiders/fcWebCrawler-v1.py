
import json
import scrapy
from Fact_Check_Web_Crawler.items import Metadata, Image_context, FactCheckWebCrawlerItem
from scrapy.loader import ItemLoader


class fcSpider(scrapy.Spider):
    name = 'boomCrawler-v1'

    start_urls = ['https://www.boomlive.in/fact-check/1']
    metadata_list = []

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

        metadata = ItemLoader(item=Metadata(), response=response)

        metadata.add_value("news_src", "boomlive.in")
        # images from first selector
        metadata.add_value("images_url",
                           response.css("div.single-featured-thumb-container img::attr(src)").getall())
        # images from second selector
        metadata.add_value("images_url",
                           response.css("div.image-and-caption-wrapper img::attr(src)").getall())
        # images from social media embeddings selectors
      # l.add_css("images_url", "youtube-thumbnail, twitter-embeds, instagram-embeds")
        metadata.add_value("src_article_url", response.url)
        metadata.add_value("article_heading", response.css(
            "header h1.is-custom-title::text").get())
        metadata.add_value("short_context", response.css("div h2::text").get())
        metadata.add_value("short_intro", response.css("div p::text").get())
        metadata.add_value("author", response.css(
            "div a.icon-link::text").get())
        metadata.add_value("date", response.css(
            "span span.convert-to-localtime::text").get())

   #     i = ItemLoader(item=Image_context)

        # for image_url in l["images_url"]:
        #     l["images_url"].remove(image_url)
        #     i.add_value("id", image_url)
        #     i.add_value("image_url", image_url)
        #     i.add_value("metadata", l)

        # fci = ItemLoader(item=FactCheckWebCrawlerItem)
        # i = ItemAdapter(i)
        # i = i.asdict()
        # fci.add_value("image_context", i)

        # source_url = response.url
        # article_heading = response.css("header h1.is-custom-title::text").get()
        # short_context = response.css("div h2::text").get()
        # short_intro = response.css("div p::text").get()
        # author = response.css("div a.icon-link::text").get()
        # date = response.css("span span.convert-to-localtime::text").get()
        # image_set1 = response.css(
        #     "div.single-featured-thumb-container img::attr(src)").getall()
        # image_set2 = response.css(
        #     "div.image-and-caption-wrapper img::attr(src)").getall()

        # article_metadata_dic = {
        #     "source_url": source_url,
        #     "article_heading": article_heading,
        #     "short_context": short_context,
        #     "short_into": short_intro,
        #     "author": author,
        #     "date": date,
        #     "image_set1": image_set1,
        #     "image_set2": image_set2
        # }
        print(metadata.load_item())
