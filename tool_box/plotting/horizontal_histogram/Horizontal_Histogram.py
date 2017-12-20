'''
Created on Jan 18, 2016

@author: decha
'''

import matplotlib.pyplot as plt
plt.rcdefaults()
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42
import numpy as np
import matplotlib.pyplot as plt

class HorizontalHistogram(object):
    '''
    classdocs
    '''

    @staticmethod
    def plot_grouped_data(grouped_data, x_label, out_filepath, xlim, xtick, figsize=None):
        
        data = grouped_data

        label = []
        plot_data = []
        col = []
        pat = []
        
        bar_pos = []
        
        bar_count = 0
        
        for idx, data_set in enumerate(data):
        
            if not HorizontalHistogram.is_Grouped_data_valid(data_set): continue

            label = label + data_set['label']
            plot_data = plot_data + data_set['plot_data']
            
            patterns = ('-', '+', 'x', '\\', '*', 'o', 'O', '.')
            color = '{}'.format(0.5/len(data)*idx )

            for a in data_set['label']:
                bar_pos.append(bar_count)
                col.append(color)
                pat.append(patterns[idx])
                bar_count+=1
            
            if idx != len(data)-1:
                bar_count+=0.5

        # fig size
        if figsize is None:
            figsize=(5, bar_count/2)
        plt.figure(figsize=figsize)

        y_pos = bar_pos

#         y_pos = [0, 1.25, 2.25, 3.5, 4.5, 5.5] #[0, 2, 3, 5, 6, 7]

        bars = plt.barh(y_pos, plot_data, align='center', alpha=0.4)
        
        col = ['#000000', '0.5', '0.5', '1', '1', '1'] #['0.0', '0.166666666667', '0.166666666667', '0.333333333333', '0.333333333333', '0.333333333333']
        
        for bar, pattern, color in zip(bars, pat, col):
#             bar.set_hatch(pattern)
            bar.set_color(color)

        print col
        print label
        
        print y_pos
        
        plt.yticks(y_pos, label, fontsize = 10)
        plt.xlabel(x_label)
        
        plt.xlim(xlim)
        plt.xticks(xtick)

        plt.tight_layout()
        plt.savefig(out_filepath)
        
        pass

    @staticmethod
    def is_Grouped_data_valid(group_data):
        if group_data['set_name'] is None : return False
        if group_data['plot_data'] is None : return False
        if group_data['label'] is None : return False
        if len(group_data['plot_data']) != len(group_data['label']) : return False
        
        return True

    @staticmethod
    def plot(data, error, label):
        pass

    def __init__(self, params):
        '''
        Constructor
        '''
        