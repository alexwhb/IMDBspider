import scrapy

from tutorial.items import MovieItem, CastItem


class tutorialSpider(scrapy.Spider):
	name = "tutorial"
	allowed_domains = ["imdb.com"]
	start_urls = [
		"http://www.imdb.com/chart/top?ref_=nv_ch_250_4" # this is the top 250 list
	] 

	# for now this method just parses the top 250 IMDB page and has a callbck request to each title link 
	# so I can parse more film info per film. 
	def parse(self, response):
		for sel in response.xpath("//*[@class='chart']/tbody/tr/td[2]"):
			item = MovieItem()
			item['Title'] = sel.xpath('a/text()').extract()[0]
			item['Rating'] = sel.xpath('span[1]/@data-value').extract()[0]
			item['Ranking'] = sel.xpath('span[1]/text()').re('\d+')[0]
			item['ReleaseDate'] = sel.xpath('span[2]/@data-value').extract()[0]
			item['MianPageUrl'] = "http://imdb.com"+sel.xpath('a/@href').extract()[0]

			request = scrapy.Request(item['MianPageUrl'], callback=self.parseMovieDetails)
			request.meta['item'] = item
			yield request


	def parseMovieDetails(self, response):
		item = response.meta['item']
		item = self.getBasicFilmInfo(item, response)	
		item = self.getTechnicalDetials(item, response)
		item = self.getCastMemberInfo(item, response)		
		return item


	def getBasicFilmInfo(self, item, response):
		item['Director'] = response.xpath("//div[@itemprop='director']/a/span/text()").extract()
		item['Writers'] = response.xpath("//div[@itemprop='creator']/a/span/text()").extract() #this can deffinatly be multiple people. 
		item['Sinopsis'] = response.xpath("//div[@itemprop='description']").extract()[0] # this one is going to need to be cleaned up
		item['Genres'] = response.xpath("//div[@itemprop='genre']/a/text()").extract()
		item['MpaaRating'] = response.xpath("//span[@itemprop='contentRating']/text()").extract()[0]
		return item


	def getCastMemberInfo(self, item, response):
		item['CastMembers'] = []
		for index, castMember in enumerate(response.xpath("//*[@id='titleCast']/table/tr")):
			# the first index does not have any actor data in it, so we skip it. 
			if(index == 0):
				continue

			cast = CastItem()
			cast['Ranking'] = index 
			cast['ActorName'] = self.ifNotEmptyGetIndex(castMember.xpath("td[2]").extract())
			cast['CharacterName'] = self.ifNotEmptyGetIndex(castMember.xpath("td[4]/div").extract())
			item['CastMembers'].append(cast)

		return item

	def getTechnicalDetials(self, item, response):
		# some of these items do not get values so I need to set a defualt for them. I don't want errors. 
		for index, details in enumerate(response.xpath("//*[@id='titleDetails']/div")):
			titleDetails = details.xpath('h4/text()').extract()
			if(titleDetails):		
				item = self.mapFilmDetails(response, self.ifNotEmptyGetIndex(titleDetails), item, index)

		return item


	# this method looks at each item form the film detials wraper, and figures out what text goes with wich item,
	# sense there are no clear ways of doing it otherwise. 
	def mapFilmDetails(self, response, titleDetails, item, index):
		index += 1 # the xpaths are not zero indexed
		if(titleDetails):
			if("Language" in titleDetails):
				item['Language'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]/a/text()").extract())
			elif("Country" in titleDetails):
				item['Country'] =  self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]/a/text()").extract())
			elif("Budget" in titleDetails):
				item['Budget'] =  self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]").extract())
			elif("Gross" in titleDetails):
				item['GrossProffit'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]").extract())
			elif("Opening Weekend" in titleDetails):
				item['OpeningWeekendProffit'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]").extract()) #it also might be just \d
			elif("Sound Mix" in titleDetails):
				item['SoundMix'] = response.xpath("//*[@id='titleDetails']/div["+str(index)+"]/a/text()").extract()
			elif("Color" in titleDetails):
				item['Color'] =  self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]/a/text()").extract())
			elif("Aspect Ratio" in titleDetails):
				item['AspectRatio'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]/text()").extract(), 1)
			elif("Runtime:" in titleDetails):
				item['Runtime'] = self.ifNotEmptyGetIndex(response.xpath("//*[@id='titleDetails']/div["+str(index)+"]/time/text()").extract())
		return item


	def ifNotEmptyGetIndex(self, item, index = 0):
		if item: #check to see it's not empty
			return item[index]
		else:
			return item
