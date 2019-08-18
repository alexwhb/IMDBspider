import scrapy
from scrapy.loader import ItemLoader
from ..items import MovieItem


class IMDBspider(scrapy.Spider):
    name = "IMDBspider"
    allowed_domains = ["imdb.com"]

    def start_requests(self):
        # movie_titles = ['The Incredibles']
        with open('/Users/alexwhb/Desktop/IMDBspider/IMDBspider/spiders/movies_to_search_for.txt') as f:
            movie_titles = list(f)

        for title in movie_titles:
            search_url = f'https://imdb.com/find?q={title.strip()}'

            yield scrapy.Request(url=search_url, callback=self.parse_search_results)

    # for now this method just parses the top 250 IMDB page and has a callbck request to each title link
    # so I can parse more film info per film.
    def parse_search_results(self, response):
        l = ItemLoader(item=MovieItem(), response=response)
        l.add_xpath('title', '//*[@id="main"]/div/div[2]/table/tr[1]/td[2]/a/text()')
        l.add_xpath('release_date', '//*[@id="main"]/div/div[2]/table/tr[1]/td[2]/text()')

        href = response.xpath('//*[@id="main"]/div/div[2]/table/tr[1]/td[2]/a/@href').extract()[0]
        url_to_film_long_description = f'http://imdb.com{href}'

        yield scrapy.Request(url=url_to_film_long_description, callback=self.parse_film_description,
                             meta={'movie_item': l.load_item()})

    def parse_film_description(self, response):
        l = ItemLoader(item=response.meta['movie_item'], response=response)

        l.add_xpath('director', '//*[@id="title-overview-widget"]/div[2]/div[1]/div[2]/a/text()')
        l.add_xpath('writers', '//*[@id="title-overview-widget"]/div[2]/div[1]/div[3]/a/text()')
        l.add_xpath('main_cast_members', '//*[@id="title-overview-widget"]/div[2]/div[1]/div[4]/a/text()')
        l.add_xpath('meta_score', '//*[@id="title-overview-widget"]/div[2]/div[3]/div[1]/a/div/span/text()')
        l.add_xpath('mpaa_rating', '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/text()')
        l.add_xpath('runtime', '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[2]/div[2]/div/time/text()')
        l.add_xpath('imdb_rating',
                    '//*[@id="title-overview-widget"]/div[1]/div[2]/div/div[1]/div[1]/div[1]/strong/span/text()')
        l.add_xpath('genres', '//*[@id="titleStoryLine"]/div[4]/a/text()')
        l.add_xpath('budget', '//*[@id="titleDetails"]/div[7]/text()')
        l.add_xpath('world_wide_box_office', '//*[@id="titleDetails"]/div[10]/text()')
        l.add_xpath('language', '//*[@id="titleDetails"]/div[3]/a[1]/text()')
        l.add_xpath('countries', '//*[@id="titleDetails"]/div[2]/a/text()')
        yield l.load_item()
