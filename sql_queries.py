# DROP TABLES
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# Quotations indicate that query string uses multiple lines
songplay_table_create = (""" 
    CREATE TABLE IF NOT EXISTS songplays 
    (songplay_id INT PRIMARY KEY, 
    start_time TIMESTAMP REFERENCES time(start_time), 
    user_id INT NOT NULL REFERENCES users(user_id),
    level TEXT, 
    song_id TEXT REFERENCES songs(song_id), 
    artist_id TEXT REFERENCES artists(artist_id), 
    session_id INT, 
    location TEXT,
    user_agent TEXT) 
""")

# user_table_create = (""" 
#    CREATE TABLE IF NOT EXISTS users 
#    (user_id INT NOT NULL PRIMARY KEY, 
#    first_name TEXT NOT NULL, 
#    last_name TEXT NOT NULL, 
#    gender TEXT, 
#    level TEXT)
# """)

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users
    (user_id int NOT NULL, 
    first_name text NOT NULL, 
    last_name text NOT NULL, 
    gender text, 
    level text,
    PRIMARY KEY (user_id))
""")

song_table_create = (""" 
    CREATE TABLE IF NOT EXISTS songs 
    (song_id TEXT PRIMARY KEY, 
    title TEXT NOT NULL, 
    artist_id TEXT NOT NULL REFERENCES artists(artist_id), 
    year INT, 
    duration FLOAT NOT NULL)
""")

artist_table_create = (""" 
    CREATE TABLE IF NOT EXISTS artists 
    (artist_id TEXT PRIMARY KEY, 
    name TEXT NOT NULL, 
    location TEXT, 
    lattitude FLOAT, 
    longitude FLOAT)
""")

time_table_create = (""" 
    CREATE TABLE IF NOT EXISTS time 
    (start_time TIMESTAMP PRIMARY KEY, 
    hour INT, 
    day INT, 
    week INT, 
    month INT, 
    year INT, 
    weekday TEXT)
""")

# INSERT RECORDS

songplay_table_insert = (""" 
    INSERT INTO songplays 
    (songplay_id, 
    start_time, 
    user_id,
    level, 
    song_id, 
    artist_id, 
    session_id, 
    location,
    user_agent) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (songplay_id) DO NOTHING;
""")

user_table_insert = (""" 
    INSERT INTO users
    (user_id, 
    first_name, 
    last_name, 
    gender, 
    level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id) DO NOTHING;
""")

song_table_insert = (""" 
    INSERT INTO songs
    (song_id, 
    title, 
    artist_id, 
    year, 
    duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id) DO NOTHING;
""")

artist_table_insert = (""" 
    INSERT INTO artists
    (artist_id, 
    name, 
    location, 
    lattitude, 
    longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id) DO NOTHING;
""")


time_table_insert = (""" 
    INSERT INTO time
    (start_time, 
    hour, 
    day, 
    week, 
    month, 
    year, 
    weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time) DO NOTHING;
""")

# FIND SONGS
# Implement the song_select query in sql_queries.py to find the song ID and artist ID based on the title, artist name, and duration of a song.

song_select = (""" 
    SELECT 
        song_id, 
        artists.artist_id 
    FROM songs
    JOIN artists
    ON songs.song_id = artists.artist_id
    WHERE artists.name = %s
    AND songs.title = %s 
    AND songs.duration = %s;
""")

# QUERY LISTS
# Note 1: Order matters. Start creating first dimension tables and last fact tables.
# Note 2: Also start creating tables with no REFERENCE statements. 

create_table_queries = [time_table_create, user_table_create, artist_table_create, song_table_create, songplay_table_create]
drop_table_queries = [time_table_drop, user_table_drop, artist_table_drop, song_table_drop, songplay_table_drop]