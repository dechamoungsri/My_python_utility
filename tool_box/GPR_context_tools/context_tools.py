'''
Created on Jan 8, 2016

@author: decha
'''
from tool_box.util.utility import Utility
import re

class ContextTools(object):
    '''
    classdocs
    '''
    
    @staticmethod
    def get_all_context_names(filepath):
        
        pattern = re.compile(r""".+-\sname:\s(?P<name>.+begin.*)""", re.VERBOSE)
        
        for line in Utility.read_file_line_by_line(filepath):
            
            match = re.match(pattern, line)

            if match is None:
                continue
            
            print match.group('name')
        
        pass
    
    @staticmethod
    def get_context_list_of_a_phone(filepath, target_phone):
        yaml_file = Utility.yaml_load(filepath)
#         print yaml_file['preprocess']
        print 'Target phone : {}'.format(target_phone)
        for event in yaml_file['context_events']:
            name = event['name']
            args = event['value_getter']['event_feature']['args']
            type = None
            if len(args) > 1: 
                type = args[1]['args'][0]
            
#             print type
            
            if type == 'entity':
                d = "{}".format(args[0])
                d = d.split(',')
                for ph in d:
                    if '\'{}\''.format(target_phone) in ph:
                        ph = '{}'.format(ph)
                        ph = ph.split('[')[-1].split(']')[0]
#                         print ph
#                         if int(ph) == 1:
                        if 'begin' in name:
                            if ph == '{}'.format(1):
                                print name, ph
                        
#                 print d
            
#             break

#         Utility.print_yaml_formatted(yaml_file['context_events'][2])
#         Utility.print_yaml_formatted(yaml_file['context_events'][2]['name'])
#         Utility.print_yaml_formatted(yaml_file['context_events'][2]['value_getter']['event_feature']['args'][0]['uua'])
        pass
    
    def __init__(self, params):
        '''
        Constructor
        '''
        