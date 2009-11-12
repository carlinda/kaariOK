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
    
    playlist_html = render_to_string('playlists/partial/playlist.html',
        {
            'songs' : songs,
        },
         context_instance=RequestContext(request)
    )
    if request.is_ajax():
        output = {
            'html' : playlist_html,
        }
        return HttpResponse(simplejson.dumps(output))
    else:
        return render_to_response('playlists/user_playlist.html',
        {
            'playlist_html' : playlist_html,
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
    
def move_song_up(request, song_id):
    playlist = Playlist.get_or_create(request.user.id)
    song=Song.objects.get(id=song_id)
    item = PlaylistItem.objects.get(playlist=playlist, song=song, active=True)
    item.move_up()
    
    return user_playlist(request, request.user.id)
    
def move_song_down(request, song_id):
    playlist = Playlist.get_or_create(request.user.id)
    song=Song.objects.get(id=song_id)
    item = PlaylistItem.objects.get(playlist=playlist, song=song, active=True)
    item.move_down()

    return user_playlist(request, request.user.id)