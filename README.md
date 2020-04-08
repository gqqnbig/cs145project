# Movie Preference Prediction
The dataset is adapted from the [MovieLens](https://grouplens.org/datasets/movielens/20m/) dataset with modifications, e.g. the user IDs are hashed and shuffled.

This is the dataset for CS145 course project use.

genome-scores.csv: movieid, tagid, relevance, indicating that for each movie-tag pair, the strength of this pair. Tags are user-generated metadata about movies. Each tag is typically a single word or short phrase. The meaning, value, and purpose of a particular tag is determined by each user.

genome-tags.csv: tagid, tag, indicating that each tagid coresponding to a specific tag.

kaggle_sample_submission.csv: a sample submission.

movies.csv: movieid, title, genres, indicating each movie's name and corresponding genres.

tags_shuffled_rehashed.csv: userId, movieId and tag, indicating that each user assigns a movie a tag.

test_ratings.csv: test dataset. Please follow the format of the sample submission to submit your answer to this test set.

train_ratings.csv: training dataset. It consists of three fields: userId, movieId, and rating (binary: 0 indicating dislike and 1 indicating like).

val_ratings.csv: validation dataset with the same fields as the training dataset.


## Apriori Algorithm
Tried 2 methonds
1. From Website
   --apriori.py
   --validation.py
2. From Mlxtend
   --mlxtend.py
   --validate_ver2.py
Accuracy:
highest:0.53

# Command Line Options
Our program is executed with ./Program.py on Linux, with Shebang, interpreted by python3, or python3 Program.py on Windows.

## --data-folder x

`x` should be a path to the folder holding the dataset. If the specified folder doesn’t have data, the program will download one from Kaggle API. By default, `x` is `../data`.

## --model x

Choose a model to run. `x` should be a model name, choose from RandomForest or DecisionTree. By default `x` is `RandomForest`.

## --relevance x

Only tags with relevance greater than or equal to `x` will be considered as relevant tags to a movie. By default, `x` is `0.46`.

## --parallel x

If `x` is an integer, the program uses `x` processes. If `x` is `auto`, the program will determine the proper number of processes. By default, `x` is `auto`.

## --first-users x

The program will only test users whose ID is less than or equal to `x`. This option is for fast experiment. If this option is present, submit.csv will not be generated.

To reproduce our results, the following command line should be used:

```
./Program.py 
```

which is the same as

```
./Program.py --model RandomForest --parallel auto --relevance 0.46
```

The output is like this.
```
Classification using RandomForest starts with 4 processes.
[Thread 2] User 34972 is done. Progress is 1%. Used time is 77s. Remaining time is 7649s.
[Thread 2] User 68902 is done. Progress is 99%. Used time is 13314s. Remaining time is 134s.
[Thread 4] User 138148 is done. Progress is 99%. Used time is 13344s. Remaining time is 134s.
Fixed 47 empty prediction in table ValidationRatings.
Fixed 698 empty prediction in table TestRatings.
Successfully submitted to CS 145 Project
Used time: 13461.748700618744
Best accuracy is 0.6601360859924246. This accuracy is 0.7244378676327179.
```
