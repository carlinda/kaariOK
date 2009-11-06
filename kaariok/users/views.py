from django.contrib.auth import authenticate, login
from django.utils import simplejson
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template import RequestContext

from django.contrib.auth.models import User
from kaariok.users.models import Rating
from kaariok.songs.models import Song

from kaariok.songs.views import song_detail

def login_user(request, user_id):
    user = User.objects.get(id=user_id)
    login_user = authenticate(username=user.username, password=' ')
    success = False
    selected_id = user_id
    if login_user is not None:
        if user.is_active:
            login(request, login_user)
            success = True
            selected_id = login_user.id
            
    output = {
        'success' : success,
        'user_id' : selected_id,
    }
    return HttpResponse(simplejson.dumps(output))
    
def changeRating(request, song_id ,new_status, action):
    # Delete current rating
    try:
        rating = Rating.objects.get(user=request.user, song=song_id);
        rating.delete()
    except:
        pass
        
    if action == 'switch':
        new_rating = Rating(user=request.user, song=Song.objects.get(id=song_id), value=new_status)
        new_rating.save()
    
    return song_detail(request, song_id, True)
    
def new_user(request):
    name = request.GET.get('newUserName','').replace(" ", "")
    user = User.objects.create_user(name, '', '')
    user.save()
    
    users = User.objects.all().extra(select={'username_upper': 'upper(username)'}).order_by('username_upper')
    
    html = render_to_string('users/templatetags/user_selector.html', {'users':users, 'selected_user':user.id}, context_instance=RequestContext(request));
    
    output = {
        'html' : html,
    }
    return HttpResponse(simplejson.dumps(output))