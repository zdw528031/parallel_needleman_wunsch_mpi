from mpi4py import MPI
import numpy as np
import random
import string
from timeit import default_timer as timer
import sys

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

def determine(AP):
    if AP.i_index == 0 or AP.j_index == 0:
        return True
    return False

def remove_job_done(AP_Array,local_back_tracking_result):
    for AP in AP_Array:
        if determine(AP):
            local_back_tracking_result.append(AP)
    AP_Array[:] = [ x for x in AP_Array if not determine(x)]
    if len(AP_Array) == 0:
        return "break_sign"

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

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

GAP = -1
MATCH = 1
MISMATCH = -1

#sequence_one = randomString(int(sys.argv[1]))
#sequence_two = randomString(int(sys.argv[1]))

sequence_one = "GCATGCU"
sequence_two = "GATTACA"

length_of_sequence_one = len(sequence_one)
length_of_sequence_two = len(sequence_two)

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

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

def calculate_result(Data_Matrix,i,j,local_sequence_two):
    vertical_value = Data_Matrix[i-1][j] + GAP
    horizontal_value = Data_Matrix[i][j-1] + GAP
    if local_sequence_two[i-1] == sequence_one[j-1]:
        diagonal_value = Data_Matrix[i-1][j-1] + MATCH
    else:
        diagonal_value = Data_Matrix[i-1][j-1] + MISMATCH
    return max_vaule_of_three_and_find_where_it_come_from(vertical_value,horizontal_value,diagonal_value)

if rank == 0:
    start = timer()
    local_sequence_two = sequence_two[length_of_sequence_two*(rank)/size:length_of_sequence_two*(rank+1)/size]
    Local_Data_Matrix = np.zeros((len(local_sequence_two)+1,length_of_sequence_one+1), dtype = np.int)
    Local_Data_Matrix[0][1:length_of_sequence_one+1] = np.arange(1,length_of_sequence_one+1) * GAP
    Local_Data_Matrix[1:,0] = np.arange(1,len(local_sequence_two)+1)*GAP

    Local_Pointer_Matrix = np.zeros((len(local_sequence_two)+1,length_of_sequence_one+1), dtype = np.int)
    phase_checker = 1
    i = 1
    j = 1
    while i != len(local_sequence_two)+1 and j != length_of_sequence_one+1:
        return_value = calculate_result(Local_Data_Matrix,i,j,local_sequence_two)
        Local_Data_Matrix[i,j] = return_value[0]
        Local_Pointer_Matrix[i,j] = return_value[1]

        if i == len(local_sequence_two):
            data = Local_Data_Matrix[i,j]
            comm.send(data, dest=rank+1, tag=rank)
        i += 1
        j -= 1
        if j == 0 or i > len(local_sequence_two):
            phase_checker += 1
            j = phase_checker
            i = 1
            continue
    i = 2
    j = length_of_sequence_one
    phase_checker = 2
    while i != len(local_sequence_two)+1 or j != length_of_sequence_one:
        return_value = calculate_result(Local_Data_Matrix,i,j,local_sequence_two)
        Local_Data_Matrix[i,j] = return_value[0]
        Local_Pointer_Matrix[i,j] = return_value[1]
        if i == len(local_sequence_two):
            data = Local_Data_Matrix[i,j]
            comm.send(data, dest=rank+1, tag=rank)
        i += 1
        j -= 1
        if i > len(local_sequence_two):
            phase_checker += 1
            i = phase_checker
            j = length_of_sequence_one
            continue
    data = comm.recv(source=rank+1, tag=rank+1)
    Alignment_Pair_Array = data
    local_back_tracking_result = []
    for AP in Alignment_Pair_Array:
        AP.i_index = len(local_sequence_two)
    while True:
        if remove_job_done(Alignment_Pair_Array,local_back_tracking_result) == "break_sign":
            break
        for AP in Alignment_Pair_Array:
            Pointer = Local_Pointer_Matrix[AP.i_index,AP.j_index]
            if Pointer == 0:
                print("error")
                exit(0)
            if Pointer == 1:
                AP.align_sequence_one.insert(0, "-")
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
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
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
                AP.i_index -= 1

                NEW_AP.align_sequence_one.insert(0, sequence_one[NEW_AP.j_index-1])
                NEW_AP.align_sequence_two.insert(0, "-")
                NEW_AP.j_index -= 1

                Alignment_Pair_Array.append(NEW_AP)
                break
            if Pointer == 4:
                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
                AP.j_index -= 1
                AP.i_index -= 1
                break
            if Pointer == 5:#ONLY_VERTICAL_AND_DIAGONAL
                NEW_AP = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
                AP.j_index -= 1
                AP.i_index -= 1

                NEW_AP.align_sequence_one.insert(0, "-")
                NEW_AP.align_sequence_two.insert(0, local_sequence_two[NEW_AP.i_index-1])
                NEW_AP.i_index -= 1
                
                Alignment_Pair_Array.append(NEW_AP)
                break
            if Pointer == 6:#ONLY_HORIZONTAL_AND_DIAGONAL
                NEW_AP = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
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
            AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
            AP.j_index -= 1
            AP.i_index -= 1

            NEW_AP_1.align_sequence_one.insert(0, "-")
            NEW_AP_1.align_sequence_two.insert(0, local_sequence_two[NEW_AP.i_index-1])
            NEW_AP_1.i_index -= 1

            NEW_AP_2.align_sequence_one.insert(0, sequence_one[NEW_AP.j_index-1])
            NEW_AP_2.align_sequence_two.insert(0, "-")
            NEW_AP_2.j_index -= 1

            Alignment_Pair_Array.append(NEW_AP_1)
            Alignment_Pair_Array.append(NEW_AP_2)
            break
    end = timer()
    total_time = end - start
    for AP in local_back_tracking_result:
        print(AP.align_sequence_one)
        print(AP.align_sequence_two)
        print("-------------------")
    
    print("total time:"+str(total_time))

    
else:
    local_sequence_two = sequence_two[length_of_sequence_two*(rank)/size:length_of_sequence_two*(rank+1)/size]
    Local_Data_Matrix = np.zeros((len(local_sequence_two)+1,length_of_sequence_one+1), dtype = np.int)
    Local_Data_Matrix[:rank*length_of_sequence_two+1,0] = np.arange(rank*length_of_sequence_two/size,(rank+1)*length_of_sequence_two/size+1)*GAP

    Local_Pointer_Matrix = np.zeros((len(local_sequence_two)+1,length_of_sequence_one+1), dtype = np.int)

    for index in range(length_of_sequence_one):
        data = comm.recv(source=rank-1, tag=rank-1)
        Local_Data_Matrix[0,index+1] = data
        i = 1
        j = index+1
        while True:
            return_value = calculate_result(Local_Data_Matrix,i,j,local_sequence_two)
            Local_Data_Matrix[i,j] = return_value[0]
            Local_Pointer_Matrix[i,j] = return_value[1]
            if i == len(local_sequence_two) and rank != size-1:
                data = Local_Data_Matrix[i,j]
                comm.send(data, dest=rank+1, tag=rank)
            i += 1
            j -= 1
            if j == 0 or i > len(local_sequence_two):
                break
    i = 2
    j = length_of_sequence_one
    phase_checker = 2
    while i != len(local_sequence_two)+1 or j != length_of_sequence_one:
        return_value = calculate_result(Local_Data_Matrix,i,j,local_sequence_two)
        Local_Data_Matrix[i,j] = return_value[0]
        Local_Pointer_Matrix[i,j] = return_value[1]
        if i == len(local_sequence_two) and rank != size-1:
            data = Local_Data_Matrix[i,j]
            comm.send(data, dest=rank+1, tag=rank)
        i += 1
        j -= 1
        if i > len(local_sequence_two):
            phase_checker += 1
            i = phase_checker
            j = length_of_sequence_one
            continue

    if rank == size - 1:
        Alignment_Pair_Array = [Alignment_Pair(len(local_sequence_two),length_of_sequence_one)]
    else:
        data = comm.recv(source=rank+1, tag=rank+1)
        Alignment_Pair_Array = data
    local_back_tracking_result = []
    if rank != size - 1:
        for AP in Alignment_Pair_Array:
            AP.i_index = len(local_sequence_two)
    while True:
        if remove_job_done(Alignment_Pair_Array,local_back_tracking_result) == "break_sign":
            break
        for AP in Alignment_Pair_Array:
            Pointer = Local_Pointer_Matrix[AP.i_index,AP.j_index]
            if Pointer == 0:
                print("error")
                exit(0)
            if Pointer == 1:
                AP.align_sequence_one.insert(0, "-")
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
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
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
                AP.i_index -= 1

                NEW_AP.align_sequence_one.insert(0, sequence_one[NEW_AP.j_index-1])
                NEW_AP.align_sequence_two.insert(0, "-")
                NEW_AP.j_index -= 1

                Alignment_Pair_Array.append(NEW_AP)
                break
            if Pointer == 4:
                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
                AP.j_index -= 1
                AP.i_index -= 1
                break
            if Pointer == 5:#ONLY_VERTICAL_AND_DIAGONAL
                NEW_AP = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
                AP.j_index -= 1
                AP.i_index -= 1

                NEW_AP.align_sequence_one.insert(0, "-")
                NEW_AP.align_sequence_two.insert(0, local_sequence_two[NEW_AP.i_index-1])
                NEW_AP.i_index -= 1
                
                Alignment_Pair_Array.append(NEW_AP)
                break
            if Pointer == 6:#ONLY_HORIZONTAL_AND_DIAGONAL
                NEW_AP = Alignment_Pair(AP.i_index,AP.j_index,AP.align_sequence_one[:],AP.align_sequence_two[:])

                AP.align_sequence_one.insert(0, sequence_one[AP.j_index-1])
                AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
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
            AP.align_sequence_two.insert(0, local_sequence_two[AP.i_index-1])
            AP.j_index -= 1
            AP.i_index -= 1

            NEW_AP_1.align_sequence_one.insert(0, "-")
            NEW_AP_1.align_sequence_two.insert(0, local_sequence_two[NEW_AP.i_index-1])
            NEW_AP_1.i_index -= 1

            NEW_AP_2.align_sequence_one.insert(0, sequence_one[NEW_AP.j_index-1])
            NEW_AP_2.align_sequence_two.insert(0, "-")
            NEW_AP_2.j_index -= 1

            Alignment_Pair_Array.append(NEW_AP_1)
            Alignment_Pair_Array.append(NEW_AP_2)
            break
    data = local_back_tracking_result
    comm.send(data, dest=rank-1, tag=rank)