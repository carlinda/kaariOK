from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import Q

from kaariok.playlists.models import Playlist, PlaylistItem
from kaariok.songs.models import Song
from django.contrib.auth.models import User

def user_playlist(request, user_id):
    playlist = Playlist.get_or_create(user_id)
    items = PlaylistItem.objects.filter(playlist=playlist, active=True)
    songs = [item.song for item in items]
    
    return render_to_response('playlists/user_playlist.html',
    {
        'songs' : songs,
    },
    context_instance=RequestContext(request))