# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class GeojsonPipeline(object):
	def __init__(self):
		self.file = open('geoitems.json', 'w+')

	def geofeature_from_item(self, item):
		geometry = {'type'			:'Point',
					'coordinates'	:[item['lon'], item['lat']]}

		del item['lat']
		del item['lon']
		json_friendly_item = {}
		for i in item:
			json_friendly_item[i] = item[i]

		return {'type'			:'Feature',
				'geometry'		:geometry,
				'properties'	:json_friendly_item}
   
	def open_spider(self,spider):
		self.file.write('{"type": "FeatureCollection", "features": [')

	def close_spider(self,spider):
		self.file.write(']}')

	def process_item(self, item, spider):
		line = json.dumps(self.geofeature_from_item(item)) + ",\n"
		self.file.write(line)
		return item
