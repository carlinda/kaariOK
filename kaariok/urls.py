from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Project view imports
from kaariok.users.views import login_user, changeRating, new_user
from kaariok.songs.views import song_search, song_detail, song_edit, song_save_edit
from kaariok.playlists.views import user_playlist

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
    (r'^accounts/user/new/$', new_user),
    
    # Song Urls
    (r'^song/search/$', song_search),
    (r'^song/(?P<song_id>.*)/edit/save/$', song_save_edit),
    (r'^song/(?P<song_id>.*)/edit/$', song_edit),
    (r'^song/(?P<song_id>.*)/$', song_detail),
    
    # Rating
    (r'^rating/(?P<song_id>.*)/(?P<new_status>.*)/(?P<action>.*)/$', changeRating),
    
    # Playlists
    (r'^playlist/user/(?P<user_id>.*)/$', user_playlist),
    
    # Serving media for 
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root': settings.MEDIA_ROOT}),
    
    # For testing only
    (r'^basetest/', test_base),
)
