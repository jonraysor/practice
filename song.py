import re


class Song:
    def __init__(self, artist, song, release_date, label_abbreviation, genre, core_genre, date_selected, release_age):
        self.id = re.sub('[^A-Za-z0-9]+', '', song) + re.sub('[^A-Za-z0-9]+', '', artist)
        self.artist = artist
        self.song = song
        self.date = release_date
        self.label = label_abbreviation
        self.genre = genre
        self.core = core_genre
        self.date = date_selected
        self.age = release_age
        self.consumption = {}
        self.sales = {}
        self.audio = {}
        self.video = {}
        self.ondemand = {}





