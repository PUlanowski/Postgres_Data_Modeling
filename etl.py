import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    Processing song file and populating DB tables.

    Parameters
    ----------
    cur : TYPE
        DESCRIPTION.
    filepath : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    # open song file

    df = pd.DataFrame()
    df = pd.read_json(filepath,lines=True)

    # insert song record
    songs_df = df[['song_id', 'title', 'artist_id', 'year','duration']]
    song_data = songs_df.values[0].tolist()
    cur.execute(song_table_insert, song_data)

    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude','artist_longitude']]
    artist_data = artist_data.values[0].tolist()
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    '''
    Processing log file and populating DB tables.
    
    Parameters
    ----------
    cur : attributes
        paramater for psycopg2
    filepath : TYPE: string
        filepaths to both song and log files

    Returns
    -------
    None.

    '''
    # open log file
    df = pd.DataFrame()
    df = pd.read_json(filepath,lines=True)

    # filter by NextSong action
    df_nextsong = df.loc[(df.page == 'NextSong')]

    # convert timestamp column to datetime
    time_df = pd.DataFrame()
    ts = df_nextsong[['ts']]
    ts = pd.to_datetime(ts['ts'], unit = 'ms')
    
    # insert time data records
    column_labels = ('start_time','hour','day','weekofyear','month','year','weekday')
    time_data = (ts, ts.dt.hour, ts.dt.day, ts.dt.weekofyear, ts.dt.month, ts.dt.year, ts.dt.weekday)
    time_df = pd.DataFrame(dict(zip(column_labels, time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']] 

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            print(results)
            songid, artistid = results
            print(songid, artistid)
        else:
            songid, artistid = None, None

        # insert songplay record
    songplay_data = (row.ts, row.userId, row.level, songid, artistid,\
                     row.sessionId, row.location, row.userAgent)
    cur.execute(songplay_table_insert, songplay_data)



def process_data(cur, conn, filepath, func):
    '''
    This function is processing and checking files from songs and log json repository.

    Parameters
    ----------
    cur : function
        paramater for psycopg2
    conn : function
        connection to database with connection attributes
    filepath : TYPE: string
        filepaths to both song and log files
    func : TYPE: variable
        invoke function

    Returns
    -------
    all_files : list
        list of json files from song ang log repository

    '''
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))
        
        
def main():
    '''
    Orchestrating whole etl script.
    Input are connection to appropriate database.
    -------
    None.

    '''
    #priv: conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=")
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()