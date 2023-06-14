# imports
import numpy as np
from scipy.linalg import eig

# ============================================================


class substitution:
    def __init__(self, matrix = [], alphabet = [], rule = [], fix_12 = False):
        # alphabet is a list of strings
        # ["1","2","3"] or ["a", "b", "c"]
        self.alphabet = alphabet
        self.rule = rule

        self.len_alphabet = len(alphabet)
        # rule is a dictionary which maps every letter in the alphabet to a
        # word which we will have be a string.
        # a dictionary is structured
        # rule = {
        #  "1": "1213",
        #  "2": "121",
        #  "3": "12"
        # }
        self.A, self.PF = self.construct_matrix()
        self.length_dictionary = {self.alphabet[i]: self.PF[i] for i in range(len(self.alphabet))}

    def construct_matrix(self):
        # A_{ij} = the number of is in tau(j)
        A = np.zeros((self.len_alphabet,self.len_alphabet)).astype(int)
        for j in range(self.len_alphabet):
            symbol = self.alphabet[j]
            for i in range(self.len_alphabet):
                rule = self.rule[self.alphabet[i]]
                A[j,i] = rule.count(symbol)
        eigenvalues, eigenvectors = eig(A, left = True, right = False)
        PF = eigenvectors[:, np.argmax(np.abs(eigenvalues))]

        return A, np.real(PF/np.linalg.norm(PF))
        # returns the normalized left PF eigenvector (because I was worried
        # it was not normalized)


    def hit_ic(self, ic):
        # ic means initial_condition and an initial_condition will have a marked
        # 0 point which we use a |
        # so for example "ab|cd"
        # correspond to indices "-2 -1 | 0 1" in indices
        # hits the word once
        new_word = ""
        for letter in ic:
            if letter == "|":
                new_word += "|"
            else:
                new_word += self.rule[letter]
        return new_word

    def hit_k_times(self, ic, k_its):
        # hits the ic k times
        word_to_hit = ic
        for i in range(k_its):
            word_to_hit = self.hit_ic(word_to_hit)
        return word_to_hit




#
#
#
