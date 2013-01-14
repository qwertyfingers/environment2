from django.test import TestCase
import unittest
from mTurk1.models import Key_sim_pair, Agent_setup, Sim_setup, View_setup
from django.core.exceptions import ValidationError


#Tests key_sim_pair functions
class Key_sim_pair_TestCase(unittest.TestCase):
    def setUp(self):
        self.pair1=Key_sim_pair.objects.create(key="A1B2",
    simulation="sim_folder\exampleB.sim",active=False,reward_key="Y3Z4")
                        
        self.pair2=Key_sim_pair.objects.create(key="12345ABCDE",
    simulation="sim_folder\exampleA.sim",active=True,reward_key="AB")
        
    def test_valid_reward(self):
        self.assertEqual(self.pair1.valid_reward("AB"), False)
        self.assertEqual(self.pair2.valid_reward("AB"), True)
    
    def test_be_rewarded(self):
        self.assertEqual(self.pair1.be_rewarded("Y3Z4"), False)
        self.assertEqual(self.pair2.be_rewarded("Y3Z4"), False)
        self.assertEqual(self.pair2.be_rewarded("AB"), True)
        
        
        
#Test setup files

class Setup_file_TestCase(unittest.TestCase):
    def setUp(self):
        self.pass_file=r"H:\AptanaWorkspace\environment1\src\mTurk1\simulations\test_files\agent_PASS.json"
        self.fail_file_extension=r"H:\AptanaWorkspace\environment1\src\mTurk1\simulations\test_files\view_INVALIDEXTENSION.js"
        self.fail_file_json=r"H:\AptanaWorkspace\environment1\src\mTurk1\simulations\test_files\agent_INVALIDJSON.json"
        self.fail_file_exists=r"H:\AptanaWorkspace\environment1\src\mTurk1\simulations\test_files\agent123.json"
    
    def test_pass(self):
        self.test_pass_agent=Agent_setup(agent_file=self.pass_file).full_clean()
        self.assertEqual(self.test_pass_agent, None)
        
        self.test_pass_sim=Sim_setup(sim_file=self.pass_file).full_clean()
        self.assertEqual(self.test_pass_sim, None)
        
        self.test_pass_view=View_setup(view_file=self.pass_file).full_clean()
        self.assertEqual(self.test_pass_view, None)
        
    def test_extension(self): #this doesnt work at the moment
        self.agent_fail=Agent_setup(agent_file=self.fail_file_extension)
        self.assertRaises(ValidationError)
        
        self.sim_fail=Sim_setup(sim_file=self.fail_file_extension)
        self.assertRaises(ValidationError)
        
        self.view_fail=View_setup(view_file=self.fail_file_extension)
        self.assertRaises(ValidationError)