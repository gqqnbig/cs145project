#!/usr/bin/env python3

import os
import csv
import re
import sys
from types import SimpleNamespace
import bisect
from sklearn import tree
import numpy as np
import sqlite3


def ensureMovieYearGenresFile(fileName):
	if os.path.isfile(os.path.join(DATA_FOLDER, movieYearGenresFileName)):
		return

	movies = {}
	global ALL_GENRES
	with open(DATA_FOLDER + "/movies.csv", encoding='utf-8') as moviesFile:  # will automatically close the file when exit the with block
		reader = csv.reader(moviesFile)
		next(reader)  # skip the column headers
		for row in reader:
			id = row[0]
			title = row[1].strip()

			m = re.search('\((\d+)\)$', title)
			if m is None:
				print("Movie title doesn't have year. Id=" + id + ", title=" + title, file=sys.stderr)
				continue

			if row[2] == '(no genres listed)':
				continue

			year = int(m.group(1))
			genres = row[2].split('|')

			if (any([bisect.bisect_left(ALL_GENRES, g) < 0 for g in genres])):
				raise Exception('One of {0} is not listed in allGenres.'.format(genres))

			# print('year is %d' % year)
			# print(genres)

			item = SimpleNamespace()
			item.year = year
			item.genres = genres
			movies[id] = item

	# print(', '.join(allGenres))

	with open(DATA_FOLDER + "/" + fileName, encoding='utf-8', mode='w', newline='') as f:
		writer = csv.writer(f)
		writer.writerow(['id', 'year'] + ALL_GENRES)
		for id in movies:
			item = movies[id]
			map = [0] * len(ALL_GENRES)
			for i in range(len(item.genres)):
				index = bisect.bisect_left(ALL_GENRES, item.genres[i])
				map[index] = 1

			writer.writerow([id, item.year] + map)


def doesTableExist(TABLE_NAME, cur):
	cur.execute("SELECT 1 FROM sqlite_master WHERE name =? and type='table'", (TABLE_NAME,))
	return cur.fetchone() is not None


def ensureMovieYearGenresTable(movieYearGenresFileName, dbConnection):
	cur = dbConnection.cursor()
	TABLE_NAME = 'MovieYearGenres'
	if doesTableExist(TABLE_NAME, cur):
		return

	# Syntax 'create table if not exists' exists, but we don't know if we need to insert rows.
	with open(os.path.join(DATA_FOLDER, movieYearGenresFileName), encoding='utf-8') as movieYearGenresFile:
		csvReader = csv.reader(movieYearGenresFile)
		headers = next(csvReader)

		headers[0] = headers[0] + ' INTEGER NOT NULL PRIMARY KEY'
		headers = headers[0:1] + ['[' + h + '] INTEGER' for h in headers[1:]]
		cur.execute("CREATE TABLE {1} ({0})".format(', '.join(headers), TABLE_NAME))
		# table names can't be the target of parameter substitution
		# https://stackoverflow.com/a/3247553/746461

		to_db = [row for row in csvReader]

		cur.executemany("INSERT INTO {1} VALUES ({0});".format(','.join('?' * len(headers)), TABLE_NAME), to_db)
		dbConnection.commit()

	cur.execute('select * from {0} where id=131162'.format(TABLE_NAME))
	print(cur.fetchone())


def ensureRatingsTable(fileName, dbConnection):
	cur = dbConnection.cursor()
	TABLE_NAME = 'Ratings'
	if doesTableExist(TABLE_NAME, cur):
		return

	cur.execute("CREATE TABLE {0} (userId INTEGER NOT NULL,movieId INTEGER NOT NULL,rating INTEGER NOT NULL, PRIMARY KEY(userId,movieId))".format(TABLE_NAME))
	with open(os.path.join(DATA_FOLDER, fileName), encoding='utf-8') as f:
		csvReader = csv.reader(f)
		next(csvReader)

		to_db = [row for row in csvReader]

		cur.executemany("INSERT INTO {0} VALUES (?,?,?);".format(TABLE_NAME), to_db)
		dbConnection.commit()

	cur.execute('select * from {0} where userId=1 and movieId=151'.format(TABLE_NAME))
	print(cur.fetchone())


DATA_FOLDER = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + "/../data")
ALL_GENRES = sorted(['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

if __name__ == "__main__":
	movieYearGenresFileName = 'movies-year-genres.csv'
	ensureMovieYearGenresFile(movieYearGenresFileName)

	con = sqlite3.connect(os.path.join(DATA_FOLDER, "sqlite.db"))  # we may use ":memory:", but it may be too large, about 1.5GB
	ensureMovieYearGenresTable(movieYearGenresFileName, con)
	ensureRatingsTable('train_ratings_binary.csv', con)

	cur = con.cursor()

	cur.execute('''
SELECT Ratings.rating, Ratings.userId, MovieYearGenres.year, {0} FROM Ratings
join MovieYearGenres on Ratings.movieId=MovieYearGenres.id'''.format(','.join(['[' + g + ']' for g in ALL_GENRES])))
	print(cur.fetchone())

	con.close()

# clf = tree.DecisionTreeClassifier()