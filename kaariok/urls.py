from django.conf.urls.defaults import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# For testing only
from django.shortcuts import render_to_response
def test_base(request):
    return render_to_response('test.html')
# End testing

urlpatterns = patterns('',
    # Example:
    # (r'^kaariok/', include('kaariok.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    # Serving media for 
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
    	{'document_root': settings.MEDIA_ROOT}),
    
    # For testing only
    (r'^basetest/', test_base),
)
