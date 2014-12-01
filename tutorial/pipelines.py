# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3 as lite

con = None # this is the db connection object. 
# it gets created on init and deleted on __del__ just be carful of circular dependincys, because del might not get called in that case. 

class TutorialPipeline(object):

	def __init__(self):
		self.setupDBCon()
		self.createTables()
		

	def process_item(self, item, spider):
		for key, value in item.iteritems():
			if key == "CastMembers":
				continue

			if(isinstance(value, list)):
				if value:
					templist = []
					for obj in value:
						temp = self.stripHTML(obj)
						templist.append(temp)
					item[key] = templist
				else:
					item[key] = ""
			else:
				item[key] = self.stripHTML(value)

		self.storeInDb(item)

		return item

	def storeInDb(self, item):
		self.storeFilmInfoInDb(item)
		filmID = self.cur.lastrowid
		
		for cast in item['CastMembers']:
			self.storeActorInfoInDb(cast, filmID)


	def storeFilmInfoInDb(self, item):
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
			gross_proffit, \
			opening_weekend_proffit, \
			aspect_ratio, \
			sound_mix, \
			color\
			) \
		VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", \
		( \
			item.get('Title', ''), 
			float(item.get('Rating', 0.0)), 
			int(item.get('Ranking', 0)), 
			item.get('ReleaseDate',''), 
			item.get('MianPageUrl', ''),
			', '.join(item.get('Director', '')),
			', '.join(item.get('Writers', '')),
			item.get('Runtime', ''),
			item.get('Sinopsis', '').strip(),
			', '.join(item.get('Genres', '')),
			item.get('MpaaRating', ''),
			self.cleanMoney(item.get('Budget','')),
			item.get('Language', ''),
			item.get('Country', ''),
			self.cleanMoney(item.get('GrossProffit', '')),
			self.cleanMoney(item.get('OpeningWeekendProffit', '')),
			item.get('AspectRatio', '').strip(),
			', '.join(item.get('SoundMix', '')),
			item.get('Color', '')
		))
		self.con.commit()  

	def storeActorInfoInDb(self, item, filmID):
		self.cur.execute("INSERT INTO Actors(\
			film_id, \
			actor_name, \
			charecter_name, \
			ranking \
			) \
		VALUES(?,?,?,?)", 
		(
			filmID,
			self.stripHTML(item.get('ActorName','')).strip(),
			self.stripHTML(item.get('CharacterName','')).strip(),
			item.get('Ranking', 0)
		))
		self.con.commit()  

	def setupDBCon(self):
		self.con = lite.connect('test.db')
		self.cur = self.con.cursor()
  			

	def stripHTML(self, string):
		tagStripper = MLStripper()
		tagStripper.feed(string)
		return tagStripper.get_data()


	def cleanMoney(self, string):
		# you could add more simpbles to this, but it gets kinda complex with some of the symbles being unicode, so I skpped that for now. 
		currencySymbles = "$" 
		cleanMoneyString = ""
		stopAdding = False
		for index, char in enumerate(list(string)):
			if char in currencySymbles and not stopAdding:
				cleanMoneyString += char
			elif char == "," and not stopAdding:
				cleanMoneyString += char
			elif char.isdigit() and not stopAdding:
				cleanMoneyString += char
			elif char in ' ':
				# we know that numbers do not have spaces in them, so we can assume that once the number
				# has started there will be no spaces
				if len(cleanMoneyString) > 0:
					stopAdding = True


		return cleanMoneyString

	# this is the class destructor. It will get called automaticly by python's garbage collecter once this class is no longer used. 
	def __del__(self):
		self.closeDB()

	# I'm currently droping the tables if they exist before I run the script each time, so that
	# I don't get duplicate info. 
	def createTables(self):
		self.dropFilmsTable()
		self.dropActorsTable()

		self.createActorsTable()
		self.createFilmsTable()


	def createFilmsTable(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS Films(id INTEGER PRIMARY KEY NOT NULL, \
			title TEXT, \
			rating REAL, \
			ranking INT, \
			release_date TEXT, \
			page_url TEXT, \
			director TEXT, \
			writers Text, \
			runtime TEXT, \
			sinopsis TEXT, \
			genres TEXT, \
			mpaa_rating TEXT, \
			budget TEXT, \
			language TEXT, \
			country TEXT, \
			gross_proffit TEXT, \
			opening_weekend_proffit TEXT, \
			aspect_ratio TEXT, \
			sound_mix TEXT, \
			color TEXT \
			)")

	def createActorsTable(self):
		self.cur.execute("CREATE TABLE IF NOT EXISTS Actors(id INTEGER PRIMARY KEY NOT NULL, \
			film_id INTEGER NOT NULL, \
			actor_name TEXT, \
			charecter_name TEXT, \
			ranking INTEGER )")

	def dropFilmsTable(self):
		self.cur.execute("DROP TABLE IF EXISTS Films")

	def dropActorsTable(self):
		self.cur.execute("DROP TABLE IF EXISTS Actors")

	def closeDB(self):
		self.con.close()



from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)
