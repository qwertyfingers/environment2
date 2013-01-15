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
    logger.info("ATTEMPT: Extract unvalidated reports from POST")
    for key, value in POST.iteritems():
        logger.debug('%s %s' %(key,value))
        if 'report_' in key:
            unvalidated_reports.append(value)
    num_reports=len(unvalidated_reports)
    logger.info("Extracted %s unvalidated reports from POST" %num_reports)
    
    
    #Create and save a report group for the sim key  
    logger.info("ATTEMPT: Create and save a report group")
    logger.debug("Create report group")
    report_group=Report_group2(pass_key_group=db_key_sim)
    logger.debug("Save report group")
    report_group.save()    
    submitted_valid_form=False
    logger.info("OK: Saved a new report_group")
    valid_counter=0
    
    #For each report, create a QueryDict and validate this against the GUIForm
    logger.info("Start processing unvalidated reports")
    for report in unvalidated_reports:
        logger.debug("Report in unvalidated reports: %s" %report)
        report_query_dict=QueryDict(report)
        logger.debug("Create form instance")
        form_instance = GUI_report_1(report_group=report_group)
        form=GUIForm_1(report_query_dict,instance=form_instance)
        logger.debug("Form Data: %s" %form) 
        logger.info("ATTEMPT: Validate Form data with timestamaps")  
        if form.is_valid():
            logger.info("OK: Validated Form data with timestamps")
            form.save()
            submitted_valid_form=True
            valid_counter=valid_counter+1
        else:
            form_errors=form.errors
            logger.info("FAILED: Validating Form with timestamps")
            logger.debug("form_errors: %s" %form_errors)
            form=GUIForm_1b(report_query_dict,instance=form_instance)
            logger.info("ATTEMPT: Validate Form data without timestamps")
            if form.is_valid():
                logger.info(" OK: Validate Form without timestamps")
                form.save()
                submitted_valid_form=True
                valid_counter=valid_counter+1
            else:
                logger.info("FAILED: Validate Form without timestamps")
                logger.info("FAILED: Validate Form data")
                
                  
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