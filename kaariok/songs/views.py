from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import Q

from kaariok.songs.models import Song

def song_search(request):
    # Get params
    approved_param = ""
    search_string = ""
    try:
        approved_param = int(request.GET.get('approved',''));
    except:
        pass
    try:
        search_string = request.GET.get('search_string','')
    except:
        pass
        
    songs = Song.objects.all()#.extra(select={'name_upper' : 'upper(name)'}).order_by('name_upper')
    
    # Apply filters
    # Approved filter
    if approved_param is not '' and approved_param is not 3:        
        songs = songs.filter(approved=approved_param);
    # Search string filter
    if search_string is not '':
        songs = songs.filter(Q(name__icontains=search_string) | Q(artist__name__icontains=search_string))
        
        
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