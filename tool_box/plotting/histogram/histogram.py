import numpy as np
import matplotlib.pyplot as plt

class VerticalHistogram(object):
    '''
    classdocs
    '''

    @staticmethod
    def plot(data, label, caption, outfile):

    	plt.clf()

    	# plt.hist(data, label=label, alpha=0.75)
    	# plt.title(caption)

    	plt.bar(label, data, width=0.75, align='center')
    	plt.xticks(label, map(str,label))
    	# plt.yticks(range(0,max(data),yinterval))

    	plt.savefig(outfile)

    	pass