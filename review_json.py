import openai
import csv, json
import time

openai.api_key = "key_name_here"
embedding_model_name = "text-embedding-ada-002"

count = 100
moviedata = {}
movietitle = {}
with open("new_movies") as csvfile:
    rows = csv.reader(csvfile, delimiter=",")
    for row in rows:
        movieid = row[0]
        title = row[1]
        movietitle[movieid] = title

with open("rotten_tomatoes_movie_reviews.csv") as csvfile:
    rows = csv.reader(csvfile, delimiter=",")
    for row in rows:
        if row[1] not in moviedata:
            moviedata[row[1]] = {}
        if row[0] not in movietitle:
            continue
        title = movietitle[row[0]]
        reviewid = row[1]
        moviedata[reviewid]["title"] = movietitle[row[0]]
        moviedata[reviewid]["reviewid"] = row[1]
        moviedata[reviewid]["creationdate"] = row[2]
        moviedata[reviewid]["criticname"] = row[3]
        moviedata[reviewid]["originalscore"] = row[5]
        moviedata[reviewid]["reviewstate"] = row[6]
        moviedata[reviewid]["reviewtext"] = row[8]

returnarray = []
for review in moviedata:
    if count == 0:
        break
    count -= 1
    result = openai.Embedding.create(
        input=moviedata[review]["reviewtext"], engine=embedding_model_name
    )
    moviedata[review]["embedding"] = result.data[0].embedding
    time.sleep(1)
    returnarray.append(moviedata[review])


print(json.dumps(moviedata))
