# imports

import numpy as np
import matplotlib.pyplot as plt
from substitution import *
# for colors
from distinctipy import distinctipy
# ============================================================
#
# Helper Functions
#
def plot_box(end_points, label, color, y_line=0, fig = [], ax = [], fontsize = 10):
    # end_points is a list of two numbers
    # the function plots a box with base [y_line, end_points[0]] [y_line, end_points[1]]
    # and height 0.5 and colors it with a given color and puts the label in the middle in
    # helvetica, because arial is ugly.
    x = [end_points[0], end_points[1], end_points[1], end_points[0], end_points[0]]
    y = [y_line, y_line, y_line + 0.5, y_line + 0.5, y_line]
    if fig == [] and ax == []:
        fig, ax = plt.subplots()
    ax.plot(x, y, color="black", linewidth=0.05)  # Plot box border
    ax.fill(x, y, color=color, alpha=0.25)  # Fill box with color
    # Write label in the middle of the box with the specified fontsize
    text_x = (end_points[0] + end_points[1]) / 2
    text_y = y_line + 0.25
    ax.text(text_x, text_y, label,
            ha='center', va='center',
            fontsize=fontsize,
            color = color,
            weight="bold")

# test
# --------
# fig, ax = plt.subplots()
# plot_box([2,4],"Josh", "green",2,fig = fig, ax = ax)
# plot_box([0,1],"Scott", "red",0,fig = fig, ax = ax)
# plot_box([2,4],"Losha", "blue",-2,fig = fig, ax = ax)
# plt.show()

def find_word(D1, D2, input_interval):
    matching_words = []
    left_right_same = []
    length = input_interval[1]-input_interval[0]
    relevant_top_interval = 0
    relevant_bottom_interval = 0

    for word, intervals in D1.items():
        for interval in intervals:
            if input_interval[0] >= interval[0] and input_interval[1] <= interval[1]:
                matching_words.append(word)
                relevant_top_interval = interval

    for word, intervals in D2.items():
        for interval in intervals:
            if input_interval[0] >= interval[0] and input_interval[1] <= interval[1]:
                matching_words.append(word)
                relevant_bottom_interval = interval

    if relevant_top_interval[0] == relevant_bottom_interval[0] and relevant_top_interval[1] == relevant_bottom_interval[1]:
        left_right_same.append('S')
    elif relevant_top_interval[0] <= relevant_bottom_interval[0] and relevant_top_interval[1] <= relevant_bottom_interval[1]:
        left_right_same.append('L')
    else:
        left_right_same.append('R')

    result = matching_words + left_right_same + list([np.round(length, 5)])

    return result

def find_unique_entries(lst):
    unique_entries = []
    seen_entries = set()

    for entry in lst:
        key = tuple(entry[:-1])  # Ignore the last element for comparison
        last_element = entry[-1]
        duplicate = False

        for seen_entry in seen_entries:
            if abs(seen_entry[-1] - last_element) <= 0.00001:
                duplicate = True
                break

        if not duplicate:
            seen_entries.add((key, last_element))
            unique_entries.append(entry)

    return unique_entries

# ============================================================


class tiling:
    def __init__(self, words, substitutions, fig = [], ax = [], fontsize = 10):
        # words is a list of strings
        if not isinstance(words, list):
            # sorry cheap trick because I imagine two situations -- SS wants
            #
            self.words = [words]
        else:
            self.words = words
        # substitutions is a list of substitution classes
        if not isinstance(substitutions, list):
            self.substitutions = [substitutions]
        else:
            self.substitutions = substitutions
        # the ith_row corresponds to the ith coordinate
        self.coordinates = self.convert_word_to_points()
        if fig == [] and ax == []:
        # In case i forget to specify the figure and ax.
            self.fig = plt.figure(np.random.randint(1000), figsize=(8,8))
            self.ax = self.fig.add_subplot(1, 1, 1)
            self.ax.set_aspect('equal', adjustable='box')
            self.ax.set_axis_off()
        else:
            self.fig = fig
            self.ax = ax
        self.fontsize = fontsize
        # hard coding this to 10 colors fix it later
        cmap = plt.get_cmap('tab10')
        self.colors = [cmap(i) for i in range(10)]
        # convert the words to x_coordinates
        self.convert_word_to_points()



    def convert_word_to_points(self):
        self.coordinates = []
        for i in range(len(self.words)):
            word = self.words[i]
            length_dictionary = self.substitutions[i].length_dictionary
            len_word = len(word)
            points = np.zeros(len_word)
            zero_index = word.index('|')
            for j in range(zero_index+1,len_word):
                points[j] = points[j - 1] + length_dictionary[word[j]]
            for j in np.arange(zero_index-1,-1,-1):
                points[j] = points[j+1] - length_dictionary[word[j]]
            # cheap fix it for optimization
            self.coordinates.append(list(np.round(points,8)))

    def amalgamate_points_and_words(self):

        # find the x coordinates for all of the tiles
        self.all_x_points = sorted(list(set(self.coordinates[0] + self.coordinates[1])))

        # this makes the dictionary of points for the find_word function because
        # I was too stupid to think of something better

        self.word_1_dictionary = {letter:[] for letter in self.substitutions[0].alphabet}
        self.word_2_dictionary = {letter:[] for letter in self.substitutions[1].alphabet}
        zero_marker_free_word_1 = self.words[0].replace("|","")
        zero_marker_free_word_2 = self.words[1].replace("|","")
        for i in range(len(zero_marker_free_word_1)):
            self.word_1_dictionary[zero_marker_free_word_1[i]].append([self.coordinates[0][i],self.coordinates[0][i+1]])
        for i in range(len(zero_marker_free_word_2)):
            self.word_2_dictionary[zero_marker_free_word_2[i]].append([self.coordinates[1][i],self.coordinates[1][i+1]])

        # find all the words
        self.amalgamated_word_alphabet = []

        for j in range(len(self.all_x_points)-1):
            interval =[self.all_x_points[j], self.all_x_points[j+1]]
            box_information = find_word(self.word_1_dictionary,
                                                   self.word_2_dictionary,
                                                   interval)
            # box_label is a string and box_information is the list
            self.amalgamated_word_alphabet.append(box_information)


        unique_lists = [list(x) for x in set(map(tuple, self.amalgamated_word_alphabet))]

        # instead of [ladjskfn] = word i
        generated_colors = distinctipy.get_colors(len(self.amalgamated_word_alphabet))
        self.label_dictionary = {str(unique_lists[i]): ["w" + str(i+1), generated_colors[i] ]for i in range(len(unique_lists))}



    def plot_annotations(self, fig = [], ax = []):
        D = self.label_dictionary
        if fig == [] and ax == []:
            fig = plt.figure(np.random.randint(1000))
            ax = fig.add_subplot(1,1,1)
            ax.set_axis_off()
        x = 0.5
        y_start = len(D)*0.2
        spacing = 0.2
        ax.set_xlim((0,1))
        ax.set_ylim((0,y_start+1))

        for key, value in D.items():
            text = f"{value[0]} = {key}"
            color = value[1]
            plt.text(x, y_start, text, color=color,  fontsize=10, fontweight='bold', ha='center', va='center')
            y_start -= spacing

        plt.title(" num words = " + str(len(D)))


    def plot_tiles(self, plot_label = False):
        for i in range(len(self.coordinates)):
            relevant_sub = self.substitutions[i]
            # generate colors
            if i == 0:
                color_dictionary = {relevant_sub.alphabet[j]: self.colors[i+j] for j in range(relevant_sub.len_alphabet)}
            else:
                # fix the 2
                color_dictionary = {relevant_sub.alphabet[j]: self.colors[i+j+2] for j in range(relevant_sub.len_alphabet)}
            y = -1 * i
            x_coordinates = self.coordinates[i]

            zero_marker_free_word = self.words[i].replace("|","")

            for j in range(len(x_coordinates)-1):
                plot_box(end_points = [x_coordinates[j], x_coordinates[j+1]],
                         label = zero_marker_free_word[j],
                         color = color_dictionary[zero_marker_free_word[j]],
                         y_line= y,
                         fig = self.fig,
                         ax = self.ax,
                         fontsize = self.fontsize)

        # write the words

            if plot_label:
                self.ax.text(-0.8 + min(x_coordinates),  y + 0.25,
                            "word " + str(i+1),
                            ha='left',
                            va='center',
                            fontsize=10,
                            color="black")

            # mark vertical 0
        if len(self.words) > 1:
            self.amalgamate_points_and_words()


            for j in range(len(self.all_x_points)-1):
                interval =[self.all_x_points[j], self.all_x_points[j+1]]
                box_information = find_word(self.word_1_dictionary,
                                            self.word_2_dictionary,
                                            interval)
                box_label, color = self.label_dictionary[str(box_information)]
                plot_box(end_points = interval,
                              label =box_label,
                              color = color,
                              y_line= -2,
                              fig = self.fig,
                              ax = self.ax,
                              fontsize = self.fontsize)


            # make color dictionary
            # for
            #     plot_box(end_points = interval,
            #              label =box_label,
            #              color = new_colors[box_label],
            #              y_line= -2,
            #              fig = self.fig,
            #              ax = self.ax,
            #              fontsize = self.fontsize)

            if plot_label:
                self.ax.text(-0.8 + min(self.all_x_points),  -1.75,
                             "combined",
                             ha='left',
                             va='center',
                             fontsize=10,
                             color="black")


            for x in self.all_x_points:
                self.ax.plot([x,x],
                             [0.5,-2],
                             color = "gray",
                             linestyle = "dashed",
                             linewidth = 0.5)

            self.ax.plot([0,0],[0.5,-2], color = "black")










#
