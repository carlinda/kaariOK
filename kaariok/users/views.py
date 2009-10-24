from django.contrib.auth import authenticate, login
from django.utils import simplejson
from django.http import HttpResponse

from django.contrib.auth.models import User

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