
import sys
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

import numpy as np

class SubjectiveUtility(object):


    @staticmethod
    def read_pref_with_2_object(pref_object, met):

        is_cin = False

        all_score = dict()
        all_score['01'] = 0
        all_score['10'] = 0

        # met = ['00_HMM_single_level/', '01_HMM_multi_level/', '02_GPR_multi_level/']

        d = dict()
        d[met[0]] = '0'
        d[met[1]] = '1'

        for score_file in pref_object:

            # print score_file

            if 'Test' in score_file.keys()[0] : continue
            # if 'Cin' in score_file.keys()[0] : 
            #     if is_cin: 
            #         continue
            #     else: 
            #         is_cin = True

            # score = Utility.load_json('{}/{}'.format(data_folder, score_file))
            score = score_file[score_file.keys()[0]]

            # print score
            for s in score:
                # print s, score[s]
                
                for m in score[s]:
                    # print m, score[s][m]

                    if (met[0] in m) & (met[1] in m):
                        if score[s][m] == met[0]:
                            all_score['01'] = all_score['01'] + 1
                        else:
                            all_score['10'] = all_score['10'] + 1

        print '-----------------------------------------'

        for idx, k in enumerate(['01', '10']):
            print met[idx], k, all_score[k]

            # print all_score[k]/count[k]


    @staticmethod
    def read_pref_with_object(pref_object):

        is_cin = False

        all_score = dict()
        all_score['01'] = 0
        all_score['10'] = 0
        all_score['02'] = 0
        all_score['20'] = 0
        all_score['12'] = 0
        all_score['21'] = 0

        met = ['00_HMM_single_level/', '01_HMM_multi_level/', '02_GPR_multi_level/']

        d = dict()
        d[met[0]] = '0'
        d[met[1]] = '1'
        d[met[2]] = '2'

        for score_file in pref_object:

            # print score_file

            if 'Test' in score_file.keys()[0] : continue
            if 'Cin' in score_file.keys()[0] : 
                if is_cin: 
                    continue
                else: 
                    is_cin = True

            # score = Utility.load_json('{}/{}'.format(data_folder, score_file))
            score = score_file[score_file.keys()[0]]

            # print score
            for s in score:
                # print s, score[s]
                
                for m in score[s]:
                    # print m, score[s][m]

                    if (met[0] in m) & (met[1] in m):
                        if score[s][m] == met[0]:
                            all_score['01'] = all_score['01'] + 1
                        else:
                            all_score['10'] = all_score['10'] + 1

                    if (met[0] in m) & (met[2] in m):
                        if score[s][m] == met[0]:
                            all_score['02'] = all_score['02'] + 1
                        else:
                            all_score['20'] = all_score['20'] + 1

                    if (met[1] in m) & (met[2] in m):
                        if score[s][m] == met[1]:
                            all_score['12'] = all_score['12'] + 1
                        else:
                            all_score['21'] = all_score['21'] + 1

        print '-----------------------------------------'

        for k in ['01', '10', '02', '20', '12', '21']:
            print k, all_score[k]

            # print all_score[k]/count[k]

    @staticmethod
    def read_pref_2_method(data_folder, met):

        all_score = dict()
        all_score['01'] = 0
        all_score['10'] = 0

        # met = ['01_wav_gpr_single_level/', '02_wav_gpr_multi_level/', '03_wav_gpr_pog/']

        d = dict()
        d[met[0]] = '0'
        d[met[1]] = '1'

        for score_file in Utility.list_file(data_folder):
            if score_file.startswith('.') : continue
            if not 'pref' in score_file : continue

            # print score_file

            score = Utility.load_json('{}/{}'.format(data_folder, score_file))

            # print score
            for s in score:
                # print s, score[s]
                
                for m in score[s]:
                    # print m, score[s][m]

                    if (met[0] in m) & (met[1] in m):
                        if score[s][m] == met[0]:
                            all_score['01'] = all_score['01'] + 1
                        else:
                            all_score['10'] = all_score['10'] + 1

        print '-----------------------------------------'

        for k in ['01', '10']:
            print k, all_score[k]

            # print all_score[k]/count[k]

    @staticmethod
    def read_pref(data_folder):

        all_score = dict()
        all_score['01'] = 0
        all_score['10'] = 0
        all_score['02'] = 0
        all_score['20'] = 0
        all_score['12'] = 0
        all_score['21'] = 0

        met = ['01_wav_gpr_single_level/', '02_wav_gpr_multi_level/', '03_wav_gpr_pog/']

        d = dict()
        d[met[0]] = '0'
        d[met[1]] = '1'
        d[met[2]] = '2'

        for score_file in Utility.list_file(data_folder):
            if score_file.startswith('.') : continue
            if not 'pref' in score_file : continue

            # print score_file

            score = Utility.load_json('{}/{}'.format(data_folder, score_file))

            # print score
            for s in score:
                # print s, score[s]
                
                for m in score[s]:
                    # print m, score[s][m]

                    if (met[0] in m) & (met[1] in m):
                        if score[s][m] == met[0]:
                            all_score['01'] = all_score['01'] + 1
                        else:
                            all_score['10'] = all_score['10'] + 1

                    if (met[0] in m) & (met[2] in m):
                        if score[s][m] == met[0]:
                            all_score['02'] = all_score['02'] + 1
                        else:
                            all_score['20'] = all_score['20'] + 1

                    if (met[1] in m) & (met[2] in m):
                        if score[s][m] == met[1]:
                            all_score['12'] = all_score['12'] + 1
                        else:
                            all_score['21'] = all_score['21'] + 1

        print '-----------------------------------------'

        for k in ['01', '10', '02', '20', '12', '21']:
            print k, all_score[k]

            # print all_score[k]/count[k]


    @staticmethod
    def read_mos_object(mos_object):

        is_cin = False

        all_score = dict()

        c_all_score = dict()

        count = dict()

        for person_score in mos_object:

            print person_score.keys()

            if 'Test' in person_score.keys()[0] : continue
            # if 'Cin' in person_score.keys()[0] : 
            #     if is_cin: 
            #         continue
            #     else: 
            #         is_cin = True

            score = person_score[person_score.keys()[0]]

            for s in score:
                
                for k in score[s]:
                    score[s][k]
                    if k in all_score:
                        all_score[k] = all_score[k] + float(score[s][k])

                        # if k=='01_GPR_single_level/':
                        #     print float(score[s][k]), all_score[k]

                        count[k] = count[k] + 1
                        c_all_score[k].append(float(score[s][k]))
                    else:
                        all_score[k] = float(score[s][k])
                        count[k] = 1
                        c_all_score[k] = []
                        c_all_score[k].append(float(score[s][k]))
                        
        print '-----------------------------------------'

        for k in all_score:
            print k, all_score[k]
            print count[k]

            print all_score[k]/count[k]
            print 'Mean :', np.average(c_all_score[k]), 'Var :', np.var(c_all_score[k])


    @staticmethod
    def read_mos(data_folder):

        all_score = dict()

        c_all_score = dict()

        count = dict()

        for score_file in Utility.list_file(data_folder):
            if score_file.startswith('.') : continue
            if not 'mos' in score_file : continue

            # print score_file
            score = Utility.load_json('{}/{}'.format(data_folder, score_file))

            for s in score:
                # print score[s]
                for k in score[s]:
                    # print k, score[s][k]
                    if k in all_score:
                        all_score[k] = all_score[k] + float(score[s][k])

                        # if k=='01_GPR_single_level/':
                        #     print float(score[s][k]), all_score[k]

                        count[k] = count[k] + 1
                        c_all_score[k].append(float(score[s][k]))
                    else:
                        all_score[k] = float(score[s][k])
                        count[k] = 1
                        c_all_score[k] = []
                        c_all_score[k].append(float(score[s][k]))
                        
        print '-----------------------------------------'

        for k in all_score:
            print k, all_score[k]
            print count[k]

            print all_score[k]/count[k]
            print 'Mean :', np.average(c_all_score[k]), 'Var :', np.var(c_all_score[k])


    # """docstring for SubjectiveUtility"""
    # def __init__(self, arg):
    #     super(SubjectiveUtility, self).__init__()
    #     self.arg = arg
        
################################

# import sys
# sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

# from tool_box.util.utility import Utility

# import numpy as np
# import matplotlib.pyplot as plt

# def plot_barh(outpath, data, label, xlim, x_label, x_tick, xerr):

#     plt.figure(figsize=(5,2))

#     pos = range( len(data) )
#     color=['0.3','0.55','0.8']

#     plt.clf()
#     barlist=plt.barh( pos ,data, align='center', alpha=0.4 ,xerr=xerr, 
#         capsize=5,
#         error_kw={'ecolor':'0.0',   
#                           'elinewidth':2})

#     for i in range( len(color) ):
#         barlist[i].set_color(color[i])

#     plt.xlabel(x_label)
#     plt.yticks(pos, label)
#     plt.xlim(xlim)
#     plt.xticks(x_tick)
#     plt.tight_layout()

#     plt.savefig(outpath)

# if __name__ == '__main__':

#     outpath = './mos.eps'

#     label = ['Baseline', 'Manual', 'Unsupervised']

#     logF0_distortion = [2.06 , 3.49 , 3.56]
#     xerr_distortion = [0.17 , 0.17 , 0.16]

#     plot_barh(outpath, logF0_distortion, label, [1, 5], 'Mean opinion score', [1,2,3,4,5], xerr_distortion)


#     pass

############################################

# import sys
# sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

# from tool_box.util.utility import Utility

# import numpy as np
# import matplotlib.pyplot as plt

# def plot_barh(outpath, data, label, xlim, x_label, x_tick, x_tick_label, xerr):

#     plt.figure(figsize=(5,2))

#     pos = range( len(data) )
#     color=['0.3','0.55','0.8']

#     plt.clf()

#     c = [color[1], color[2], color[2]]
#     barlist=plt.barh( pos ,[100,100,100], align='center', alpha=0.4)
#     for i in range( len(color) ):
#         barlist[i].set_color(c[i])

#     c = [color[0], color[0], color[1]]
#     barlist=plt.barh( pos ,data, align='center', alpha=0.4, xerr=xerr,
#         capsize=5,
#         error_kw={'ecolor':'0.0',   
#                           'elinewidth':2})
#     for i in range( len(color) ):
#         barlist[i].set_color(c[i])

#     plt.xlabel(x_label)

#     plt.yticks(pos, [label[0], label[0], label[1]])

#     print pos

#     ax2 = plt.twinx()
#     ax2.set_ylim([-0.5,2.5])
#     ax2.set_yticks(pos)
#     ax2.set_yticklabels([label[1], label[2], label[2]])

#     plt.xlim(xlim)
#     plt.xticks(x_tick, x_tick_label)

#     plt.tight_layout()

#     plt.savefig(outpath)

# if __name__ == '__main__':

#     outpath = './pref.eps'

#     label = ['Baseline', 'Manual', 'Unsupervised']

#     logF0_distortion = [ float(16)/100*100 , float(12)/100*100 , float(52)/100*100]

#     xerr = [0.0719*100, 0.0637*100, 0.0979*100]

#     plot_barh(outpath, logF0_distortion, label, [0, 100], 'Preference score', [0, 25, 50, 75, 100], ['0%', '25%', '50%', '75%', '100%'], xerr)


#     pass


