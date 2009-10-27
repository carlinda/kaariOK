from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from kaariok.songs.models import Song

def song_search(request):
    songs = Song.objects.all().extra(select={'name_upper' : 'upper(name)'}).order_by('name_upper')
    song_list_html = render_to_string('songs/partial/song_list.html',
        {'songs' : songs},
         context_instance=RequestContext(request)
    )
    
    if request.is_ajax():
        output = {
            'html' : song_list_html,
        }
        return HttpResponse(simplejson.dumps(output))
    else:
        return render_to_response('songs/search.html',
        {
            'song_list_html' : song_list_html,
        },
        context_instance=RequestContext(request))