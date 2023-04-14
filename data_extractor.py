import pandas as pd
import re
import json
from song import Song
from activity_types import Activity

"""
JSON is utilized as the output our statistics to allow for a highly adoptable and usable output. Seeing that the 
team utilizes Django and does serve request to users via APIs, JSON is a web native format and is most optimal for 
this use case. In addition, there are many libraries to work with JSON across all languages which makes this output 
accessible to other projects. 
"""


def get_data(file):
    report = pd.ExcelFile(file)
    sheets = report.sheet_names
    data_frames = {sheet: report.parse(sheet) for sheet in sheets}
    songs = {}
    for key in data_frames:
        if key == 'Report Summary':
            songs = get_entity_selections(transform_report_summary(data_frames[key]))
        if key != 'Report Summary':
            data_frames[key] = data_frames[key].iloc[0:]
            data_frames[key] = data_frames[key].dropna(axis=1, how='all')
            song_frame = transform_song_info(data_frames[key])
            song = create_song(song_frame)
            (get_stats(transform_frame(data_frames[key]), song, songs))
    for key in songs.keys():
        if not songs[key]:
            print("WARNING:", key, " has no statistics")
    with open('./data/report.json', 'w') as file:
        json.dump(songs, file)


def transform_report_summary(data_frame):
    """

    :param data_frame:
    :return:  format the report summary
    """
    data_frame = data_frame.transpose()
    header = list(data_frame.iloc[0])
    data_frame.columns = header
    return data_frame


def get_entity_selections(data_frame):
    """

    :param data_frame:
    :return: gather the entity selections
    """
    songs = data_frame['Entity Selection'].values[1].split('\n')
    parsed_songs = {}
    for song in songs:
        substrings = ['Song:', 'Artist:']
        for substring in substrings:
            song = song.replace(substring, "")
        song = re.sub('[^A-Za-z0-9]+', '', song)
        parsed_songs[song] = None
    return parsed_songs


def transform_song_info(data_frame):
    """

    :param data_frame:
    :return: format information from each sheet
    """
    song_frame = data_frame.iloc[0:8, 0:].T
    song_frame = song_frame.iloc[:2]
    header = list(song_frame.iloc[0])
    song_frame = song_frame.tail(-1)
    song_frame.columns = header
    return song_frame


def create_song(data_frame):
    """

    :param data_frame:
    :return: create song dictionary
    """
    song_info = data_frame.iloc[0]
    song_info = {keys.lower(): key for keys, key in song_info.to_dict().items()}
    song_info = {keys.replace(' ', '_'): key for keys, key in song_info.items()}
    return Song(**song_info)


def transform_frame(data_frame):
    """

    :param data_frame:
    :return: clean up song sheets
    """
    columns_to_remove = ['Market', 'Retailer/Provider', 'ISRC/Barcode']
    drop_indices = range(0, 10)
    header = list(data_frame.iloc[9])
    data_frame = data_frame.drop(index=drop_indices)
    data_frame.columns = header
    data_frame = data_frame.drop(columns_to_remove, axis=1)
    return data_frame


def get_stats(data_frame, song, final_report):
    """

    :param data_frame:
    :param song:
    :param final_report:
    :return: gather all required statistics about the songs within the dictionary
    """
    activity = ''
    for _, row in data_frame.iterrows():
        if row['Activity']:
            activity = Activity[re.sub('[^A-Za-z0-9]+', '', row['Activity'])].value.lower()
        for col in row.index:
            if col.startswith('Week'):
                attribute = getattr(song, activity)
                attribute[col] = row[col]
            if col.startswith('ATD'):
                attribute = getattr(song, activity)
                attribute[col] = row[col]
        final_report[song.id] = vars(song)
    return final_report
