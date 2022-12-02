!pip install psycopg2-binary
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np



anime = pd.read_csv('anime.csv')
rating = pd.read_csv('rating.csv')


username = 'postgres'
password = 'PetroIsFucker55'
database = 'Lab2'
host = 'localhost'
port = 5433

query_1 = '''
CREATE VIEW GenreCount AS
SELECT genres.name_genre,COUNT(genre_anime.anime_id) as amount_genre FROM genre_anime
Join genres ON genres.genre_id = genre_anime.genre_id
GROUP BY genres.name_genre
order by amount_genre;

'''
query_2 = '''
CREATE VIEW RatingCount AS
SELECT ROUND(rating) as rating, COUNT(*) as amount_rating FROM anime
GROUP BY ROUND(rating)
ORDER BY amount_rating;

'''
query_3 = '''
CREATE VIEW RatingToMembers AS
Select Round(members,-4) as members,Round(AVG(rating),2) from anime
group by Round(members,-4)
order by members
'''

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)
print(type(conn))



with conn.cursor() as cursor:
    cursor.execute('DROP VIEW IF EXISTS GenreCount')
    cursor.execute(query_1)
    cursor.execute('SELECT * FROM GenreCount')
    geres_count = pd.DataFrame(cursor.fetchall()).rename(columns = {0:'genre', 1 : 'genre_count'})

plt.style.use('fivethirtyeight')
fig, ax = plt.subplots()
ax.barh(geres_count['genre'],geres_count['genre_count'])
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))




with conn.cursor() as cursor:
    cursor.execute('DROP VIEW IF EXISTS RatingCount')
    cursor.execute(query_2)
    cursor.execute('SELECT * FROM RatingCount')
    rating_count = pd.DataFrame(cursor.fetchall()).rename(columns = {0:'rating', 1 : 'rating_count'})

explode = (0, 0.1, 0, 0)  

fig1, ax1 = plt.subplots()

colors = plt.get_cmap('Blues')(np.linspace(0.2, 0.7, len(rating_count['rating_count'])))

wedges, texts, autotexts = ax1.pie(rating_count['rating_count'], explode=explode, labels=rating_count['rating'], colors=colors,autopct='%1.1f%%',
        shadow=True, startangle=90)

ax1.axis('equal')  

ax1.legend(wedges,rating_count['rating'],
          title="Ratings",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))

plt.show()






with conn.cursor() as cursor:
    cursor.execute('DROP VIEW IF EXISTS RatingToMembers')
    cursor.execute(query_3)
    cursor.execute('SELECT * FROM RatingToMembers')
    rate_mambers = pd.DataFrame(cursor.fetchall()).rename(columns = {0:'members', 1 : 'rating'})


plt.style.use('ggplot')
fig2, ax2 = plt.subplots()
ax2.plot(rate_mambers['members'],rate_mambers['rating'], linewidth = 2)
ax2.set_xlabel('members')
ax2.set_ylabel('rating')
