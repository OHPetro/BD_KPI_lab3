SELECT * FROM genre_anime;
CREATE TABLE genre_anime_copy AS SELECT * FROM genre_anime; 
DELETE FROM genre_anime_copy;
SELECT * FROM genre_anime_copy;


DO $$
 DECLARE
	 anime_id genre_anime_copy.anime_id%TYPE;
	 genre_id genre_anime_copy.genre_id%TYPE;

 BEGIN
     anime_id := 1;
	 genre_id := 1;
	 
     FOR counter IN 1..20
         LOOP
            INSERT INTO genre_anime_copy (anime_id, genre_id)
             VALUES (counter, floor(random()*(10-1+1))+1);
         END LOOP;
 END;
 $$
 
SELECT * FROM genre_anime_copy;
