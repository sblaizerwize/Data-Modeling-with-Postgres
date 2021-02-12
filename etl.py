import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """
    - Reads the JSON filepath
    - Drops any NULL fields
    - Extracts the required fields for artist and song tables
    - Loads records into artist and song tables
    """

    # open song file
    df = pd.read_json(path_or_buf=filepath, lines=True)
    # drop records with no userId
    df.dropna(axis=0, how='any', inplace=True)
    
    for value in df.values:
        num_songs, artist_id, artist_latitude, artist_longitude, artist_location, artist_name, song_id, title, duration, year = value

        # insert artist record
        artist_data = [artist_id, artist_name, artist_location, artist_latitude, artist_longitude]
        cur.execute(artist_table_insert, artist_data)
    
        # insert song record
        song_data = [song_id, title, artist_id, year, duration]
        cur.execute(song_table_insert, song_data)
        
def process_log_file(cur, filepath):
    """
    - Reads the JSON filepath
    - Drops any NULL fields
    - Extracts the timestamp field
    - Transforms timestamp into datetime type
    - Loads records into time table
    - Extracts and loads records into user table
    - Extracts and transforms the required fields for songplay table
    - Loads records into songplay table
    """

    # open log file
    df = pd.read_json(path_or_buf=filepath, lines=True)
    
    # drop records with no userId
    df.dropna(axis=0, how='any', inplace=True)

    # LOAD TIME TABLE
    ## filter by NextSong action
    df_time = df[df['page']=='NextSong']['ts']
    
    ## transformation to all the timestamp column
    t = pd.to_datetime(df_time, unit='ms')
    
    ## extract the timestamp, hour, day, week of year, month, year, and weekday
    time_data = [t.to_list(), t.dt.hour.to_list(), t.dt.day.to_list(), t.dt.weekofyear.to_list(), t.dt.month.to_list(), t.dt.year.to_list(), t.dt.day_name().to_list()]

    ## create dictionary
    column_labels = ['start_time','hour','day','week','month','year','weekday']
    time_data_dict = {}
    j = 0 
    for i in column_labels:
        time_data_dict[i]= time_data[j]
        j += 1

    ## transform dictionary into dataframe
    time_df = pd.DataFrame.from_dict(time_data_dict)
    
    ## insert time data records
    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, row)

    # -------------------------------------

    # LOAD USER TABLE
    user_df = df[['userId','firstName','lastName', 'gender', 'level']]
    
    ## drop records with no userId
    # user_df.dropna(axis=0, how='any', inplace=True)

    ## insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)  
        
    # -------------------------------------
    # LOAD SONGPLAY TABLE
    ## drop records with no userId
    # df.dropna(axis=0, how='any', inplace=True)
    
    ## insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (index, pd.to_datetime(row.ts, unit='ms'), int(row.userId), row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)  
        
        
def process_data(cur, conn, filepath, func):
    """
    - Appends all JSON files into a list
    - Gets the total number of files to be processed
    - Processes every single file 
    """

    # get all files matching extension from directory
    # EXAMPLE 
    # TRAAAAW128F429D538.json
    # TRAAABD128F429CF47.json
    # TRAAADZ128F9348C2E.json
    
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    # EXAMPLE
    # '100 files found in data/song_data'
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    # EXAMPLE
    # 10/100 files processed.
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """
    - Starts a pyscopg2 connections to sparkifydb
    - Gets a cursor
    - Processes song_data and log_data files
    - Closses connection 
    """

    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()