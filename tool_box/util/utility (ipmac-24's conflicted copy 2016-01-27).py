'''
Created on Aug 16, 2015

@author: decha
'''

import pickle
import os
import matplotlib
import matplotlib.pyplot as plt
import yaml
import yaml_handler
import json
import shutil
from collections import OrderedDict
import logging
import commands
import numpy as np

class Utility(object):
    
    @staticmethod
    def char_range(c1, c2):
        """Generates the characters from `c1` to `c2`, inclusive."""
        for c in xrange(ord(c1), ord(c2)+1):
            yield chr(c)
    
    @staticmethod
    def count_valid_file(path):
        count = 0
        for file in Utility.list_file(path):
            if file.startswith('.'): continue
            count+=1
        return count
    
    @staticmethod
    def fill_zero(number, fill_index):
        str = '{}'.format(number)
        return str.zfill(fill_index)
    
    @staticmethod
    def save_obj(obj, outpath_file ):
        with open(outpath_file, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    
    @staticmethod
    def load_obj(name):
        with open(name, 'rb') as f:
            return pickle.load(f)
    
    @staticmethod
    def make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    @staticmethod
    def get_color_map(number_of_colors, color_spec=matplotlib.cm.jet):
        cmap = color_spec#plt.get_cmap('hot')#matplotlib.cm.jet
        colors = [cmap(float(i) / number_of_colors) for i in range(number_of_colors)]
        return colors
    
    
    @staticmethod
    def yaml_load(name):
        stream = file(name, 'r')    # 'document.yaml' contains a single YAML document.
        # usage example:
        #return Utility.ordered_load(stream, yaml.SafeLoader)
        return yaml.load(stream)

    @staticmethod
    def yaml_save(name, yaml_obj):
        print name
        yaml_handler.dump(yaml_obj, open(name, 'w'))

    @staticmethod
    def load_json(file):
        import json
        
        with open(file) as data_file:    
            data = json.load(data_file)
            
        return data
    
    @staticmethod
    def save_json(outfilepath, data):
        with open(outfilepath, 'w') as outfile:
            json.dump(data, outfile)
    
    @staticmethod
    def print_json_beautifully(json_text):
        parsed = json.loads('{}'.format(json_text))
        print json.dumps(parsed, indent=4, sort_keys=True)
       
    @staticmethod
    def print_yaml_formatted(yaml_obj):
        print yaml.dump(yaml_obj)
    
    @staticmethod 
    def list_file(file_path):
        return os.listdir("{}".format(file_path))
        
    @staticmethod
    def copyFile(src,dst):
        shutil.copyfile(src, dst)
    
    @staticmethod
    def appendFile(file, text):
        with open(file, "a") as myfile:
            myfile.write(text)
        myfile.close()
    
    @staticmethod
    def logging_create(log_file_path):

        logging.basicConfig(filename=log_file_path,level=logging.DEBUG)
        #logging.debug('kuy')
    
    @staticmethod
    def logging_debug(text):
        logging.debug(text)
    
    @staticmethod
    def remove_file(path):
        os.remove(path)
    
    @staticmethod
    def get_input_sensitivity(input_sensitivity, ndim):    
        return input_sensitivity.argsort()[::-1][:ndim]
    
    @staticmethod
    def get_basefilename(str):
        spl = str.split('/')
        return spl[len(spl)-1].split('.')[0]
    
    @staticmethod
    def read_file_line_by_line(filepath):
        with open(filepath) as f:
            content = f.readlines()
        return content
    
    @staticmethod
    def read_lf0_into_ascii(file, output_is_f0=False):
        lf0_ascii = commands.getstatusoutput('x2x +fa {}'.format(file))[1].splitlines() 
#         print lf0_ascii
        lf0 = np.array(lf0_ascii)
        lf0 = lf0.astype(np.float)
        
        if output_is_f0:
            return np.exp(lf0)
        
        else :
            return lf0
        
        pass
    
#     import os
#     import shutil
    @staticmethod
    def copy_rename(old_file_name, new_file_name):
            src_dir= os.curdir
            dst_dir= os.path.join(os.curdir , "subfolder")
            src_file = os.path.join(src_dir, old_file_name)
            shutil.copy(src_file,dst_dir)
            
            dst_file = os.path.join(dst_dir, old_file_name)
            new_dst_file_name = os.path.join(dst_dir, new_file_name)
            os.rename(dst_file, new_dst_file_name)
    
    @staticmethod
    def write_to_file_line_by_line(filepath, list):
        f = open(filepath,'w')
        for l in list:
            f.write('{}\n'.format(l)) # python will convert \n to os.linesep
        f.close() # you can omit in most cases as the destructor will call it
    
    #pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+""",re.VERBOSE)
    #match = re.match(pattern, line)
    #phone = match.group('curphone')
    