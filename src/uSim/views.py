# Create your views here.
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson


def home(request):
    setup_files=[]
    setup_files.append('H:/AptanaWorkspace/environment1/src/mTurk1/JSONandJS/sim_test_1/sim_settings_test_0.1.json')
    setup_files.append('H:/AptanaWorkspace/environment1/src/mTurk1/JSONandJS/sim_test_1/agent_settings_test_0.1.json')
    setup_files.append('H:/AptanaWorkspace/environment1/src/mTurk1/JSONandJS/sim_test_1/view_settings_test_0.1.json')
    json_dump=[]
    for setup_file in setup_files:
        f=open(setup_file,'rt')
        json_data=simplejson.load(f)                  
        json_dump.append(simplejson.dumps(json_data))                  
        f.close()
    json_sim_settings=json_dump[0]
    json_agent_settings=json_dump[1]
    json_view_settings=json_dump[2]
    
    return render_to_response('uSim/simulation_frame.html',{"json_sim_settings":json_sim_settings,"json_agent_settings":json_agent_settings,"json_view_settings":json_view_settings},context_instance=RequestContext(request),)
