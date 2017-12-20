
import sys
sys.path.append('/home/h1/decha/Dropbox/python_workspace/Utility/')

from tool_box.util.utility import Utility

class Latext_Tool(object):
    """docstring for ClassName"""

    @staticmethod
    def plot_all_data(figure_array, caption_array, outpath):

        number_of_column = len(figure_array[0])

        for l in figure_array:
            if len(l) > number_of_column:
                number_of_column = len(l)

        # print number_of_column

        latex_file = []
        Latext_Tool.latex_header(latex_file)

        column = " "
        for i in range(number_of_column):
            column = column  + "c" + " "

        width = 1/float(number_of_column)
        print width

        for i, row in enumerate(figure_array):

            tubular_header = '\\begin{{tabular}}{{{}}}'.format(column)
            latex_file.append(tubular_header)

            figure_row = ''
            # for j, fig in enumerate(row):
            for j in range(0,number_of_column):
                # if row[j] != None:
                try:
                    figure_row+= '\\includegraphics[width={}\\hsize]{{{}}}'.format(width, row[j]) 
                except:
                    # figure_row+= '\\includegraphics[width={}\\hsize]{{{}}}'.format(width, '/home/h1/decha/Dropbox/circle.eps') 
                    print 'No eps file'
                    
                if j != (len(row)-1):
                    figure_row += ' & '

            figure_row += '\\\\'
            latex_file.append(figure_row)

            figure_row = ''
            # for j, cap in enumerate(caption_array[i]):
            for j in range(0,number_of_column):
                # if caption_array[i][j] != None:
                try:
                    figure_row+= '{}'.format(caption_array[i][j]) 
                except:
                    # figure_row+= '{}'.format('Nofile') 
                    print 'No file'
                if j != (len(row)-1):
                    figure_row += ' & '

            figure_row += '\\\\'
            latex_file.append(figure_row)

            tubular_footer = '\\end{tabular}'
            latex_file.append(tubular_footer)

        Latext_Tool.latex_footer(latex_file)

        Utility.write_to_file_line_by_line(outpath, latex_file)

        # for l in latex_file:
        #     print l

    @staticmethod
    def latex_footer(latex_file):
        footer = [
            '\\end{document}'
        ]
        latex_file.extend(footer)

    @staticmethod
    def latex_header(latex_file):

        header = [
            '\\documentclass[a4paper]{article}',
            '\\usepackage[a4paper, landscape]{geometry}',
            '\\usepackage{graphicx}',
            '\\usepackage{color}',
            '\\oddsidemargin=-5pt',
            '\\evensidemargin=-5pt',
            '\\topmargin=-5pt',
            '\\begin{document}'
        ]
        latex_file.extend(header)
# '',
        # return latex_file

    def __init__(self):
        pass

# \begin{tabular}{ c c }
#   \includegraphics[width=0.25\hsize]{/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/02_delta_delta-delta/BGP_LVM/Tone_0/stress_unstress_plot.eps} & \includegraphics[width=0.25\hsize]{/home/h1/decha/Dropbox/Inter_speech_2016/Syllable_object/02_delta_delta-delta/BGP_LVM/Tone_0/stress_unstress_plot.eps} \\
#   abc & abc \\
# \end{tabular}

# \end{document}


