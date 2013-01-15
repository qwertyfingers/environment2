from django.db import models
from django.forms.models import ModelForm
import re
from django.core import validators
from django.core.exceptions import ValidationError
import os
import json
import random
import string
from django.db.models.fields.related import ForeignKey



#Manager for table wide key_sim_pair functions
class Key_sim_pair_manager(models.Manager):
    def get_random_order(self):
        random_order = self.objects.order_by('?')
        return random_order

class Key_sim_pair(models.Model):
    
    """
    A model that creates a key-sim pair with the following fields
        key : The unique identifier key for the simulation
        simulation : The path to a simulation file
        active - Boolean value that designates if the simulation is active(points towards a simulation) or not
        reward_key - The unique key used to identify when a user completes the task
    
    """
    #validator for keys
    key_regex = re.compile('[A-Z0-9]{30}')
    key_validator = validators.RegexValidator(key_regex)
    
    key = models.CharField(max_length=30, validators=[key_validator])
    simulation = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    reward_key = models.CharField(max_length=30, validators=[key_validator])
    
    
    def __unicode__(self):
        return self.key
    
    def valid_reward(self, reward_to_check):
        if (self.reward_key == reward_to_check):
            return True
        else:
            return False
        
       
        
    def be_rewarded(self, reward_to_check):
        if(self.active):
            if(self.valid_reward(reward_to_check)):
                return True
            else:
                return False
        else:
            return False

class Report_group(models.Model):
    key_sim_pair = models.ForeignKey(Key_sim_pair)
    def __unicode__(self):
        return self.key_sim_pair.key





        


#===============================================================================
#Models 
#
#===============================================================================

#Validators for files

#Checks if file exists
def validate_file(val_file):
    if (os.path.isfile(val_file) == False):
        raise ValidationError(u'File is not a valid file: %s' % val_file)

#Checks if file has valid .json extension   
def validate_json_extension(val_file):
    if (val_file.endswith('.json') or val_file.endswith('.JSON')) == False:
        raise ValidationError(u'File does not have valid json extension: %s' % val_file)


#Checks if file contains valid/readable json    
def validate_json_file(val_file):
    try:
        f = open(val_file, 'rt')
        try:
            json.load(f)
        except ValueError:
            raise ValidationError(u'File is not valid json: %s' % val_file)
            
        finally:
            f.close()
               
    except IOError:
        raise ValidationError(u'File could not be opened: %s' % val_file)
        
#Runs the file validators       
def validate_setup_file(val_file):
        validate_file(val_file)
        validate_json_extension(val_file)
        validate_json_file(val_file)           
    



class Sim_setup(models.Model):
    """
    A model that associates a json file with a sim setup databse entry for creating a simulation
    
    sim_file : the location of the file
    created_at: the date-time the database etnry was created
    updated_at: the date-time the databse entry was edited
    """
    sim_file = models.CharField(max_length=150, validators=[validate_setup_file])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return ("%s %s") %(self.id, self.sim_file)

      
class Agent_setup(models.Model):
    """
    A model that associates a json file with a agent setup databse entry for creating a simulation
    
    agent_file : the location of the file
    created_at: the date-time the database etnry was created
    updated_at: the date-time the databse entry was edited
    """
    agent_file = models.CharField(max_length=150, validators=[validate_setup_file])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return ("%s %s") %(self.id,self.agent_file)
    
     
class View_setup(models.Model):
    """
    A model that associates a json file with a view setup databse entry for creating a simulation
    
    view_file : the location of the file
    created_at: the date-time the database etnry was created
    updated_at: the date-time the databse entry was edited
    """
    view_file = models.CharField(max_length=150, validators=[validate_file, validate_json_extension, validate_json_file])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return ("%s %s") %(self.id,self.view_file)

                
class Simulation(models.Model):
    """
    A model that associates a sim_setup, agent_setup and 1 or more view_setup's to form a simulation
    """
    simulation_name = models.CharField(max_length=50)
    sim_setup = models.ForeignKey(Sim_setup)
    agent_setup = models.ForeignKey(Agent_setup)
    view_setup = models.ManyToManyField(View_setup)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return ("%s %s") %(self.id, self.simulation_name)
    

class Simulation_instance(models.Model):
    """
    A model that creates a particular instance of a simulation
    An instance is made up of the simulations agent and sim setups plus one view setup
    To run a live simulation instance, it also requires a pass_key_group associated with it
    """
    simulation = models.ForeignKey(Simulation)
    view_instance = models.ForeignKey(View_setup)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __unicode__(self):
        return ("%s, SIM:%s, VIEW:%s") %(self.id, self.simulation.simulation_name, self.view_instance.id)
    
class Experiment_group(models.Model):
    name=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __unicode__(self):
        return ("%s %s") %(self.id,self.name)
    
class Pass_key_group(models.Model):
    """
    A model that creates a a sim_key and a reward_key with the following fields
        sim_key : The unique identifier key for the simulation instance
        
        active - Boolean value that designates if the simulation is active(points towards a simulation) or not
        reward_key - The unique key used to identify when a user completes the task
    
    """
    #validator for keys
    key_regex = re.compile('[A-Z0-9]{30}')
    key_validator = validators.RegexValidator(key_regex)
    
    #database model
    simulation_instance = models.ForeignKey(Simulation_instance)
    user_key= models.CharField(max_length=30,default=lambda: create_key(), validators=[key_validator])
    reward_key = models.CharField(max_length=30,default=lambda: create_key(), validators=[key_validator])
    active_key = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    experiment_group=models.ForeignKey(Experiment_group, blank=True, null=True)

    def __unicode__(self):
        return ("%s SIM_INSTANCE:%s") %(self.id, self.simulation_instance.id)



class Report_group2(models.Model):
    pass_key_group = models.ForeignKey(Pass_key_group)
    def __unicode__(self):
        return ("%s PASS_KEY_GROUP: %s") %(self.id, self.pass_key_group.id)


    
def create_key(key_length=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(key_length))
    
class GUI_report_1(models.Model):
    
    COLOUR_CHOICES = [('NONE', 'none'),
                    ('BLACK', 'black'),
                    ('NAVY', 'navy'),
                    ('GREEN', 'green'),
                    ('TEAL', 'teal'),
                    ('MAROON', 'maroon'),
                    ('PURPLE', 'purple'),
                    ('OLIVE', 'olive'),
                    ('SILVER', 'silver'),
                    ('GRAY', 'gray'),
                    ('BLUE', 'blue'),
                    ('LIME', 'lime'),
                    ('AQUA', 'aqua'),
                    ('RED', 'red'),
                    ('FUCHSIA', 'fuchsia'),
                    ('YELLOW', 'yellow'),
                    ('WHITE', 'white'),
                    ]
    
    ACTIONS = [('Appeared', 'Appeared'),
             ('Disappeared', 'Disappeared'),
             ('Accelerated', 'Accelerated'),
             ('Decelerated', 'Decelerated'),
             ('Stopped', 'Stopped'),
             ('Started', 'Started'),
             ('Turned_Left', 'Turned_Left'),
             ('Turned_Right', 'Turned_Right'), ]   
    SIZE = [('Small', 'Small'),
          ('Medium', 'Medium'),
          ('Large', 'Large'), ]

    target_colour = models.CharField(max_length=50 , choices=COLOUR_CHOICES)#
    target_action = models.CharField(max_length=50, choices=ACTIONS) #
    target_size = models.CharField(max_length=50, choices=SIZE)#
    target_click_x = models.DecimalField(max_digits=20, decimal_places=10)#
    target_click_y = models.DecimalField(max_digits=20, decimal_places=10)#
    
    
    target_color_time=models.DecimalField(max_digits=20, decimal_places=0,blank=True, null=True)#
    target_color_frame=models.IntegerField(blank=True, null=True)#
    
    target_click_time=models.DecimalField(max_digits=20, decimal_places=0,blank=True, null=True)#
    target_click_frame=models.IntegerField(blank=True, null=True)#
    
    target_action_time=models.DecimalField(max_digits=20, decimal_places=0,blank=True, null=True)#
    target_action_frame=models.IntegerField(blank=True, null=True)#
    
    target_size_time=models.DecimalField(max_digits=20, decimal_places=0,blank=True, null=True)#
    target_size_frame=models.IntegerField(blank=True, null=True)#
    
    start_report_time=models.DecimalField(max_digits=20, decimal_places=0,blank=True, null=True)#
    start_report_frame=models.IntegerField(blank=True, null=True)#
    
    end_report_time=models.DecimalField(max_digits=20, decimal_places=0,blank=True, null=True)#
    end_report_frame=models.IntegerField(blank=True, null=True)#
    
    
    created = models.DateTimeField(auto_now_add=True)#
    #report_number=models.IntegerField(default=0)
    #sim_frame_submit=models.IntegerField(default=0)
    report_group = models.ForeignKey(Report_group2)#
    
    def __unicode__(self):
        return ("%s REPORT_GROUP: %s") %(self.id, self.report_group.id)
   
    
     
    
class GUIForm_1(ModelForm):
    class Meta:
        model = GUI_report_1
        exclude = ('created', 'report_group')         

    
class GUIForm_1b(ModelForm):
     class Meta:
        model = GUI_report_1
        exclude = ('created', 'report_group','target_color_time','target_color_frame',
                   'target_click_time','target_click_frame','target_action_time','target_action_frame',
                   'target_size_time','target_size_frame','start_report_time','start_report_frame',
                   'end_report_time','end_report_frame')      



        
 
