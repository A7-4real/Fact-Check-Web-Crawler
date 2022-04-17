# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from itemadapter import ItemAdapter

# metadata class


class Metadata(Item):

    # image context metadata
    news_src = Field(serializer=str)
    src_article_url = Field(serializer=str)
    # image url collected from different css selectors stored in python dict
    images_url = Field(serializer=dict)
    article_heading = Field(serializer=str)
    short_context = Field(serializer=str)
    short_intro = Field(serializer=str)
    author = Field(serializer=str)
    date = Field(serializer=str)


class Image_context(Item):

    # image context as a whole
    id = Field(serializer=str)
    image_url = Field(serializer=str)
    metadata = Field(serializer=Metadata)         # Metadata item


class FactCheckWebCrawlerItem(Item):

    # apended Images_context items
    image_context = Field(serializer=Image_context)
    pass


# adapterMetadata = ItemAdapter(Metadata)
# adapterImageContext = ItemAdapter(Image_context)
# adapterFcw = ItemAdapter(FactCheckWebCrawlerItem)
