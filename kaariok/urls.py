from django.conf.urls.defaults import *
from django.contrib.auth.views import login, logout
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# Project view imports
from kaariok.users.views import login_user, changeRating, new_user
from kaariok.songs.views import song_search, song_detail, song_edit, song_save_edit
from kaariok.playlists.views import user_playlist, add_song_to_playlist, remove_item_from_playlist, move_item_up, move_item_down, user_playlist_page, master_playlist, master_add_playlist, add_item_to_master_playlist, move_item_up_on_master_list, move_item_down_on_master_list, remove_item_from_master_playlist, playlists_list_reload

from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    # Example:
    # (r'^kaariok/', include('kaariok.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Generic index view
    (r'^$', direct_to_template, {'template': 'main.html'}),

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
    (r'^playlist/user/$', user_playlist_page),
    (r'^playlist/user/(?P<user_id>.*)/$', user_playlist),
    (r'^playlist/add/(?P<song_id>.*)/$', add_song_to_playlist),
    (r'^playlist/remove/(?P<item_id>.*)/$', remove_item_from_playlist),
    (r'^playlist/move/(?P<item_id>.*)/up/$', move_item_up),
    (r'^playlist/move/(?P<item_id>.*)/down/$', move_item_down),
    (r'^playlist/master_add/(?P<user_id>.*)/$', master_add_playlist),
    (r'^playlist/master/$', master_playlist),
    (r'^playlist/master/add/(?P<item_id>.*)/$', add_item_to_master_playlist),
    (r'^playlist/master/move/(?P<item_id>.*)/up/$', move_item_up_on_master_list),
    (r'^playlist/master/move/(?P<item_id>.*)/down/$', move_item_down_on_master_list),
    (r'^playlist/master/remove/(?P<item_id>.*)/$', remove_item_from_master_playlist),
    (r'^playlist/list/reload/$', playlists_list_reload),
    
    
    
    # Serving media for 
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root': settings.MEDIA_ROOT}),
)
