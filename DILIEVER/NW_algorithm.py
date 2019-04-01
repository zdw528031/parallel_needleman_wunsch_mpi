import numpy as np
import sys
import random
import string
print_mode = False
timing_mode = True
if timing_mode:
    from timeit import default_timer as timer


GAP = -1
MATCH = 1
MISMATCH = -1

back_tracking_result = []

sequence_one = "GCATGCUA"
sequence_two = "GATTACAA"

length_of_sequence_one = len(sequence_one)
length_of_sequence_two = len(sequence_two)

start = timer()
DataMatrix = np.zeros((length_of_sequence_two+1,length_of_sequence_one+1), dtype = np.int)
PointerMatrix = np.zeros((length_of_sequence_two+1,length_of_sequence_one+1), dtype = np.int)
end = timer()
init_time = end - start
"""
for pointer matrix is for backtracking
there might be lot of different implementation

for mine one pointer matrix value have different meaning states as below:

    0: NO_DIRECTION (default_value)
    1: ONLY_VERTICAL
    2: ONLY_HORIZONTAL
    3: ONLY_VERTICAL_AND_HORIZONTAL
    4: ONLY_DIAGONAL
    5: ONLY_VERTICAL_AND_DIAGONAL
    6: ONLY_HORIZONTAL_AND_DIAGONAL
    7: VERTICAL_HORIZONTAL_DIAGONAL

"""
class Alignment_Pair():
    def __init__(self,i,j,other_sequence_one = None,other_sequence_two = None):
        self.i_index = i
        self.j_index = j
        self.align_sequence_one = []
        self.align_sequence_two = []
        if other_sequence_one is not None:
            self.align_sequence_one = other_sequence_one
        if other_sequence_two is not None:
            self.align_sequence_two = other_sequence_two


def randomString(stringLength=10):
    """ Generate a random string of fixed length """
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def init_first_column_and_first_row(Matrix):
    Matrix[0][0] = 0
    Matrix[0][1:length_of_sequence_one+1] = np.arange(1,length_of_sequence_one+1)*GAP
    Matrix[1:,0] = np.arange(1,length_of_sequence_two+1)*GAP

def max_vaule_of_three_and_find_where_it_come_from(vertical,horizontal,diagonal):
    if diagonal < horizontal and diagonal < vertical:
        if horizontal == vertical:
            return horizontal,3
        if vertical > horizontal:
            return vertical,1
        return horizontal,2
    else:
        if diagonal > horizontal and diagonal > vertical:
            return diagonal,4 #ONLY_DIAGONAL
        if vertical > horizontal:
            if vertical == diagonal:
                return vertical,5
            return vertical,1
        if horizontal > vertical:
            if horizontal == diagonal:
                return horizontal,6
            return horizontal,2
        return diagonal,7
        

def get_match_or_mismatch_value(char_one,char_two):
    if char_one == char_two:
        return MATCH
    return MISMATCH


def determine(AP):
    if AP.i_index == 0 or AP.j_index == 0:
        return True
    return False

def remove_job_done(AP_Array):
    for AP in AP_Array:
        if determine(AP):
            back_tracking_result.append(AP)
    AP_Array[:] = [ x for x in AP_Array if not determine(x)]
    if len(AP_Array) == 0:
        return "break_sign"


def fill_in_matrix(Data_Matrix,Pointer_Matrix):
    for i in range(1,length_of_sequence_two+1):
        for j in range(1,length_of_sequence_one+1):
            vertical = Data_Matrix[i-1][j] + GAP
            horizontal = Data_Matrix[i][j-1] + GAP
            diagonal = Data_Matrix[i-1][j-1] + get_match_or_mismatch_value(sequence_one[j-1],sequence_two[i-1])
            return_value = max_vaule_of_three_and_find_where_it_come_from(vertical,horizontal,diagonal)
            Data_Matrix[i][j] = return_value[0]
            Pointer_Matrix[i][j] = return_value[1]

def back_track(Data_Matrix,Pointer_Matrix):
    Alignment_Pair_Array = [Alignment_Pair(length_of_sequence_two,length_of_sequence_one)]
    while True:
        if remove_job_done(Alignment_Pair_Array) == "break_sign":
            break
        for AP in Alignment_Pair_Array:
            Pointer = Pointer_Matrix[AP.i_index,AP.j_index]
            if Pointer == 0:
                print("error")
                exit(0)
            if Pointer == 1:
                AP.align_sequence_one.insert(0, "-")
                AP.align_sequence_two.insert(0, sequence_two[AP.i_index-1])
                AP.i_index -= 1
                break
            if Pointer == 2:
                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, "-")
                AP.j_index -= 1
                break
            if Pointer == 3:#ONLY_VERTICAL_AND_HORIZONTAL
                NEW_AP = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

                AP.align_sequence_one.insert(0, "-")
                AP.align_sequence_two.insert(0, sequence_two[AP.i_index-1])
                AP.i_index -= 1

                NEW_AP.align_sequence_one.insert(0, sequence_one[NEW_AP.j_index-1])
                NEW_AP.align_sequence_two.insert(0, "-")
                NEW_AP.j_index -= 1

                Alignment_Pair_Array.append(NEW_AP)
                break
            if Pointer == 4:
                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, sequence_two[AP.i_index-1])
                AP.j_index -= 1
                AP.i_index -= 1
                break
            if Pointer == 5:#ONLY_VERTICAL_AND_DIAGONAL
                NEW_AP = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, sequence_two[AP.i_index-1])
                AP.j_index -= 1
                AP.i_index -= 1

                NEW_AP.align_sequence_one.insert(0, "-")
                NEW_AP.align_sequence_two.insert(0, sequence_two[NEW_AP.i_index-1])
                NEW_AP.i_index -= 1
                
                Alignment_Pair_Array.append(NEW_AP)
                break
            if Pointer == 6:#ONLY_HORIZONTAL_AND_DIAGONAL
                NEW_AP = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, sequence_two[AP.i_index-1])
                AP.j_index -= 1
                AP.i_index -= 1

                NEW_AP.align_sequence_one.insert(0, sequence_one[NEW_AP.j_index-1])
                NEW_AP.align_sequence_two.insert(0, "-")
                NEW_AP.j_index -= 1

                Alignment_Pair_Array.append(NEW_AP)
                break
            #VERTICAL_HORIZONTAL_DIAGONAL
            NEW_AP_1 = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])
            NEW_AP_2 = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

            AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
            AP.align_sequence_two.insert(0, sequence_two[AP.i_index-1])
            AP.j_index -= 1
            AP.i_index -= 1

            NEW_AP_1.align_sequence_one.insert(0, "-")
            NEW_AP_1.align_sequence_two.insert(0, sequence_two[NEW_AP.i_index-1])
            NEW_AP_1.i_index -= 1

            NEW_AP_2.align_sequence_one.insert(0, sequence_one[NEW_AP.j_index-1])
            NEW_AP_2.align_sequence_two.insert(0, "-")
            NEW_AP_2.j_index -= 1

            Alignment_Pair_Array.append(NEW_AP_1)
            Alignment_Pair_Array.append(NEW_AP_2)
            break


if timing_mode:
    start = timer()
    init_first_column_and_first_row(DataMatrix)
    end = timer()
    init_time += end - start
    #print(init_time)
else:
    init_first_column_and_first_row(DataMatrix)
if print_mode:
    print(DataMatrix)
    pass

if timing_mode:
    start = timer()
    fill_in_matrix(DataMatrix,PointerMatrix)
    back_track(DataMatrix,PointerMatrix)
    end = timer()
    computation_time = end - start
    print("final score = "+ str(DataMatrix[length_of_sequence_two][length_of_sequence_one]) )
    print("total result number:"+str(len(back_tracking_result)))
    for AP in back_tracking_result:
        print(AP.align_sequence_one)
        print(AP.align_sequence_two)
        print("-------------------")
    print("total_time:"+str(computation_time+init_time))
else:
    fill_in_matrix(DataMatrix,PointerMatrix)
    back_track(DataMatrix,PointerMatrix)
    print("final score = "+ str(DataMatrix[length_of_sequence_two][length_of_sequence_one]) )
    print("total result number:"+str(len(back_tracking_result)))
    for AP in back_tracking_result:
        print(AP.align_sequence_one)
        print(AP.align_sequence_two)
        print("-------------------")

