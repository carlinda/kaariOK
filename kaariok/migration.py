import sqlite3
from kaariok.songs.models import Song, Artist, Album, Language
from django.contrib.auth.models import User
from kaariok.users.models import Rating

# big output hash
output = []

con = sqlite3.connect("kaariok.sqlite")

c = con.cursor()

# Migration by parts:

# Migrate artists
c.execute('SELECT ar_nombre, ar_fotito, ar_fotito_type, ar_id FROM artistas')
artists = {}
for artist in c:
    if artist[1] is not None and artist[1] != '' and artist[1] != ' ':
#         type = artist[2].split("/")
#         if type == 'jpeg':
#             type = 'jpg'
#         filename = artist[0] + "."+type
#         FILE = open(filename, "w")
#         FILE.write(artist[1])
#         FILE.close()
#         artista = Artist(id=ar_id, name=artist[0], picture=filename)
        artista = Artist(name=artist[0])
    else:
        artista = Artist(name=artist[0])
    artista.save()
    artists[artist[3]] = artista

# Albums
c.execute('SELECT cd_codigo, cd_id from discos')

discs = {}
for disc in c:
    album = Album(code=disc[0])
    album.save()
    discs[disc[1]] = album

# songs
c.execute('SELECT kar_cancion, kar_filename, kar_track, kar_aprobado, kar_codigo, kar_artista, kar_lang, kar_id FROM canciones')
songs = {}
for song in c:
    language = None
    if song[6] == 'E' or song[6] == "'E'":
        language = Language.objects.get(pk=2)
    elif song[6] == 'S':
        language = Language.objects.get(pk=1)
    else:
        language = None
    cancion = Song(name=song[0], filename=song[1], track=song[2], approved=song[3], album=discs[song[4]], artist=artists[song[5]], language=language)
    cancion.save()
    songs[song[7]] = cancion

# user ratings
c.execute('SELECT usr_id, kar_id, com_conocido FROM comentarios')
for rating in c:
    rate = ''
    if rating[2] == 'LOVE':
        rate = 'love'
    elif rating[2] == 'NO':
        rate = 'hate'
    elif rating[2] == 'SI':
        rate = 'known'
    elif rating[2] == 'NO SE':
        rate = 'hate'
    else:
        rate = None

    user = None
    if rating[0] == 'carlita':
        user = User.objects.get(username='Carli')
    elif rating[0] == 'pedratan':
        user = User.objects.get(username='Pedro')
    else:
        user = None

    try: 
        comentario = Rating(user=user, song=songs[rating[1]], comment='', value=rate)
        comentario.save()
    except KeyError:
        pass

con.close()
