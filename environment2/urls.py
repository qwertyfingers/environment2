from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^tests/test_package/',include('test_package.urls',namespace="t_p")), # look for test pages
                       url(r'^sims/tasks/',include('mTurk1.urls',namespace="mturk1")),
                       url(r'^admin/', include(admin.site.urls)),
                       #url(r'^(.+)$','mTurk1.views.tasks_no_match'), #look for everything else......... (needed?)
  
)
