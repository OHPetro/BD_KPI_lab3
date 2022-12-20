!pip install psycopg2-binary
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np
import csv
import psycopg2
import psycopg2.extras
import random 
from itertools import islice


username = 'postgres'
password = 'PetroIsFucker55'
database = 'Lab2'
host = 'localhost'
port = 5433
conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
print(type(conn))



## Genres

query_1 = '''
DELETE FROM genres
'''
query_2 = '''
INSERT INTO genres (genre_id, name_genre) Values (%s, %s)
'''



def import_genre(cur):
    cur.execute(query_1)
    df = pd.read_csv('anime.csv')
    
    full = []
    temp = []
    for i in range(0,500):
        temp = df.genre[i].replace(',','').split()
        full.extend(temp)
    res_serie_of_genres = pd.Series(full).unique()
    
    for row in range(0,len(res_serie_of_genres)):

        genre_name = res_serie_of_genres[row]
        genre_id = row
        
        
        values = [genre_id, genre_name]
        cur.execute(query_2, values)
        
with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    cursor.execute(query_1)
    import_genre(cursor)
    conn.commit()
    
    
    
    
    ## User


query_5 = '''
DELETE FROM user_
'''
query_6 = '''
INSERT INTO user_ (user_id, user_nickname) Values (%s, %s)
'''       
        
def import_user(cur):
    cur.execute(query_5)
    with open("rating.csv") as csv_file:

        df = pd.read_csv('rating.csv')
        

        full_user_id = df['user_id'].unique()
        for i in range(0,len(full_user_id)):
            user_id = int(full_user_id[i])
            user_nickname = 'user'+ str(i)

            values = [user_id, user_nickname]
            cur.execute(query_6, values)
            
with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    import_user(cursor)
    conn.commit()
    
    
    
    # Anime


query_7 = '''
DELETE FROM Anime
'''
query_8 = '''
INSERT INTO Anime (anime_id, anime_name, anime_type, members, episodes, rating) Values (%s, %s,%s, %s,%s, %s)
'''  
            
def import_anime(cur):
    cur.execute(query_7)
    with open("anime.csv",encoding="utf-8") as csv_file:
        
        for i in range(0,300):
            for row in csv.DictReader(csv_file):
                anime_id = row['anime_id']
                anime_name = row['name']
                members = row['members']
                episodes = row['episodes']
                rating = str(random.randint(1,10))
                anime_type = row['type']

                #if not row['type']:
                    #continue 
                #type_id = row['type']
                #cur.execute('select type_id from type_ where type_name = %s', (type_id,))
                #type_id = cur.fetchone()[0]

                values = [anime_id, anime_name, anime_type, members, episodes, rating]
                cur.execute(query_8, values)

with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    import_anime(cursor)
    conn.commit()
    
    
##  genre_anime

query_9 = '''
DELETE FROM genre_anime
'''
query_10 = '''
INSERT INTO genre_anime (genre_id, anime_id) Values (%s, %s)
'''  
            
def Genre_anime(cur):
    cur.execute(query_9)
    with open("anime.csv",encoding="utf-8") as csv_file:

        for row in csv.DictReader(csv_file):
            temp_genres = row['genre'].replace(',','').split()

            if not row['anime_id']:
                continue
            anime_id = row['anime_id']
            cur.execute('select anime_id from anime where anime_id = %s', (anime_id,))
            anime_id = cur.fetchone()
            if anime_id is None:
                continue
            anime_id = anime_id[0]

            for genre in temp_genres:


                cur.execute('select genre_id from Genres where name_genre = %s', (genre,))

                genre_id = cur.fetchone()
                if genre_id is None:
                    continue
                genre_id = genre_id[0]

                values = [genre_id,anime_id]
                cur.execute(query_10, values)
with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    Genre_anime(cursor)
    conn.commit()
    
    
df= pd.read_csv('rating.csv')
df = df.head(1000)
df.to_csv('dd.csv')

query_11 = '''
DELETE FROM user_rating
'''
query_12 = '''
INSERT INTO user_rating ( user_rating_id, anime_id, user_id, user_rating) Values (%s, %s, %s, %s)
'''  
            
def User_rating(cur):
    cur.execute(query_11)
    with open("dd.csv",encoding="utf-8") as csv_file:
        user_rating_id = 0 
        for row in csv.DictReader(csv_file):
            
     
            user_rating_id = user_rating_id + 1


            if int(row['rating']) < 0 :
                continue
            user_rating = row['rating']



            anime_id = row['anime_id']
            cur.execute('select anime_id from anime where anime_id = %s', (anime_id,))
            anime_id = cur.fetchone()
            if anime_id is None:
                continue
            anime_id = anime_id[0]



            user_id = row['user_id']
            cur.execute('select user_id from user_ where user_id = %s', (user_id,))
            user_id = cur.fetchone()
            if user_id is None:
                continue
            user_id = user_id[0]



            values = [user_rating_id, anime_id, user_id, user_rating]
            cur.execute(query_12, values)
with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
    User_rating(cursor)
    conn.commit()
