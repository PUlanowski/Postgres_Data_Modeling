# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS artists"
song_table_drop = "DROP TABLE IF EXISTS users"
artist_table_drop = "DROP TABLE IF EXISTS songs"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("CREATE TABLE IF NOT EXISTS songplays(\
                songplay_id integer CONSTRAINT pk_songplays PRIMARY KEY,\
                start_time timestamp UNIQUE,\
                user_id integer UNIQUE,\
                level varchar,\
                song_id varchar UNIQUE,\
                artist_id varchar UNIQUE,\
                session_id integer,\
                location varchar,\
                user_agent varchar);")

artist_table_create = ("CREATE TABLE IF NOT EXISTS artists(\
                artist_id varchar CONSTRAINT pk_artists PRIMARY KEY,\
                name varchar,\
                location varchar,\
                latitude float,\
                longitude float,\
                CONSTRAINT fk_artists FOREIGN KEY(artist_id)\
                    REFERENCES songplays(artist_id));")

user_table_create = ("CREATE TABLE IF NOT EXISTS users(\
                user_id integer CONSTRAINT pk_users PRIMARY KEY,\
                first_name varchar,\
                last_name varchar,\
                gender varchar,\
                level varchar,\
                CONSTRAINT fk_users FOREIGN KEY(user_id)\
                    REFERENCES songplays(user_id));")

song_table_create = ("CREATE TABLE IF NOT EXISTS songs(\
                song_id varchar CONSTRAINT pk_songs PRIMARY KEY,\
                title varchar,\
                artist_id varchar,\
                year integer,\
                duration float,\
                CONSTRAINT fk_songs FOREIGN KEY(song_id)\
                    REFERENCES songplays(song_id));")

time_table_create = ("CREATE TABLE IF NOT EXISTS time(\
                start_time timestamp CONSTRAINT pk_time PRIMARY KEY,\
                hour time,\
                day integer,\
                week integer,\
                month integer,\
                year integer,\
                weekday integer,\
                CONSTRAINT fk_time FOREIGN KEY(start_time)\
                    REFERENCES songplays(start_time));")
                
# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""
""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]