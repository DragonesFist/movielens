# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 23:25:59 2020

@author: 240022854
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder 
from sklearn.linear_model import LinearRegression  
from sklearn.model_selection import train_test_split
from sklearn.metrics import max_error

#reading the data
data = pd.read_csv("u.data",sep="\t", header=None)
data.columns = ["user_id", "movie_id","rating", "timestamp"]

#reading genres
genre = pd.read_csv("u.genre", sep="|", header=None)
genre.columns = ["genre","genre_id"]

#reading items(movies)
items = pd.read_csv("u.item", sep="|", header=None,encoding = "ISO-8859-1") #encoding is added to avoid any unicode errors, you can safely remove it if you dont see any errors
items_columns = ["movie_id" , "movie_title", "release_date", "video_release_date","IMDb_URL", "unknown","Action","Adventure","Animation","Children's" ,"Comedy","Crime","Documentary","Drama","Fantasy","Film-Noir",  "Horror","Musical","Mystery","Romance","Sci-Fi","Thriller","War","Western"]
items.columns = items_columns

#reading info -- space separated
info = pd.read_csv("u.info"," ", header = None)
info.columns= ["Count", "Category"]


#reading occupation
occupation = pd.read_csv("u.occupation", header=None)
occupation.columns = ["Occupation"]

#reading user
user = pd.read_csv("u.user", header=None, sep="|")
user.columns = ["user_id", "age", "gender", "occupation" ,"zip_code"]

#combining the data

data_combined = data.copy(deep=True) #deep copy is used to eliminate any dependency/changes to master datafrome
data_combined = data_combined.drop(["timestamp"], axis=1)
#adding additinal columns to dataframe

data_combined = data_combined.merge(user, how = "outer", on="user_id")
#addind mvovie info

data_combined = data_combined.merge(items, how ="outer", on="movie_id")


#encoding the data
#label encoder for gender
le = LabelEncoder()
data_combined["gender"] = le.fit_transform(data_combined["gender"])
data_combined["occupation"] = le.fit_transform(data_combined["occupation"])

#dropping few columns
data_combined.drop(["movie_title","release_date","video_release_date","IMDb_URL"],axis=1,inplace=True)

#applying linear regression

labels = data_combined["rating"]
data_combined.drop(["rating","zip_code"], inplace=True, axis=1)

X_train, X_test, y_train, y_test = train_test_split(data_combined, labels, test_size=0.33, random_state=42)
reg = LinearRegression().fit(X_train, y_train)
reg.coef_
reg.intercept_

y_pred = reg.predict(X_test)
y_pred= pd.DataFrame(y_pred)






