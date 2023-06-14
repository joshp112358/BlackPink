import numpy as np
from substitution import *
from tiling import *

# ============================================================
# Define substitution rules tau1 and tau2
alphabet1 = ["1", "2", "3"]
rule1 = {
"1": "3121",
"2": "211",
"3": "12"
}

tau1 = substitution(alphabet = alphabet1, rule = rule1)

alphabet2 = ["1", "2", "3"]
rule2 = {
"1": "2131",
"2": "211",
"3": "12"
}

tau2 = substitution(alphabet = alphabet2, rule = rule2)

print(tau1.A)

# ============================================================
initial_condition = "1|2"
number_of_powers = 6

one_hit_tau_1 = tau1.hit_k_times(initial_condition,number_of_powers)
one_hit_tau_2 = tau2.hit_k_times(initial_condition,number_of_powers)

# these are strings with the marked zero point with "|"
print(one_hit_tau_1)
print("-------------")
print("-------------")
print(one_hit_tau_2)

# ============================================================

#
# plot
#
fig = plt.figure(np.random.randint(1000), figsize=(8,8))
ax = fig.add_subplot(1, 1, 1)
ax.set_aspect('equal', adjustable='box')
ax.set_axis_off()

tile = tiling([one_hit_tau_1,one_hit_tau_2], [tau1, tau2], fig = fig, ax = ax)
# tile = tiling(one_hit_tau_1, tau1, fig = fig, ax = ax)
tile.plot_tiles()

print("-------------")
print("number of words = ", len(tile.label_dictionary))
#
#
fig.set_size_inches(500, 18)
fig.savefig('tiling6.pdf', format='pdf')


fig2 = plt.figure(np.random.randint(1000), figsize=(8,8))
ax2 = fig2.add_subplot(1, 1, 1)
ax2.set_aspect('equal', adjustable='box')
ax2.set_axis_off()
tile.plot_annotations(fig = fig2, ax = ax2)

fig2.set_size_inches(10,5)
fig2.savefig('legend6.pdf', format='pdf')

plt.show()
