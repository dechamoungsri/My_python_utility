'''
Created on Dec 27, 2015

@author: decha
'''

import numpy
import os
import sklearn, sklearn.metrics

import sys
sys.path.append('../../')

from tool_box.util.utility import Utility
import re

class Distortion(object):
    '''
    classdocs
    '''
    
    UNDEF_VALUE = -1.0e+10
    
    @staticmethod
    def cal_duration_distortion_from_label_and_npy_list(org_path, syn_path):

        dur_true_list = []
        dur_pred_list = []

        for file in Utility.list_file(org_path):
            if file.startswith('.'): continue

            base = Utility.get_basefilename(file)
            syn = numpy.load('{}/{}.npy'.format(syn_path, base))

            for idx, line in enumerate(Utility.read_file_line_by_line('{}/{}'.format(org_path, file))):

                if ('sil' in line) | ('pau' in line) :
                    continue

                # print syn[idx]
                o = line.split(' ')

                dur_true_list.append(1000 * (float(o[1]) - float(o[0]))/10000000 )
                dur_pred_list.append(1000 * syn[idx] )

        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(dur_true_list, dur_pred_list))
        return rmse, len(dur_true_list), len(dur_pred_list)

    @staticmethod
    def cal_duration_distortion_from_path(org_path, syn_path):

        real, pred = [], []

        for f in Utility.list_file(org_path):
            if f.startswith('.'): continue
            real_phone_list, real_dur_list = Distortion.load_mono_ori_list_in_sec('{}/{}'.format(org_path, f))

            pred_phone_list, pred_dur_list = Distortion.load_mono_ori_list_in_sec('{}/{}'.format(syn_path, f))

            for r, p, c in zip(real_dur_list, pred_dur_list, real_phone_list):

                # print c

                if ('sil' in c) | ('pau' in c):
                    continue

                real.append(r*1000)
                pred.append(p*1000)

        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(real, pred))

        return (rmse, len(real), real, pred)

    @staticmethod
    def load_mono_ori_list_in_sec(file_path):

        pattern = re.compile(r"""(?P<start>.+)\s+(?P<end>.+)\s+(?P<curphone>.+)""",re.VERBOSE)

        phone_list = []
        dur_list = []

        for line in Utility.read_file_line_by_line(file_path):
            match = re.match(pattern, line)
            if match:
               phone = match.group('curphone')
               start = match.group('start')
               end = match.group('end')

               phone_list.append(phone)
               dur_list.append( (float(end) - float(start)) / 10000000 )


        return (phone_list, dur_list)

    @staticmethod
    def load_ori_list_in_sec(file_path):

        pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+""",re.VERBOSE)

        phone_list = []
        dur_list = []

        for line in Utility.read_file_line_by_line(file_path):
            match = re.match(pattern, line)
            if match:
               phone = match.group('curphone')
               start = match.group('start')
               end = match.group('end')

               phone_list.append(phone)
               dur_list.append( (float(end) - float(start)) / 10000000 )


        return (phone_list, dur_list)

    

    @staticmethod
    def duration_distortion_from_numpy_list(org_path,syn_path):

        path = syn_path

        original_path = org_path

        ori = []
        ph_list = []

        syn = []

        for f in Utility.list_file(path):
            if f.startswith('.'): continue
            if 'mean' not in f : continue

            syn_path = '{}/{}'.format(path, f)
            # print syn_path
            syn_list = numpy.load(syn_path)
            sl = syn_list.flatten()
            syn.extend(list(sl))

            base = Utility.get_basefilename(f)
            base = base[0:len(base)-5]
            ori_path = '{}/{}.lab'.format(original_path, base)
            # print ori_path

            phone_list, dur_list = Distortion.load_ori_list_in_sec(ori_path)

            ori.extend(dur_list)
            ph_list.extend(phone_list)

        # print len(ph_list), len(ori), len(syn)

        dur_true_list = []
        dur_pred_list = []

        for idx, p in enumerate( ph_list ):
            if (p == 'sil') | (p == 'pau') : continue

            dur_true_list.append(1000 * ori[idx] )
            dur_pred_list.append(1000 * syn[idx] )

        if len(dur_true_list) != len(dur_pred_list):
            print "Not equal"
            
        print dur_pred_list
        print dur_true_list

        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(dur_true_list, dur_pred_list))
        print('Duration RMSE: {:f} in {} phones'.format(rmse, len(dur_true_list)))

    @staticmethod
    def load_ori_list_in_sec_and_num_phone_list(file_path):

        pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+/A:.+/D:.+\-(?P<phone_num>.+)\+.+/E:.+""",re.VERBOSE)

        num_phone_list = []
        dur_list = []

        for line in Utility.read_file_line_by_line(file_path):
            match = re.match(pattern, line)
            if match:
               phone_num = match.group('phone_num')
               start = match.group('start')
               end = match.group('end')

               num_phone_list.append(phone_num)
               dur_list.append( (float(end) - float(start)) / 10000000 )


        return (num_phone_list, dur_list)

    @staticmethod
    def duration_distortion_from_numpy_list_syllable_level(org_path,syn_path):

        path = syn_path

        original_path = org_path

        ori = []
        ph_list = []

        syn = []

        for f in Utility.list_file(path):
            if f.startswith('.'): continue
            if 'mean' not in f : continue

            syn_path = '{}/{}'.format(path, f)
            # print syn_path
            syn_list = numpy.load(syn_path)
            sl = list(syn_list.flatten())
            
            base = Utility.get_basefilename(f)
            base = base[0:len(base)-5]
            ori_path = '{}/{}.lab'.format(original_path, base)
            # print ori_path

            phone_num, dur_list = Distortion.load_ori_list_in_sec_and_num_phone_list(ori_path)

            s_out = []

            sl_count = 0

            for pn in phone_num:
                if pn is 'x':
                    s_out.append(sl[sl_count])
                    sl_count = sl_count+1
                else :
                    d = 0
                    for i in range( int(pn) ):
                        d = d + sl[sl_count]
                        sl_count = sl_count+1
                    s_out.append(d)

            ori.extend(dur_list)
            ph_list.extend(phone_num)
            syn.extend(s_out)

        # print len(ph_list), len(ori), len(syn)

        dur_true_list = []
        dur_pred_list = []

        for idx, p in enumerate( ph_list ):
            if (p == 'x') : continue

            dur_true_list.append(1000 * ori[idx] )
            dur_pred_list.append(1000 * syn[idx] )

        if len(dur_true_list) != len(dur_pred_list):
            print "Not equal"
            
        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(dur_true_list, dur_pred_list))
        print('Duration RMSE: {:f} in {} phones'.format(rmse, len(dur_true_list)))


    @staticmethod
    def lf0_distortion_syn_is_gpr_format(org_path,syn_path):
        
        lf0_true_list = []
        lf0_pred_list = []
        
        for base in Utility.list_file(org_path) :
            
            if base.startswith('.'):
                continue
            
            # Load Original
            original_file = os.path.join(org_path, base)
            original_vector = numpy.loadtxt(Utility.read_lf0_into_ascii(original_file))
            
            # Load Synthesis
            synthesis_file = '{}/{}.npy'.format(syn_path, Utility.get_basefilename(base) )
            synthesis_vector = numpy.load(synthesis_file)
            synthesis_vector = synthesis_vector.reshape(len(synthesis_vector))

            for lf0_original, lf0_synthesis in zip(original_vector, synthesis_vector):
                if lf0_original == Distortion.UNDEF_VALUE:
                    continue
                if lf0_synthesis == Distortion.UNDEF_VALUE:
                    continue

                lf0_true_list.append(lf0_original)
                lf0_pred_list.append(lf0_synthesis)

        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
        print('LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

        pass


    @staticmethod
    def lf0_distortion_syn_is_readable(org_path,syn_path):
        
        lf0_true_list = []
        lf0_pred_list = []
        
        for base in Utility.list_file(org_path) :
            
            if base.startswith('.'):
                continue
            
            # Load Original
            original_file = os.path.join(org_path, base)
            original_vector = numpy.loadtxt(Utility.read_lf0_into_ascii(original_file))
            
            # Load Synthesis
            synthesis_file = os.path.join(syn_path, base)
            synthesis_vector = numpy.loadtxt(synthesis_file)

            for lf0_original, lf0_synthesis in zip(original_vector, synthesis_vector):
                if lf0_original == Distortion.UNDEF_VALUE:
                    continue
                if lf0_synthesis == Distortion.UNDEF_VALUE:
                    continue

                lf0_true_list.append(lf0_original)
                lf0_pred_list.append(lf0_synthesis)

        # print len(lf0_true_list), len(lf0_pred_list)
        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
        # print('LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

        return (rmse, len(lf0_true_list))

        pass


    @staticmethod
    def lf0_distortion(org_path,syn_path):
        
        lf0_true_list = []
        lf0_pred_list = []
        
        for base in Utility.list_file(org_path) :
            
            if base.startswith('.'):
                continue
            
            # Load Original
            original_file = os.path.join(org_path, base)
            original_vector = numpy.loadtxt(Utility.read_lf0_into_ascii(original_file))
            
            # Load Synthesis
            synthesis_file = os.path.join(syn_path, base)
            synthesis_vector = numpy.loadtxt(Utility.read_lf0_into_ascii(synthesis_file))

            for lf0_original, lf0_synthesis in zip(original_vector, synthesis_vector):
                if lf0_original == Distortion.UNDEF_VALUE:
                    continue
                if lf0_synthesis == Distortion.UNDEF_VALUE:
                    continue

                lf0_true_list.append(lf0_original)
                lf0_pred_list.append(lf0_synthesis)

        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(lf0_true_list, lf0_pred_list)) * 1200 / numpy.log(2)
        print('LF0 RMSE: {:f} in {} frames'.format(rmse, len(lf0_true_list)))

        pass

    @staticmethod
    def dur_distortion(org_path,syn_path):
        
        dur_true_list = []
        dur_pred_list = []
        
        for base in Utility.list_file(org_path) :
            
            if base.startswith('.'):
                continue
            
            basename = base.split('.')
#             print basename
            # Load Original
            org_file = os.path.join(org_path, '{}{}'.format(basename[0],'.lab'))
            org_duration_vector = Utility.read_file_line_by_line(org_file)

            syn_file = os.path.join(syn_path, '{}{}'.format(basename[0],'.dur'))
            syn_duration_vector_temp = Utility.read_file_line_by_line(syn_file)

            syn_duration_vector = []

            for vec in syn_duration_vector_temp:
                if not "state" in vec:
                    syn_duration_vector.append(vec)

            pattern = re.compile(r"""(?P<start>.+)\s(?P<end>.+)\s.+\-(?P<curphone>.+)\+.+/A:.+""",re.VERBOSE)
            syn_pattern = re.compile(r""".+\-(?P<phone>.+)\+.+/A:.+\sduration=(?P<duration>.+)\s\(frame\).+""",re.VERBOSE)
            
            #X-sil+ph/A:x_x-x_x+1_1/B:x-x+0/C:x_x-x_x+1_1/D:x-x+2/E:x-x+1/F:x_x-x_x+9_4/G:x_22_14/H:x_x-56_1+2_1.state[2]: duration=5 (frame), mean=4.609594e+00
            
            if len(org_duration_vector) != len(syn_duration_vector):
                print "Not equal"
            
            for org, syn in zip(org_duration_vector, syn_duration_vector):

                match = re.match(pattern, org)
                
                if match.group('curphone') in ["sil", "pau"]:
                    continue
                
                phone = match.group('curphone')
                duration = (int(match.group('end')) - int(match.group('start'))) / 50000

                syn_match = re.match(syn_pattern, syn)
                syn_duration = int(syn_match.group('duration'))

#                 print phone, duration, syn_match.group('phone') , syn_duration

                dur_true_list.append(1000 * duration *0.005)
                dur_pred_list.append(1000 * syn_duration *0.005)

        if len(dur_true_list) != len(dur_pred_list):
            print "Not equal"
            
        rmse = numpy.sqrt(sklearn.metrics.mean_squared_error(dur_true_list, dur_pred_list))
        print('Duration RMSE: {:f} in {} phones'.format(rmse, len(dur_true_list)))

    def __init__(self, params):
        '''
        Constructor
        '''
        