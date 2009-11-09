from django.contrib import admin
from kaariok.playlists.models import Playlist, PlaylistItem

admin.site.register(Playlist)
admin.site.register(PlaylistItem)
