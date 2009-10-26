from django.shortcuts import render_to_response
from django.template import RequestContext

from kaariok.songs.models import Song

def song_search(request):
    songs = Song.objects.all().extra(select={'name_upper' : 'upper(name)'}).order_by('name_upper')
    
    return render_to_response('songs/search.html',
    {
        'songs' : songs,
    },
    context_instance=RequestContext(request))