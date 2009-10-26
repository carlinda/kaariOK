from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Project view imports
from kaariok.users.views import login_user
from kaariok.songs.views import song_search

# For testing only
from django.shortcuts import render_to_response
from django.template import RequestContext
def test_base(request):
    return render_to_response('test.html',{},context_instance=RequestContext(request))
# End testing

urlpatterns = patterns('',
    # Example:
    # (r'^kaariok/', include('kaariok.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$',  login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/login/(?P<user_id>.*)/$', login_user),
    
    # Song Urls
    (r'^song/search/$', song_search),
    
    # Serving media for 
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root': settings.MEDIA_ROOT}),
    
    # For testing only
    (r'^basetest/', test_base),
)
