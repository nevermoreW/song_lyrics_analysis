from PyLyrics import *
import warnings
import nltk
from collections import Counter
import billboard
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

warnings.filterwarnings("ignore")


##
# Downloads the lyrics for a song.
# Pre-processing consists of removing "Features",
# " x " from the song artist. To comply by lyrics.wikia
# standards.
#
##
# Newlines, ",", ".", "(", ")", are removed
# and a string of words are returned.
# Throws a ValueError if lyrics are not found
def download_lyrics(song_artist, song_title):
    song_artist_temp=song_artist
    song_title_temp=song_title

    song_artist_temp=song_artist_temp.partition("Featuring")[0]
    song_artist_temp=song_artist_temp.partition(" x ")[0]

    lyrics=PyLyrics.getLyrics(song_artist_temp, song_title_temp)
    lyrics=lyrics.replace(",", "")
    lyrics=lyrics.replace(".", "")
    lyrics=lyrics.replace("(", "")
    lyrics=lyrics.replace(")", "")
    lyrics=lyrics.replace("\n", " ")
    lyrics=lyrics.replace('"',"")
    lyrics=lyrics.replace(";","")
    lyrics=lyrics.replace("?","")
    lyrics=lyrics.lower()
    return lyrics

def word_counter(words):
    list_of_words=[]
    for word in words.split():
        list_of_words.append(word)
    return Counter(list_of_words)

def word_type(words):
    text=set(words.split())
    text=' '.join(text)
    text=nltk.word_tokenize(text)
    text=nltk.pos_tag(text)
    return text

def get_certain_type_words(words, types):
    relevant_words=[]
    for word in words:
        if word[1] in types:
            relevant_words.append(word[0])
    return relevant_words

def n_lyrics_from_chart(chart='hot-100', n=10, date="2017-01-10"):
    chart=billboard.ChartData(chart, date=date)
    lyrics=""
    for char in chart[0:n]:
        song_artist=char.artist
        song_title=char.title
        try:
            lyrics=lyrics+ download_lyrics(song_artist, song_title)
        except ValueError:
            print "Skipping: %s %s" %(song_artist, song_title)
    return lyrics

lyrics=n_lyrics_from_chart()

relevant_words=get_certain_type_words(word_type(lyrics), set(['JJ', 'JJR','JJS', 'RB', 'RBR', 'RBS',
                                                              'VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']))
print relevant_words

    
    
