import logging
import sys
from mTurk1.models import Report_group2, GUI_report_1, GUIForm_1, GUIForm_1b,\
    validate_setup_file
from django.http import QueryDict
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.template.context import RequestContext
import pdb
from django.utils import simplejson






logger = logging.getLogger('django')

def process_reports_from_post(POST,db_key_sim,url_key):
    """
    Processes the POST request from simulation. 
    returns: 
        0 : valid reports submitted
        1 : No valid reports submitted
        100: Unknown error 
    """
    #Extract individual reports from POST
    unvalidated_reports=[]
    for key, value in POST.iteritems():
        logger.debug('%s %s' %(key,value))
        if 'report_' in key:
            unvalidated_reports.append(value)
    logger.debug("OK: extracted unvalidated reports from POST")
    
    
    #Create and save a report group for the sim key  
    report_group=Report_group2(pass_key_group=db_key_sim)
    report_group.save()    
    submitted_valid_form=False
    logger.debug("OK: Saved a new report_group")
    valid_counter=0
    num_reports=len(unvalidated_reports)
    #For each report, create a QueryDict and validate this against the GUIForm
    for report in unvalidated_reports:
        logger.debug(report)
        report_query_dict=QueryDict(report)
        form_instance = GUI_report_1(report_group=report_group)
        form=GUIForm_1(report_query_dict,instance=form_instance)   
        if form.is_valid():
            logger.debug("OK: Validated Form INCLUDING timestamps")
            form.save()
            submitted_valid_form=True
            valid_counter=valid_counter+1
        else:
            logger.debug("Unvalidated Form INCLUDING timestamps")
            form=GUIForm_1b(report_query_dict,instance=form_instance)
            if form.is_valid():
                logger.debug(" OK:Validated Form EXCLUDING timestamps")
                form.save()
                submitted_valid_form=True
                valid_counter=valid_counter+1
            else:
                logger.debug("Unvalidated Form")
                 
                  
    if(submitted_valid_form):
        logger.debug("Active and valid form")
        return [0,"OK:Valid reports submitted"]
    elif(not submitted_valid_form):
        return [1,"FAILED: No valid forms submitted"]
    else:
        return [100,"FAILED: Something went wrong"]
                   

def validate_setup_files(sim_file,agent_file,view_file):
    validate_setup_file(sim_file)
    validate_setup_file(agent_file)
    validate_setup_file(view_file)
    
    
def dump_to_json(sim_file,agent_file,view_file):
    #dump json into varaibles that are passed to the simulation as javascript varaibles
    json_dump=[]
    try:
        for setup_file in [sim_file,agent_file,view_file]:
            try:
                f=open(setup_file,'rt')
                json_data=simplejson.load(f)                  
                json_dump.append(simplejson.dumps(json_data))
                logger.debug("OK: dumped json data for %s" %setup_file)
            finally:
                f.close()
        return json_dump
    except Exception:
        raise