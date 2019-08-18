# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3 as lite
import six

con = None  # this is the db connection object.


# it gets created on init and deleted on __del__
# just be careful of circular dependency, because del might not get called in that case.

class TutorialPipeline(object):

    def __init__(self):
        self.setup_db_con()
        self.create_tables()

    def process_item(self, item, spider):
        for key, value in six.iteritems(item):
            if key == "CastMembers":
                continue

            if isinstance(value, list):
                if value:
                    temp_list = []
                    for obj in value:
                        temp = self.strip_html(obj)
                        temp_list.append(temp)
                    item[key] = temp_list
                else:
                    item[key] = ""
            elif key is not 'MainPageUrl':
                item[key] = self.strip_html(value)
            else:
                item[key] = value

        self.store_in_db(item)

        return item

    def store_in_db(self, item):
        self.store_film_info_in_db(item)
        film_id = self.cur.lastrowid

        for cast in item['CastMembers']:
            self.store_actor_info_in_db(cast, film_id)

    def store_film_info_in_db(self, item):
        self.cur.execute("INSERT INTO Films(\
			title, \
			rating, \
			ranking, \
			release_date, \
			page_url, \
			director, \
			writers, \
			runtime, \
			sinopsis, \
			genres, \
			mpaa_rating, \
			budget, \
			language, \
			country, \
			gross_profit, \
			opening_weekend_profit, \
			aspect_ratio, \
			sound_mix, \
			color\
			) \
		VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", \
                         ( \
                             item.get('Title', ''),
                             float(item.get('Rating', 0.0)),
                             int(item.get('Ranking', 0)),
                             item.get('ReleaseDate', ''),
                             item.get('MainPageUrl', ''),
                             ', '.join(item.get('Director', '')),
                             ', '.join(item.get('Writers', '')),
                             item.get('Runtime', ''),
                             item.get('Sinopsis', '').strip(),
                             ', '.join(item.get('Genres', '')),
                             item.get('MpaaRating', ''),
                             self.clean_money(item.get('Budget', '')),
                             item.get('Language', ''),
                             item.get('Country', ''),
                             self.clean_money(item.get('GrossProfit', '')),
                             self.clean_money(item.get('OpeningWeekendProfit', '')),
                             item.get('AspectRatio', '').strip(),
                             ', '.join(item.get('SoundMix', '')),
                             item.get('Color', '')
                         ))
        self.con.commit()

    def store_actor_info_in_db(self, item, filmID):
        self.cur.execute("INSERT INTO Actors(\
			film_id, \
			actor_name, \
			character_name, \
			ranking \
			) \
		VALUES(?,?,?,?)",
                         (
                             filmID,
                             self.strip_html(item.get('ActorName', '')).strip(),
                             self.strip_html(item.get('CharacterName', '')).strip(),
                             item.get('Ranking', 0)
                         ))
        self.con.commit()

    def setup_db_con(self):
        self.con = lite.connect('test.db')
        self.cur = self.con.cursor()

    def strip_html(self, string):
        tag_stripper = MLStripper()
        tag_stripper.feed(string)
        return tag_stripper.get_data()

    def clean_money(self, string):
        # you could add more symbols to this, but it gets kinda complex with some of the symbles being unicode,
        # so I sipped that for now.
        currency_symbols = "$"
        clean_money_string = ""
        stop_adding = False
        for index, char in enumerate(list(string)):
            if char in currency_symbols and not stop_adding:
                clean_money_string += char
            elif char == "," and not stop_adding:
                clean_money_string += char
            elif char.isdigit() and not stop_adding:
                clean_money_string += char
            elif char in ' ':
                # we know that numbers do not have spaces in them, so we can assume that once the number
                # has started there will be no spaces
                if len(clean_money_string) > 0:
                    stop_adding = True

        return clean_money_string

    # this is the class destructor. It will get called automatically by python's garbage collector once this class is
    # no longer used.
    def __del__(self):
        self.close_db()

    # I'm currently doping the tables if they exist before I run the script each time, so that
    # I don't get duplicate info.
    def create_tables(self):
        self.drop_films_table()
        self.drop_actors_table()

        self.create_actors_table()
        self.create_films_table()

    def create_films_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Films(id INTEGER PRIMARY KEY NOT NULL, \
			title TEXT, \
			rating REAL, \
			ranking INT, \
			release_date TEXT, \
			page_url TEXT, \
			director TEXT, \
			writers TEXT, \
			runtime TEXT, \
			sinopsis TEXT, \
			genres TEXT, \
			mpaa_rating TEXT, \
			budget TEXT, \
			language TEXT, \
			country TEXT, \
			gross_profit TEXT, \
			opening_weekend_profit TEXT, \
			aspect_ratio TEXT, \
			sound_mix TEXT, \
			color TEXT \
			)")

    def create_actors_table(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Actors(id INTEGER PRIMARY KEY NOT NULL, \
			film_id INTEGER NOT NULL, \
			actor_name TEXT, \
			character_name TEXT, \
			ranking INTEGER )")

    def drop_films_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Films")

    def drop_actors_table(self):
        self.cur.execute("DROP TABLE IF EXISTS Actors")

    def close_db(self):
        self.con.close()


from html.parser import HTMLParser


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
