from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^flightlog/', include('flightlog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^flight/(?P<flight_id>\d+)$', 'main.views.flight'),
    (r'^flight/(?P<flight_id>\d+)/circles$', 'main.views.circles'),
    (r'^flight/(?P<flight_id>\d+)/polylines$', 'main.views.polylines'),
    (r'^flight/(?P<flight_id>\d+)/stats$', 'main.views.stats'),
    (r'', include('gmapi.urls.media')),
)
