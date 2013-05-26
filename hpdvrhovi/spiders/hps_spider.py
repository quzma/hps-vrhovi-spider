# coding: utf-8

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

from hpdvrhovi.items import VrhItem

import re

class HpsSpider(BaseSpider):
	def __init__(self):
		self.failures = open('fail.log', 'w+')

	name = "hps"
	allowed_domains = ["hps.hr"]
	start_urls = [line.strip() for line in open('vrhovi.url')]

	def conversion(self, old):
		direction = {'N':1, 'S':-1, 'E': 1, 'W':-1}
		new = old.replace(u'°',' ').replace('\'',' ').replace('"',' ')
		new_dir = new[0]
		new = new[1:].split()
		new.extend([0,0,0])
		return (float(new[0])+float(new[1])/60.0+float(new[2])/3600.0) * direction[new_dir]

	def parse(self, response):
		hxs = HtmlXPathSelector(response)
		try:
			vrh = VrhItem() 
			vrh['name'] = hxs.select('//h1/text()').extract()[0] 
			
			kt_height = hxs.select('//h3/text()')[0].extract().split(',')	
			vrh['kt'] = kt_height[0]
			vrh['height_m'] = int(re.search("[0-9]+", kt_height[1]).group(0))
		
			coords = hxs.select('//tr[2]/td[2]/text()').extract()[0].replace(' ','')
			coords = re.split("E", coords)
			vrh['lat'] = self.conversion(coords[0])
			vrh['lon'] = self.conversion("E" + coords[1])
			
			vrh['view'] = hxs.select('//tr[1]/td[2]/text()').extract()[0]
			vrh['stamp'] = hxs.select('//tr[3]/td[2]/text()').extract()[0]
			vrh['approach'] = hxs.select('//tr[4]/td[2]/text()').extract()[0]
			try:
				vrh['maps'] = hxs.select('//tr[5]/td[2]/text()').extract()[0]
			except:
				pass
			vrh['img'] = 'http://www.hps.hr' + hxs.select('//*[@id="podatakContainer"]/div/a/img/@src').extract()[0]
		except:
			"NOT PASSED! " +  hxs.select('//h1/text()').extract()[0] 
			self.failures.write(hxs.select('//h1/text()').extract()[0])
			pass
		
		return vrh
