# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class VrhItem(Item):
    # define the fields for your item here like:
    # name = Field()
	name = Field()
	height_m = Field()
	lat = Field()
	lon = Field()
	kt = Field()
	view = Field()
	stamp = Field()
	approach = Field()
	maps = Field()
	img = Field()
	pass
