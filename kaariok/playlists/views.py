from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import Q

from django.db.models import Count

from kaariok.playlists.models import Playlist, PlaylistItem
from kaariok.songs.models import Song
from django.contrib.auth.models import User

from kaariok.songs.views import song_detail

def user_playlist_page(request):
    return user_playlist(request, request.user.id)

def user_playlist(request, user_id):
    playlist = None
    if user_id is "master":
        playlist = Playlist.get_or_create_master_playlist()
    else:
        playlist = Playlist.get_or_create(user_id)
    items = PlaylistItem.objects.filter(playlist=playlist, active=True).order_by('position')
        
    playlist_html = render_to_string('playlists/partial/playlist.html',
        {
            'items' : items,
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
    playlist.add_song(Song.objects.get(id=song_id), request.user)
    
    return song_detail(request, song_id, True)
    
def remove_item_from_playlist(request, item_id):
    playlist = Playlist.get_or_create(request.user.id)
    playlist.remove_item(PlaylistItem.objects.get(id=item_id))

    return user_playlist(request, request.user.id)
    
def move_item_up(request, item_id):
    playlist = Playlist.get_or_create(request.user.id)
    item = PlaylistItem.objects.get(id=item_id)
    item.move_up()
    
    return user_playlist(request, request.user.id)
    
def move_item_down(request, item_id):
    playlist = Playlist.get_or_create(request.user.id)
    item = PlaylistItem.objects.get(id=item_id)
    item.move_down()

    return user_playlist(request, request.user.id)
    
def master_playlist(request, internal=False):
    playlist = Playlist.get_or_create_master_playlist()
    items = PlaylistItem.objects.filter(playlist=playlist, active=True).order_by('position')
    playlist_html = render_to_string('playlists/partial/mini_playlist.html',
        {
            'items' : items,
        },
         context_instance=RequestContext(request)
    )
    
    playlists = Playlist.objects.filter(user__is_active=True).annotate(num_items=Count('playlistitem'))
    playlists = playlists.filter(num_items__gt=0).order_by('name')

    if request.is_ajax() or internal:
        output = {
            'html' : playlist_html,
        }
        return HttpResponse(simplejson.dumps(output))
    else:
        return render_to_response('playlists/master_playlist.html',
        {
            'playlists':playlists,
            'master_playlist':playlist_html,
        },
        context_instance=RequestContext(request))
    
def master_add_playlist(request, user_id):
    playlist = Playlist.get_or_create(user_id)
    items = playlist.playlistitem_set.filter(active=True).order_by('position')
    
    playlist_html = render_to_string('playlists/partial/master_add_playlist.html',
        {
            'items' : items,
        },
         context_instance=RequestContext(request)
    )
    
    output = {
        'html' : playlist_html,
    }
    return HttpResponse(simplejson.dumps(output))

def add_item_to_master_playlist(request, item_id):
    playlist = Playlist.get_or_create_master_playlist()
    item = PlaylistItem.objects.get(id=item_id)
    playlist.add_item(item)
        
    return master_playlist(request, internal=True)

def move_item_up_on_master_list(request, item_id):
    playlist = Playlist.get_or_create_master_playlist()
    item = PlaylistItem.objects.get(id=item_id)
    item.move_up()

    return master_playlist(request, internal=True)
    
def move_item_down_on_master_list(request, item_id):
    playlist = Playlist.get_or_create_master_playlist()
    item = PlaylistItem.objects.get(id=item_id)
    item.move_down()

    return master_playlist(request, internal=True)
 
def remove_item_from_master_playlist(request, item_id):
    item = PlaylistItem.objects.get(id=item_id)
    owner_playlist = Playlist.get_or_create(item.owner.id)
    
    owner_playlist.add_item(item)

    return master_playlist(request, internal=True)