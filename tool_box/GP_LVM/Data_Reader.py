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
    def find_data_point(model, name_index, data_object, coordinate, label, outpath):
        
        data = m.data

        pass

    @staticmethod
    def gen_syllable_tag(label_path, tone):
        # Format a_tscsda01_3 
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
    def find_data_point_from_coordinate(filepath, input_sen_path, labels, syllable_data_tag, area):
        
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
        
        syllable_tag = Utility.load_obj(syllable_data_tag)
        print len(syllable_tag)
        print syllable_tag
        
        
        # Return
        
        pass

    def __init__(self, params):
        '''
        Constructor
        '''
        