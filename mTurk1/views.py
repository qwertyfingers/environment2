import os
import logging
from django.shortcuts import render
from mTurk1.models import Experiment_group, Pass_key_group
from mTurk1.python.custom_exceptions import ConfigSettingError
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseRedirect
import pdb
from mTurk1.python.view_functions import validate_setup_files, dump_to_json,\
    process_reports_from_post
from django.core.urlresolvers import reverse

SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
logger = logging.getLogger('django')
EXPERIMENT_NAME='Experiment_0.1'


#This view collects all the keys associated with the current experiemnt
#Returns either an  error page, or a page of keys associated with the experiment
def display_keys(request):
    logger.info("view - display key")
    try:    
        try:
            experiment=Experiment_group.objects.get(name=EXPERIMENT_NAME)
            logger.debug("OK: Experiment_group found : name= %s" %EXPERIMENT_NAME)
        except NameError as e:
            logger.exception("A config setting went wrong")
            raise ConfigSettingError(e)
        except ObjectDoesNotExist as e:
            logger.exception("A config setting went wrong")
            raise ConfigSettingError(e)
    except ConfigSettingError as e:
        error_message="There is no valid experiment at this time."
        return render(request,'mTurk1/error_page.html',{'error_message':error_message})

    #If an experiment is found, then continue

    #Check for active keys in the experiment
    active_keys_set=experiment.pass_key_group_set.filter(active_key=True)
    active_keys=[]
    for key in active_keys_set:
        active_keys.append(key.user_key)
        
    #Check for inactive keys
    inactive_keys_set=experiment.pass_key_group_set.filter(active_key=False)
    inactive_keys=[]
    for key in inactive_keys_set:
        inactive_keys.append(key.user_key)
    
    if len(active_keys)>=1 or len(inactive_keys)>=1:
        
        return render(request,'mTurk1/display_keys.html',{'active_keys':active_keys, 'inactive_keys':inactive_keys})
    else:
        error_message="No keys for this experiemnt could be found"
        return render(request, 'mTurk1/error_page.html', {'error_message':error_message})





def simulation(request, key):
    
    #Get the key from the url
    #Check key from url against database
        #Check existence of key
        #Check key is active
    #Check if POST data
        #Process POST data
    #If not POSt, then direct user to simulation
    
    
    
    #Check if key exists
    try:
        current_pkg=Pass_key_group.objects.get(user_key=key)
    except:
        logger.debug("Key does not exist")
        logger.exception("Key does not exist")
        raise Http404
        
    #Check if key is active
    if current_pkg.active_key==False:
        logger.debug("Key is not active")
        logger.exception("Key is not active")
        raise Http404
    
    #If there is POST data present, check to see if it is a valid report POST
    if request.method=='POST':
        process_reports=process_reports_from_post(request.POST,current_pkg,key)
        logger.info(process_reports[0])
        #If process reports returned successfully
        if process_reports[0]==0:
            reward_key=current_pkg.reward_key
            #return render(request,'mTurk1/thankyou_page.html',{'reward_key':reward_key, 'url_key': key})
            return HttpResponseRedirect(reverse('mturk1:thankyou_post', args=[key, reward_key]))
        else:
            error_message="The information provided was not valid"
            return render(request,'mTurk1/error_page.html',{'error_message': error_message})  
    
    #If there was no post data, then proceed to loading the simulation
    #Get the setup files 
    try:
        sim_instance=current_pkg.simulation_instance
        simulation=sim_instance.simulation
        sim_setup=simulation.sim_setup
        agent_setup=simulation.agent_setup
        view_setup=sim_instance.view_instance
        logger.debug("OK: Found _setup database entries")
        
        validate_setup_files(sim_setup.sim_file,agent_setup.agent_file,view_setup.view_file)
        logger.debug("OK: Ran validation checks on _setup files") 
             
        json_dump=dump_to_json(sim_setup.sim_file,agent_setup.agent_file,view_setup.view_file)
        logger.debug("OK: dumped all json files")
            
        sim_settings=json_dump[0]
        agent_settings=json_dump[1]
        view_settings=json_dump[2]
        logger.debug("OK: assigned json_dump to variables")
    except:
        logger.debug("Could not load simulation")
        logger.exception("Could not load simulation")
        raise Http404
    
    return render(request,'uSim/simulation_testM1.html',{'json_sim_settings':sim_settings,'json_view_settings':view_settings,'json_agent_settings':agent_settings})   
    #return render(request, 'mTurk1/error_page.html', {'error_message':error_message})
    

def thankyou_post(request,key=None,reward_key=None): 
    
    return render(request, 'mTurk1/thankyou_page.html',{"url_key":key, "reward_key": reward_key}) 
    
    

  