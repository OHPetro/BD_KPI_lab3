import csv
import psycopg2


username = 'postgres'
password = 'PetroIsFucker55'
database = 'Lab2'
host = 'localhost'
port = 5433

OUTPUT_FILE_T = 'Maiushko_DB_{}.csv'

TABLES = [
    'anime',
    'genre_anime',
    'genres',
    'type_',
    'user_',
    'user_rating',
]

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn.cursor() as cursor:
    for table_name in TABLES:
        cursor.execute('SELECT * FROM ' + table_name)
        fields = [x[0] for x in cursor.description]
        with open(OUTPUT_FILE_T.format(table_name), 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cursor:
                writer.writerow([str(x) for x in row])
