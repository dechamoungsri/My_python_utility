'''
Created on Jan 18, 2016

@author: decha
'''

import sys

sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')
sys.path.append('../../Inter_speech_2016/')
sys.path.append('../../')

import matplotlib.pyplot as plt
plt.rcdefaults()
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import traceback

from tool_box.util.utility import Utility
from DataModel.Syllables.SyllableDatabaseManagement import SyllableDatabaseManagement
from DataModel.Syllables.Syllable import Syllable

import GPy

import os

from Unsupervised_learning.DBSCAN_interface import DBSCAN_executioner
from Unsupervised_learning.Kmean import Kmeans_executioner

class GP_LVM_Scatter(object):

    LABEL_TYPE_STRESS = 'LABEL_TYPE_STRESS'
    LABEL_TYPE_STRESS_SEP_GPR = 'LABEL_TYPE_STRESS_SEP_GPR'
    LABEL_TYPE_STRESS_AND_SPLIT_TONE = 'LABEL_TYPE_STRESS_AND_SPLIT_TONE'
    LABEL_TYPE_SYLLABLE_SHORT_LONG = 'LABEL_TYPE_SYLLABLE_SHORT_LONG'
    LABEL_TYPE_SYLLABLE_POSITIONS = 'LABEL_TYPE_SYLLABLE_POSITIONS'
    LABEL_TYPE_TONES = 'LABEL_TYPE_TONES'
    LABEL_TYPE_ONE_TONE_STRESS_UNSTRESS = 'LABEL_TYPE_ONE_TONE_STRESS_UNSTRESS'
    LABEL_TYPE_SYLLABLE_IN_MANUAL_PHRASE = 'LABEL_TYPE_SYLLABLE_IN_MANUAL_PHRASE'
    LABEL_TYPE_SYLLABLE_IN_MANUAL_PHRASE_PLUS_SHORT_LONG_SYLLABLE = 'LABEL_TYPE_SYLLABLE_IN_MANUAL_PHRASE_PLUS_SHORT_LONG_SYLLABLE'
    LABEL_TYPE_PHONEME = 'LABEL_TYPE_PHONEME'
    LABEL_TYPE_SYLLABLE_TYPE = 'LABEL_TYPE_SYLLABLE_TYPE'
    LABEL_TYPE_FOLLOWED_BY_SIL = 'LABEL_TYPE_FOLLOWED_BY_SIL'
    LABEL_TYPE_SEPARATED_UNSUPERVISED_GROUP = 'LABEL_TYPE_SEPARATED_UNSUPERVISED_GROUP'
    LABEL_TYPE_STRESS_3D_COLORING = 'LABEL_TYPE_STRESS_3D_COLORING'

    @staticmethod
    def plot_scatter(model, data_object, outpath, label_type=None, target_tone=None, name_index_list=None, phoneme_list=None, plotted_tone=None, bivariate=False, followed_list_file=None, perform_unsupervised=False, get_only_stress=False, non_unlabelled_stress=False, get_only_gpr_data=False,
                    return_after_dbscan=False, get_only_manual_data=False, no_short_duration=False):

        data = model.X.mean

        y, name_index, tone, stress, syllable_short_long_type, syllable_positions, phonemes, syllable_type = data_object.get_GP_LVM_training_data(
            Syllable.Training_feature_tonal_part_raw_remove_head_tail_interpolated , 
            dur_position=[1,2] , no_short_duration=no_short_duration, 
            num_sampling=50, get_only_stress=get_only_stress, non_unlabelled_stress=non_unlabelled_stress, get_only_gpr_data=get_only_gpr_data, get_only_manual_data=get_only_manual_data)

        # print 'Plot scatter'
        # print stress
        # sys.exit()

        # print syllable_type
        # print model.X.mean
        x = []
        y = []

        input_sensitivity = model.input_sensitivity()
        print input_sensitivity

        index = Utility.get_input_sensitivity(input_sensitivity, 3)
        print index

        data = np.array(data)

        name_index_list = np.array(name_index_list)

        index_filter = []
        for n in name_index:
            # print n
            idx = np.where( name_index_list==n ) [0]
            # print idx
            index_filter.append(idx[0])

        data = data[index_filter]

        stress = np.array(stress)

        labels_true = np.arange(len(stress), dtype=int)
        labels_true[stress == 'Stress'] = 1
        labels_true[stress == 'Unstress'] = 0

        # print len(data), len(stress)
        # print len(labels_true), set(labels_true)
        # sys.exit()

        if len(data) != len(stress):
            print 'Error data is not equal'
            return

        plt.clf()

        if perform_unsupervised:
            try:

                DBSCAN_executioner.run(data, labels_true, os.path.dirname(outpath), [index[0], index[1]], input_sensitivity)
                # Kmeans_executioner.run(data, labels_true, os.path.dirname(outpath), [index[0], index[1]], input_sensitivity)
            except:
                print 'Error at path : {}'.format(outpath)
                traceback.print_exc()

        if return_after_dbscan:
            return

        plt.clf()

        print 'Data : {}'.format(len(data))
        print 'Stress : {}'.format(len(stress))
        # print stress

        x = data[:,index[0]]
        x = data[:,1]
        y = data[:,index[1]]
        y = data[:,0]
        z = data[:,index[2]]

        print 'syllable_positions', len(syllable_positions)

        if label_type is GP_LVM_Scatter.LABEL_TYPE_STRESS:
            # Scatter.plot(x, y, outpath, label_list=stress, color=['r','b','g'])
            
            stress_index = np.where(stress == 'Stress')
            unstress_index = np.where(stress == 'Unstress')

            mask = np.ones(len(stress), dtype=bool)
            mask[unstress_index] = False
            # print stress
            # sys.exit()
            # Scatter.plot(x[mask], y[mask], outpath, label_list=stress[mask], color=['r','b','g'], bivariate=bivariate, X_bi=x[stress_index], Y_bi=y[stress_index])
            Scatter.plot(x, y, outpath, label_list=stress, color=['r','b','g'], bivariate=bivariate, X_bi=x[stress_index], Y_bi=y[stress_index])
        elif label_type is GP_LVM_Scatter.LABEL_TYPE_STRESS_3D_COLORING:
            # Scatter.plot(x, y, outpath, label_list=stress, color=['r','b','g'])
            
            stress_index = np.where(stress == 'Stress')
            unstress_index = np.where(stress == 'Unstress')
            normalized = (z-min(z))/(max(z)-min(z)) * 100
            Scatter.plot(x, y, outpath, label_list=None, color=normalized.astype(int).tolist(), cmap='gray')
        elif label_type is GP_LVM_Scatter.LABEL_TYPE_STRESS_SEP_GPR:

            gpr_file_list = []
            for idx, n in enumerate(name_index): 
                if 'gpr' in n:
                    gpr_file_list.append(idx)

            gpr_file_list = np.array(gpr_file_list)

            stress[gpr_file_list] = 'GPR_Stress'

            stress_index = np.where(stress == 'Stress')
            unstress_index = np.where(stress == 'Unstress')

            mask = np.ones(len(stress), dtype=bool)
            mask[unstress_index] = False

            Scatter.plot(x, y, outpath, label_list=stress, color=['r','b','g'], bivariate=bivariate, X_bi=x[stress_index], Y_bi=y[stress_index])
        elif label_type is GP_LVM_Scatter.LABEL_TYPE_STRESS_AND_SPLIT_TONE:

            stress_index = np.where(stress == 'Stress')
            unstress_index = np.where(stress == 'Unstress')

            tone = np.array(tone)

            mask = np.ones(len(stress), dtype=bool)
            mask[unstress_index] = False

            outpath = Utility.get_base_path(outpath)

            canplot = True

            try:
                labels_object = Utility.load_obj('{}/clustered_label.npy'.format(outpath))
                if len(labels_object)!=len(stress):
                    canplot = False
            except:
                canplot = False

            for t in set(tone):

                Utility.make_directory('{}/tone_stress_label/'.format(outpath))
                Utility.make_directory('{}/clustering_label/'.format(outpath))
                print len(x), len(y), len(tone), len(stress) 
                Scatter.plot(x[tone==t], y[tone==t], '{}/tone_stress_label/tone_{}.eps'.format(outpath, t), label_list=stress[tone==t], bivariate=bivariate, X_bi=x[stress_index], Y_bi=y[stress_index])
                if canplot:
                    'Plot label tone {}'.format(t)
                    Scatter.plot(x[tone==t], y[tone==t], '{}/clustering_label//tone_{}.eps'.format(outpath, t), label_list=labels_object[tone==t], bivariate=bivariate, X_bi=x[stress_index], Y_bi=y[stress_index])

        elif label_type is GP_LVM_Scatter.LABEL_TYPE_SYLLABLE_SHORT_LONG:
            Scatter.plot(x, y, outpath, label_list=syllable_short_long_type)
        elif label_type is GP_LVM_Scatter.LABEL_TYPE_SYLLABLE_POSITIONS:

            long_list = []
            short_list = []

            for idx, p in enumerate(phonemes):
                v = p.split('-')[1]
                if v not in Syllable.short_vowel:
                    long_list.append(idx)
                else:
                    short_list.append(idx)

            print len(long_list) , len(x)
            x = np.array(x)
            y = np.array(y)
            syllable_positions = np.array(syllable_positions)
            Scatter.plot(x[long_list], y[long_list], outpath, label_list=syllable_positions[long_list])
        elif label_type is GP_LVM_Scatter.LABEL_TYPE_TONES:
            Scatter.plot(x, y, outpath, label_list=tone, color=['r','g','b','black','yellow'])
        elif label_type is GP_LVM_Scatter.LABEL_TYPE_ONE_TONE_STRESS_UNSTRESS:  
            tone = np.array(map(str, tone))
            stress = np.core.defchararray.add(stress, '_' )
            stress_tone = np.core.defchararray.add(stress, tone)

            target_list = np.array([])
            print target_tone
            for t in target_tone:
                print t, target_list, np.where(tone == t)
                target_list = np.union1d(target_list, np.where(tone == t)[0])
            stress_tone = stress_tone[target_list.astype(int)]#np.delete(stress_tone, delete_list)
            x = x[target_list.astype(int)]#np.delete(x, delete_list)
            y = y[target_list.astype(int)]#np.delete(y, delete_list)
            Scatter.plot(x, y, outpath, label_list=stress_tone)
        elif label_type is None :
            Scatter.plot(x, y, outpath, label_list=None)
        elif label_type is GP_LVM_Scatter.LABEL_TYPE_SYLLABLE_IN_MANUAL_PHRASE:
            name_index = np.array(name_index)
            # print name_index
            single_list = np.array(Utility.load_obj(name_index_list['single']))
            followed_by_sil_list = np.array(Utility.load_obj(name_index_list['followed_by_sil']))
            poly_list = np.array(Utility.load_obj(name_index_list['poly']))

            all_union = []

            single_indices = [] 
            for syl in single_list:
                single_indices = np.union1d(single_indices, np.where( name_index == syl)[0])
            
            followed_by_sil_indices = [] 
            for syl in followed_by_sil_list:
                followed_by_sil_indices = np.union1d(followed_by_sil_indices, np.where( name_index == syl)[0])

            poly_indices = [] 
            for syl in poly_list:
                poly_indices = np.union1d(poly_indices, np.where( name_index == syl)[0])

            name_index[single_indices.astype(int)] = 'Single '
            name_index[followed_by_sil_indices.astype(int)] = 'Followed'
            name_index[poly_indices.astype(int)] = 'Poly'

            all_union = np.union1d(all_union, single_indices)
            all_union = np.union1d(all_union, followed_by_sil_indices)
            all_union = np.union1d(all_union, poly_indices)

            mask = np.ones(len(name_index), dtype=bool)
            mask[all_union.astype(int)] = False
            name_index[mask] = 'Other'

            Scatter.plot(x, y, outpath, label_list=name_index, color=['r','g','b','y'])

        elif label_type is GP_LVM_Scatter.LABEL_TYPE_SYLLABLE_IN_MANUAL_PHRASE_PLUS_SHORT_LONG_SYLLABLE:
            
            name_index = np.array(name_index)
            # print name_index
            single_list = np.array(Utility.load_obj(name_index_list['single']))
            followed_by_sil_list = np.array(Utility.load_obj(name_index_list['followed_by_sil']))
            poly_list = np.array(Utility.load_obj(name_index_list['poly']))

            all_union = []

            single_indices = [] 
            for syl in single_list:
                single_indices = np.union1d(single_indices, np.where( name_index == syl)[0])
            
            followed_by_sil_indices = [] 
            for syl in followed_by_sil_list:
                followed_by_sil_indices = np.union1d(followed_by_sil_indices, np.where( name_index == syl)[0])

            poly_indices = [] 
            for syl in poly_list:
                poly_indices = np.union1d(poly_indices, np.where( name_index == syl)[0])

            name_index[single_indices.astype(int)] = 'Single '
            name_index[followed_by_sil_indices.astype(int)] = 'Followed'
            name_index[poly_indices.astype(int)] = 'Poly'

            all_union = np.union1d(all_union, single_indices)
            all_union = np.union1d(all_union, followed_by_sil_indices)
            all_union = np.union1d(all_union, poly_indices)

            mask = np.ones(len(name_index), dtype=bool)
            mask[all_union.astype(int)] = False
            name_index[mask] = 'Other'

            outpath = outpath.split('.')[0]

            syllable_short_long_type = np.array(syllable_short_long_type)
            short_list = np.where(syllable_short_long_type=='short')[0]
            long_list = np.where(syllable_short_long_type=='long')[0]

            # print short_list, long_list

            Scatter.plot(x[short_list], y[short_list], '{}_short.pdf'.format(outpath), label_list=name_index[short_list], color=['r','g','b','y'])
            Scatter.plot(x[long_list], y[long_list], '{}_long.pdf'.format(outpath), label_list=name_index[long_list], color=['r','g','b','y'])

        elif label_type is GP_LVM_Scatter.LABEL_TYPE_PHONEME:
            phonemes = np.array(phonemes)
            stress = np.array(stress)
            for phoneme in phoneme_list:
                if plotted_tone != '01234':
                    if plotted_tone not in phoneme: continue

                target_index = np.where(phonemes == phoneme)
                stress_index = np.where(stress == 'Stress')
                # print stress_index

                outpath = outpath.split('.')[0]
                Scatter.plot(x[target_index], y[target_index], '{}_{}.pdf'.format(outpath, phoneme), label_list=stress[target_index], bivariate=True, X_bi=x[stress_index], Y_bi=y[stress_index], title=phoneme, xlim=(-4.4657748693986417, 8.1238328278216105), ylim=(-7.2366812187855185, 6.1187134324317736))

        elif label_type is GP_LVM_Scatter.LABEL_TYPE_SYLLABLE_TYPE:

            syllable_type = np.array(syllable_type)
            stress = np.array(stress)
            types = set(syllable_type)

            for typ in types:

                print typ

                typ_index = np.where(syllable_type==typ)

                sub_stress = stress[typ_index]
                sub_x = x[typ_index]
                sub_y = y[typ_index]
                
                stress_index = np.where(sub_stress == 'Stress')
                unstress_index = np.where(sub_stress == 'Unstress')

                mask = np.ones(len(sub_stress), dtype=bool)
                mask[unstress_index] = False

                outpath = outpath.split('.')[0]

                Scatter.plot(sub_x, sub_y, '{}_{}.pdf'.format(outpath, typ), label_list=sub_stress, color=['r','b','g'], bivariate=False, X_bi=sub_x[stress_index], Y_bi=sub_y[stress_index], title=typ, xlim=(-4.4657748693986417, 8.1238328278216105), ylim=(-7.2366812187855185, 6.1187134324317736))

        elif label_type is GP_LVM_Scatter.LABEL_TYPE_FOLLOWED_BY_SIL:
            followed_list = Utility.load_obj(followed_list_file)
            fow_index = []
            name_index = np.array(name_index)
            for f in followed_list:
                k = np.where(name_index == f)[0]
                for kk in k:
                    fow_index.append(kk.astype(int))

            # print fow_index

            stress = np.array(stress)
            stress_index = np.where(stress == 'Stress')
            unstress_index = np.where(stress == 'Unstress')

            stress[stress_index] = 'Unstress'
            stress[fow_index] = 'Stress'

            Scatter.plot(x, y, outpath, label_list=stress, color=['r','b','g'], bivariate=True, X_bi=x[fow_index], Y_bi=y[fow_index])

            tone = np.array(tone)
            for t in [0,1,2,3,4]:

                x_tone = x[np.where(tone == t)]
                y_tone = y[np.where(tone == t)]
                stress_tone = stress[np.where(tone == t)]
                tone_path = '{}_{}.pdf'.format(outpath.split('.')[0], t)
                Scatter.plot(x_tone, y_tone, tone_path, label_list=stress_tone, color=['r','b','g'], bivariate=True, X_bi=x[fow_index], Y_bi=y[fow_index], title='Tone {}'.format(t), xlim=(-3.7420549236630576, 3.7939531202951904), ylim=(-4.2426927228030289, 6.3913714950885101))

            base_path = outpath.split('.')[0] 
            Utility.save_obj(x, '{}_{}.pickle'.format(base_path,'x'))
            Utility.save_obj(y, '{}_{}.pickle'.format(base_path,'y'))
            Utility.save_obj(stress, '{}_{}.pickle'.format(base_path,'stress_followed'))
            Utility.save_obj(tone, '{}_{}.pickle'.format(base_path,'tone'))

        # elif label_type is GP_LVM_Scatter.LABEL_TYPE_SEPARATED_UNSUPERVISED_GROUP:


        pass

    def __init__(self, params):
        '''
        Constructor
        '''

class Scatter(object):

    @staticmethod
    def plot(x, y, outpath, label_list=None, color=None, alpha=0.5, bivariate=False, X_bi=None, Y_bi=None, title=None, xlim=None, ylim=None, cmap=None):

        plt.clf()

        if label_list is not None:

            lab = set(label_list)
            lab = list(lab)
            # print lab
            lab.sort(reverse=True)

            label_list = np.asarray(label_list)

            if color is None:
                color = ['r', 'b', 'g']
                color = Utility.get_color_map(len(lab))

            color.reverse()
            for idx, l in enumerate(lab):
                # print label_list == l
                plt.scatter(x[label_list == l], y[label_list == l], label=l, color=color[idx] ,alpha=0.5, cmap=cmap)

        else :
            plt.scatter(x, y, alpha=0.5, c=color, cmap=cmap)

        if bivariate:
            delta = 0.025
            xx = np.arange(np.amin(X_bi), np.amax(X_bi), delta)
            yy = np.arange(np.amin(Y_bi), np.amax(Y_bi), delta)
            # xx = np.arange(-1.0, 1.0, delta)
            # yy = np.arange(-1.0, 1.0, delta)

            mux = np.mean(X_bi)
            muy = np.mean(Y_bi)

            sigmax = np.sqrt(np.cov(X_bi,Y_bi)[0][0])
            sigmay = np.sqrt(np.cov(X_bi,Y_bi)[1][1])

            sigmaxy = np.cov(X_bi,Y_bi)[0][1]

            print mux, muy, sigmax, sigmay, sigmaxy

            # xx = np.arange(mux-2*sigmax, mux+2*sigmax, delta)
            # yy = np.arange(muy-2*sigmay, muy+2*sigmay, delta)
            X, Y = np.meshgrid(xx, yy)

            Z = mlab.bivariate_normal(X, Y, sigmax=sigmax, sigmay=sigmay, mux=mux, muy=muy, sigmaxy=sigmaxy)
            # print Z
            plt.contour(X, Y, Z)

        if title is not None:
            plt.title(title)

        plt.legend()

        if xlim:
            plt.xlim(xlim)
        if ylim:
            plt.ylim(ylim)

        print plt.xlim(), plt.ylim()
        plt.savefig(outpath)

        pass

    def __init__(self, params):
        '''
        Constructor
        '''
