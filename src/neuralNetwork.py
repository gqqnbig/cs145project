import pandas as pd
from numpy import loadtxt
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers

import os
import datasetHelper
import Program
import generate_movieRatings
import dbHelper
# import math
# import bitstring

# ALL_GENRES = sorted(['Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'IMAX', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

# Construct input data
dataFolder = datasetHelper.getDataset()
movieYearGenresFileName = 'movies-year-genres.csv'
Program.ensureMovieYearGenresFile(dataFolder, 'movies-year-genres.csv')
generate_movieRatings.ensureMergedCsv(dataFolder)

# seperate the independent and target variable on training data
train_data = pd.read_csv(os.path.join(dataFolder, 'train_movies_ratings.csv'))
train_x = train_data.drop(columns=['rating'], axis=1).to_numpy()
train_y = train_data['rating'].to_numpy()

# seperate the independent and target variable on testing data
validation_data = pd.read_csv(os.path.join(dataFolder, 'val_movies_ratings.csv'))
validation_x = validation_data.drop(columns=['rating'], axis=1).to_numpy()
validation_y = validation_data['rating'].to_numpy()

# define the keras model
model = Sequential()

# This model has three layers: one for input layer, one hidden layer, and one output layer. Can be modified.
model.add(Dense(30, input_dim=23, activation='relu'))
model.add(Dense(23, activation='relu'))
# model.add(Dense(20, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile the keras model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# fit the keras model on the dataset
# Epoches: number of times the model goes through the entire data set
# batch size: number of samples the model trains before updating loss 
model.fit(train_x, train_y, epochs=5, batch_size=50)

# evaluate the keras model
_, accuracy = model.evaluate(validation_x, validation_y)
print('Accuracy: %.2f' % (accuracy*100))