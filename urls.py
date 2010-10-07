from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
                           (r'^$', 'minesweeper.views.index'),
                           (r'^clear$', 'minesweeper.views.clear'),
                           (r'^flag$', 'minesweeper.views.flag'),
                           (r'^reset$', 'minesweeper.views.reset'),
                           (r'^high_scores$', 'minesweeper.views.view_high_scores'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
