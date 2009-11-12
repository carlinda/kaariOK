from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import Q

from kaariok.playlists.models import Playlist, PlaylistItem
from kaariok.songs.models import Song
from django.contrib.auth.models import User

from kaariok.songs.views import song_detail

def user_playlist(request, user_id):
    playlist = Playlist.get_or_create(user_id)
    items = PlaylistItem.objects.filter(playlist=playlist, active=True).order_by('position')
    songs = [item.song for item in items]
    
    above1 = [item.get_item_above_me() for item in items]
    below1 = [item.get_item_below_me() for item in items]
    above = []
    for item in items:
        above_me = item.get_item_above_me()
        if above_me is not None:
            above.append(above_me.song)
        else:
            above.append(None)
            
    below = []
    for item in items:
        below_me = item.get_item_below_me()
        if below_me is not None:
            below.append(below_me.song)
        else:
            below.append(None)
    return render_to_response('playlists/user_playlist.html',
    {
        'songs' : songs,
        'above' : above,
        'below' : below,
    },
    context_instance=RequestContext(request))
    
def add_song_to_playlist(request, song_id):
    playlist = Playlist.get_or_create(request.user.id)
    playlist.add_song(Song.objects.get(id=song_id))
    
    return song_detail(request, song_id, True)
    
def remove_song_from_playlist(request, song_id):
    playlist = Playlist.get_or_create(request.user.id)
    playlist.remove_song(Song.objects.get(id=song_id))

    return song_detail(request, song_id, True)