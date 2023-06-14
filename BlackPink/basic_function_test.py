# imports
import numpy as np
from substitution import *
from tiling import *

# ============================================================
# EXAMPLE 1
# a -> aba
# b -> ab

alphabet = ["a", "b"]

rule = {
"a": "aba",
"b": "ba"
}

sub1 = substitution(alphabet = alphabet, rule = rule)
# check we make the correct matrix
print("matrix = ")
print(sub1.A)
print("Left PF = ")
print(sub1.PF)
print("--------------------")
print("length_dictionary")
print(sub1.length_dictionary)
print("--------------------")
print("--------------------")
alphabet = ["1", "2"]

rule = {
"1": "121",
"2": "21"
}

sub2 = substitution(alphabet = alphabet, rule = rule)

print(sub2.A)
print("check that we get the same shit regardless of the alphabet")
print("--------------------")
print("length_dictionary")
print(sub2.length_dictionary)
print("--------------------")

initial_condition = "12|12"
print("hit the word 12|12 by ")
print("1 -> 121, 2 -> 21")
print("--------------------")
print("hit once")
print(sub2.hit_k_times(initial_condition,1))
print("--------------------")
print("hit twice")
print(sub2.hit_k_times(initial_condition,2))
print("--------------------")
print("hit thrice")
print(sub2.hit_k_times(initial_condition,3))
# ============================================================
# check plotting of 1 words
tile = tiling("abab|babab", sub1)
print("--------------------")
print("abab|babab")
tile.plot_tiles()

tile = tiling("1212|21212", sub2)
print("--------------------")
print("1212|21212")
tile.plot_tiles()

# ====================
# check plotting of words
#

tile = tiling(["bbaa|bbbaa","1212|21212"], [sub1, sub2])
tile.plot_tiles()
#
#
plt.show()
