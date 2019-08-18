# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
import re
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def clean_input(value):
    value = value.strip()
    if value != '':
        return value


def clean_release_date(value):
    return re.sub('\(|\)', '', value)


def clean_cast_members(value):
    if value != 'See full cast & crew':
        return value


class MovieItem(Item):
    title = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    imdb_rating = Field(output_processor=TakeFirst())
    release_date = Field(input_processor=MapCompose(clean_input, clean_release_date), output_processor=TakeFirst())
    director = Field(output_processor=TakeFirst())
    writers = Field(output_processor=Join(', '))
    world_wide_box_office = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    budget = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    language = Field(output_processor=TakeFirst())
    runtime = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    mpaa_rating = Field(input_processor=MapCompose(clean_input), output_processor=TakeFirst())
    main_cast_members = Field(input_processor=MapCompose(clean_cast_members), output_processor=Join(', '))
    meta_score = Field(output_processor=TakeFirst())
    countries = Field(input_processor=MapCompose(clean_input), output_processor=Join(', '))
    genres = Field(input_processor=MapCompose(clean_input), output_processor=Join(', '))
