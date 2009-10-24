from django.utils import simplejson
from django.http import HttpResponse



def login_user(request, user_id):
    
    output = {
        'success' : False,
    }
    return HttpResponse(simplejson.dumps(output))