from django.contrib import admin
from kaariok.songs.models import Language, Album, Artist, Song

admin.site.register(Language)
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Song)
