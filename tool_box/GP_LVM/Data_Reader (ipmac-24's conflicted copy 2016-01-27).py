'''
Created on Jan 25, 2016

@author: decha
'''

import sys
sys.path.append('../../')

from tool_box.util.utility import Utility

import numpy as np

class DataReader(object):
    '''
    classdocs
    '''

    @staticmethod
    def gen_syllable_tag(syllable_label_path, tone, start_set, end_set, tag):
        # Format a_tscsda01_3 
#         'tscsd_manual'
        lf0_tags = []
        
        for set in Utility.char_range(start_set, end_set):
            path = '{}/{}'.format(syllable_label_path, set)
            
            count = Utility.count_valid_file(path)
            
            for i in range(1, count+1):  
                
                filepath = '{}/tscsd_stust_{}{}.stresslab'.format(path,set,Utility.fill_zero(i, 2))
                syllable_count = 0
                for line in Utility.read_file_line_by_line(filepath):
                    syllable_count+=1
                    
                    if tone == '01234':
                        lf0_tags.append('{}_{}_{}{}_{}'.format(set,tag, set ,Utility.fill_zero(i, 2),syllable_count))
                    else :
                        if line[0] == tone:
                            lf0_tags.append('{}_{}_{}{}_{}'.format(set,tag, set ,Utility.fill_zero(i, 2),syllable_count))
                    
        return lf0_tags
        
        pass

    @staticmethod
    def filter_data(data, area):
        
        index_list = []
        
        x = data
        x = x[x[:,0]>area['x_low']]
        x = x[x[:,0]<area['x_up']]
        x = x[x[:,1]>area['y_low']]
        x = x[x[:,1]<area['y_up']]
        
        print x
        
        for dat in x:
            index_list.append(np.where(data==dat)[0][0])
        
        return index_list
        
        pass

    @staticmethod
    # Params
    #    filepath    : String
    #    area        : Rectangle   
    def find_data_point_from_coordinate(filepath, input_sen_path, labels, syllable_data_path, area, tone):
        
        # Read data file
        data_point = Utility.load_obj(filepath)
#         print data_point
        
        # Get input sensitivity
        input_sen_obj = Utility.load_obj(input_sen_path)
        input_sensitivety = Utility.get_input_sensitivity(input_sen_obj, 3)
#         print input_sensitivety

        x_coordinate = data_point[:,[input_sensitivety[0],input_sensitivety[1]]]
#         print x_coordinate
        x_cor = np.array(x_coordinate)
        index = DataReader.filter_data(x_cor, area)
        
        print index
        
        lab = Utility.load_obj(labels)
        print len(lab)
        print lab[index]
        
        syllable_tag = DataReader.gen_syllable_tag(syllable_data_path, tone, 'a', 'h', 'tscsd_manual')
        
        print len(syllable_tag)
        
        syllable_tag = np.array(syllable_tag)
        
        print syllable_tag[index]
        
        lab_indexed = lab[index]
        syllable_tag_indexed = syllable_tag[index]
        
        print syllable_tag_indexed[lab_indexed=='Tone 2']
        
        # Return
        
        pass

    def __init__(self, params):
        '''
        Constructor
        '''
        