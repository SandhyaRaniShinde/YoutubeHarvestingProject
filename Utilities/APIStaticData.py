'''API static module'''
#import os is an module,provides way to interact with operating system
import os

#EnvironmentReader is an Class for reading variable
class EnvironmentReader:
    #Define an empty constructor, init is contructor method and self is ref can named
    def __init__(self):
        #Pass is an statement used with init method
        pass
    #Defines method named get_specific_variable that takes a variable_name as a parameter. 
    def get_specific_variable(self, variable_name):
        #os.environ.get(variable_name)method used to retrieve the value from specified environment variable.
        return os.environ.get(variable_name)