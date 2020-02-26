import numpy as np

##############################################################################
# Input info to solve the problem
##############################################################################
# Input list to be searched
v = [1, 15, 4, 20, 9]
S = 14  # S is the sum that is desired for the numbers in the sublist
L = 3  # L is de desired lenght for the sublist

###############################################################################
# External values used to solve the problem
###############################################################################
# STATE in one indicate that the list is to be search
STATE = 1
# Array to indicate state of next jumps to try for each position given
nj = np.ones(len(v), dtype=int)
lj = np.zeros(len(v), dtype=int)
set_sum = v[0]
pos = 0
init_pos = 0
save_list = [v[0]]

###############################################################################
# Principal traceback loop algorithm
###############################################################################
# All combinations are tried having always in the list v[init_pos]; once this
#  is done with the last element there are not more sublist to be checked.
# The algorithm follows the following procedure:
# 1. Try to check if the sum and len desired is satisfied by v[init_pos], if
#    desired result stop, other case to 2.
# 2. The algorithm move to the nearest value/position to the right from the
#    acual position such that this have not been added to the list so far, if
#    find sum and len desired stop, if not try to repeat two and in case of
#    not value to the right try with 3.
# 3. Go back to the last position that has been tried from the actual position,
#    set up tried jumps to zero, if the actual position is not the last
#    position of the list try 2; otherwise finish program saying that the
#    sublist in search does not exist.

while(init_pos != (len(v) - 1) and STATE):
    # The searched list is found to be satisfied in this condition
    if (set_sum == S and len(save_list) == L):
        print("\n\nThe list is given by: ", save_list)
        STATE = 0

    # It is possible to try the next value to be summed, at nj[pos] steps from
    #   v[pos].
    elif(set_sum < S and len(save_list) < L and
         (pos + nj[pos]) < len(v)):
        lj[pos + nj[pos]] = -nj[pos]  # Aave how to go back
        pos += nj[pos]  # Go to next position
        set_sum += v[pos]  # Actualize sum
        save_list.append(v[pos])  # Add the actal value to list
        # print("c1: save_list: ", save_list)  # debug print

    # It is not possible to try the next value to be summed at nj[pos] steps
    #  from v[pos], then we go back a position and set to try the next jump
    #  that have been not been tried there.
    elif(nj[init_pos] != (len(v) - init_pos)):
        set_sum -= v[pos]  # Actuaize sum
        del save_list[-1]  # Delete value that makes condition not possible
        # Set up jumps tried in deleted value (actual pos)/(from list) again to
        #   1
        nj[pos] = 1
        pos += lj[pos]  # Go back to the last position
        nj[pos] += 1  # Set it up to try the next jump to the right
        # print("c2: save_list: ", save_list, set_sum)  # debug print

    # All possible combinations that include init_pos have been tried so far,
    #   therefore we advance in init_pos a step.
    elif(nj[init_pos] == (len(v) - init_pos)):
        # Make the initialization done for v initially, but taking as initial
        #  value the right nearest to init_pos.
        init_pos += 1
        nj = np.ones(len(v), dtype=int)
        lj = np.zeros(len(v), dtype=int)
        pos = init_pos
        set_sum = v[pos]
        save_list = [v[pos]]
        # print("c3: save_list: ", save_list)  # debug print

if (init_pos == (len(v) - 1)):
    print("There is not list found")

# All is done
