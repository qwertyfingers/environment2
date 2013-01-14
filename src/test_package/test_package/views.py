import datetime
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse

from test_package.models import Test_db_1_form











# returns html of current_date_time. Does not use a template
def simple_date_time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


#Raises the Http404 responses i.e. page not found
def simple_404(request):    
    raise Http404

#Tests that a template can be found and displayed
def template_simple(request):
    return render(request, 'test_package/template_simple.html',)

#Tests passing a varaible from url dispatcher to the view
def template_variables(request, foo):
    if foo == 'bar':
        return render(request, 'test_package/template_variables.html', {'test_var':foo})   
    else:
        return render(request, 'test_package/template_variables.html',)
    
#When the user first comes to page, it sends them to render page, if they post data sends them to thankyou
def post_simple(request): 
    if request.method=='POST':
        return HttpResponseRedirect(reverse('t_p:post_thankyou'))  
    return render(request, 'test_package/post_simple.html',)

def post_thankyou(request):
    return render(request, 'test_package/post_thankyou.html',)


def post_db_1(request):
    if request.method=='POST':
        form=Test_db_1_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('t_p:post_thankyou'))
        else:
            error_message="Form is not valid"
            return render(request, 'test_package/post_database_1.html',{"error_message":error_message})
    return render(request, 'test_package/post_database_1.html',)
          
def static_css(request):
    return render(request, 'test_package/static_css.html')

def boiler_index(request):
    return render(request, 'test_package/boiler_index.html')

def boiler_extend_frame(request):
    return render(request, 'test_package/boiler_extend_frame.html')

def test_links(request):
    return render(request, 'test_package/test_links.html')