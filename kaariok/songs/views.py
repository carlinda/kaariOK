from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse
from django.db.models import Q

from kaariok.songs.models import Song, Language
from kaariok.users.models import Rating

def convertJavascriptBoolean(bool):
    if bool == u'true' or bool == 'true':
        return True
    return False

def song_search(request):
    # Get params
    approved_param = ""
    search_string = ""
    ratings = {}
    try:
        approved_param = int(request.GET.get('approved',''));
    except:
        pass
    try:
        search_string = request.GET.get('search_string','')
    except:
        pass
    try:
        ratings['unrated'] = convertJavascriptBoolean(request.GET.get('unrated', False))
        ratings['hate'] = convertJavascriptBoolean(request.GET.get('hate', False))
        ratings['meh'] = convertJavascriptBoolean(request.GET.get('meh', False))
        ratings['known'] = convertJavascriptBoolean(request.GET.get('known', False))
        ratings['love'] = convertJavascriptBoolean(request.GET.get('love', False))
    except:
        pass
            
    songs = Song.objects.all()
    
    # Apply filters
    # Approved filter
    if approved_param is not '' and approved_param is not 3:        
        songs = songs.filter(approved=approved_param);
    # Search string filter
    if search_string is not '':
        songs = songs.filter(Q(name__icontains=search_string) | Q(artist__name__icontains=search_string))
    # Ratings filters
    unrated_Q = Q()
    hate_Q    = Q()
    meh_Q     = Q()
    known_Q   = Q()
    love_Q    = Q()
    if ratings['unrated']:
        user_ratings = Rating.objects.filter(user=request.user)
        rated_songs = [rat.song.id for rat in user_ratings]
        if rated_songs == []:
            rated_songs = [-1, ]
        unrated_Q = ~Q(id__in=rated_songs)
    if ratings['hate']:
        user_ratings = Rating.objects.filter(user=request.user, value='hate')
        hated_songs = [rat.song.id for rat in user_ratings]
        if hated_songs == []:
            hated_songs = [-1, ]
        hate_Q = Q(id__in=hated_songs)
    if ratings['meh']:
        user_ratings = Rating.objects.filter(user=request.user, value='meh')
        mehed_songs = [rat.song.id for rat in user_ratings]
        if mehed_songs == []:
            mehed_songs = [-1, ]
        meh_Q = Q(id__in=mehed_songs)
    if ratings['known']:
        user_ratings = Rating.objects.filter(user=request.user, value='known')
        known_songs = [rat.song.id for rat in user_ratings]
        if known_songs == []:
            known_songs = [-1, ]
        known_Q = Q(id__in=known_songs)
    if ratings['love']:
        user_ratings = Rating.objects.filter(user=request.user, value='love')
        loved_songs = [rat.song.id for rat in user_ratings]
        if loved_songs == []:
            loved_songs = [-1, ]
        love_Q = Q(id__in=loved_songs)
    
    songs = songs.filter(unrated_Q | hate_Q | meh_Q | known_Q | love_Q)
    
    songs = songs.extra(select={'name_upper' : 'upper(songs_song.name)'}).order_by('name_upper')
    
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
        
def song_detail(request, song_id, innerCall=False):
    song = Song.objects.get(id=song_id)
    try:
        rating = Rating.objects.get(user=request.user, song=song_id)
    except:
        rating='unknown'

    value = ''
    if rating is not 'unknown':
        value = rating.value.lower()
    else:
        value = rating

    song_detail_html = render_to_string('songs/partial/song_detail.html',
        {   
            'song' : song,
            'rating' : value,
        },
         context_instance=RequestContext(request)
    )

    if request.is_ajax() or innerCall:
        output = {
            'html' : song_detail_html,
        }
        return HttpResponse(simplejson.dumps(output))
    else:
        pass
        # return render_to_response('songs/partial/song_detail.html',
        # {   
        #     'song' : song,
        #     'rating' : value,
        # },
        # context_instance=RequestContext(request))

def song_edit(request, song_id):
    song = Song.objects.get(id=song_id)
    try:
        rating = Rating.objects.get(user=request.user, song=song_id)
    except:
        rating='unknown'

    value = ''
    if rating is not 'unknown':
        value = rating.value.lower()
    else:
        value = rating
        
    languages = Language.objects.all()

    song_detail_html = render_to_string('songs/partial/song_edit.html',
        {   
            'song' : song,
            'rating' : value,
            'approval_choices':Song.APPROVAL_CHOICES,
            'languages' : languages,
        },
         context_instance=RequestContext(request)
    )

    if request.is_ajax() or innerCall:
        output = {
            'html' : song_detail_html,
        }
        return HttpResponse(simplejson.dumps(output))
    else:
        pass
        # return render_to_response('songs/partial/song_detail.html',
        # {   
        #     'song' : song,
        #     'rating' : value,
        # },
        # context_instance=RequestContext(request))
        
def song_save_edit(request,song_id):
    # Get params
    name_param = ""
    track_param = ""
    language_param = ""
    filename_param = ""
    approved_param = ""
    try:
        name_param = request.GET.get('name','')
    except:
        pass
    try:
        track_param = request.GET.get('track','')
        try:
            int(track_param)
        except:
            track_param = u''
    except:
        pass
    try:
        language_param = request.GET.get('language','')
    except:
        pass
    try:
        filename_param = request.GET.get('filename','')
    except:
        pass
    try:
        approved_param = int(request.GET.get('approved',''));
    except:
        pass

    # Get song
    song = Song.objects.get(id=song_id)
    
    # Update song details
    song.name = name_param;
    if track_param is not u'':
        song.track = track_param
    else:
        song.track = None
    song.language = Language.objects.get(id=language_param)
    song.filename = filename_param
    song.approved = approved_param
    
    song.save()    

    return song_detail(request, song_id)