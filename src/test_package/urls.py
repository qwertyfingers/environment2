from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('test_package.views',
                       url(r'^test1a/$', 'simple_date_time', name="simple_date_time"), #Look for the root webpage
                       url(r'^test1b/$', 'simple_404', name="simple_404"), # Shows the 404 page (note, when DEBUG=true, then this will show error page, without stack trace) 
                       url(r'^test2a/$', 'template_simple', name="template_simple"),
                       url(r'^test2b/$', 'template_variables',{'foo': 'nar'}, name="template_variables_nar"), #Used to pass no variables - really we are passing a variable, but the tempalte looks for 'bar'
                       url(r'^test2c/$', 'template_variables',{'foo': 'bar'}, name="template_variables_bar",), #Pass vairable in, bar
                       url(r'^test3a/$', 'post_simple', name="post_simple"), #redirects on post
                       url(r'^thankyou/$','post_thankyou', name='post_thankyou'), #  a landing page for post data
                       url(r'^test3b/$', 'post_db_1', name='post_db_1'),#redirects on valid post data, otherwise gives error heading
                       url(r'^test4a/$', 'static_css', name='static_css'), #demo static files -  style file
                       url(r'^boiler_1/$', 'boiler_index', name='boiler_index'),
                       url(r'^boiler_2/$', 'boiler_extend_frame', name='boiler_extend_frame'),
                       url(r'^test_links/$', 'test_links', name='test_links'),
                       )
