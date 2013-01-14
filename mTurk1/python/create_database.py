import sys,os
PROJECT=(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','..')))
PROJECT2=(os.path.join(os.path.dirname( __file__ ),'..','lib/python2.7'))
sys.path=[PROJECT,PROJECT2]+sys.path
import logging
import pdb
from mTurk1.python.database_functions import generate_experiment





def create_experiment_database():
    from mTurk1.simulations.sim_test_1.configExp import ExperimentSettings
    #TRY: get settings from ExperimentSettings module
    try:
        experiment_settings=ExperimentSettings
    except:
        logger.error("create_database: Could not initialise ExperimentSettings config file")
        return 1
    
    #TRY: set up the varaibles for creating an experiment
    try: 
        sim_name=experiment_settings.sim_name
        exp_name=experiment_settings.exp_name
        agent_list=experiment_settings.agent_list
        sim_list=experiment_settings.sim_list
        view_list=experiment_settings.view_list
            
    except:
        logger.error("create_database: Could not create sim, agent and view lists ")
        return 1
    
    try:   
        valid_lists=check_lists(sim_list,agent_list,view_list)
        if all(list is True for list in valid_lists):
            logger.debug("create_database: All lists valid")
        else:
            logger.debug("create_databse: INVALID lists (labelled False). Sim: %s ; Agent: %s; View: %s" %(valid_lists[0],valid_lists[1], valid_lists[2]))
    except:
        logger.critical("create_database: Could not run valid_lists")
        return 1
        
    try:    
        status=generate_experiment(sim_list,agent_list,view_list,sim_name,exp_name)
        if status==1:
            raise Exception
        
    except:
        logger.error("create_database: Could not run generate_experiment")
        return 1
    
    return 0


def check_lists(sim_list,agent_list,view_list):
    
    valid_sim_list=False
    valid_agent_list=False
    valid_view_list=False
    
    if len(sim_list)==1:
        valid_sim_list=True
    elif len(sim_list)<1:
        logger.debug("sim_list<1")
    elif len(sim_list>1):
        logger.debug("sim_list>1")
      
    if len(agent_list)==1:  
        valid_agent_list=True
    elif len(agent_list)<1:
        logger.debug("agent_list<1")
    elif len(agent_list)>1:
        logger.debug("agent_list>1")
    
    if len(view_list)<1:
        valid_view_list=False
    elif len(view_list)>=1:
        valid_view_list=True
    
    return[valid_sim_list,valid_agent_list,valid_view_list]    





#===============================================================================
#Main
#===============================================================================      
if __name__ == "__main__":
    logger = logging.getLogger('django')
    logger.info("Running: create_database")
    result=create_experiment_database()
    logger.info("Finished: create_database, successful: %s" % result)
    
    
    
