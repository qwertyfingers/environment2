

class ConfigSettingError(Exception):
    """ This is raised when a config setting can not be found"""
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return repr(self.val)
    
