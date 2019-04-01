import numpy as np
import sys
import random
import string
print_mode = False
timing_mode = True
if timing_mode:
    from timeit import default_timer as timer

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

GAP = -1
MATCH = 1
MISMATCH = -1

back_tracking_result = []


#sequence_one = randomString(int(sys.argv[1]))
#sequence_two = randomString(int(sys.argv[1]))
sequence_one = "PCGMFVHRLRSLKAYQIMGGLEGAPQKFVPDGCGSAVLAGTIRMIIKDGDLECRLFNAKHVAFSLQNQDKGLSIHGNRLEQEARLATRIERAGQTSPPAGYLLITGIKDVVTSATRKDSEATYDLMVEEDVSALEPKIADKEPLTHSQFPKIFVSQEDMFFNNESTYELWVHYLARLSLIWIVTVYGRPSVVDKATNNNK"
sequence_two = "KALCAAKSEYIVVLRPKYTLTQINRENHPQLAQVKGTGRETYLVLGKMPIPASTLRASFTPLDYSPGYLAAARSMVWRSLVITKPNGSMPREPADKSKEMVKNKDIKGRFTEGEEPIRVENWGLETFKFSKKSNMTGVTTNGAVNKERAGSGSLGINHLLSVDFITASWNVDAFEYIEISEVTKIHDEVNIDLSSHRVLEGFVMHKFVGDDLGLSVAIKGVLYKPVIVMKAARDSDSVSVKLHYRVCSKLTEKAMQGGELRVDGKFRTAKVEKADENDGLEAYIESESCEHFVRIPKQGACANIVRTPILTILLKSTEQLLFQGPWGNSSGGSADKGQNPRNFIQAGLTISLNGRAYAYAVGVSQADAGDSAKRLPEATTISLIVGRSFPNVFKYNCEDRGFFSPIRHPIASTEHQQLEMEVTDIQWMIDKEIQELGLRSTFEPNLRVLMVERLQQKAPLEHPRLGNSISPNRSLIISIQTTEERTRREVSRSWEVCADVLEANFLDLPEGMAQAALTPIGHAFRMAYKLHSGVHQTTLKRPTFPLLQTEDDVQDSVHRGGQRPTKSGDTNQILILGCGWNEPRFQGSFLWDGKSGVVLELRNGDMICFLTAVRDALIKHGYEAYVEFIIAALPKLLRQDQVSRVGSVLESGFDPKPYAAQDPNDFISAIGASLGLTSLQAFDQFIDAELATILKTEYLCRLGEGESVMITRKGEDIPGPMSSNIDKGDHTRNGVLAITDSLLEVGREKLVTDADPNYDQKLYAAVANAAHSFARLANGTRDQTLVCYAAMIIDTWMDAIYIGPQGEARGFHYFQVVFGVFEKDKPRNMELFVLLANLVIMLEVIHSSIGSPAQNCVLTEYPPYMYKLITDFTENMADILGTDKKGAKRLCGVHGLKPNAVMSECSHLDIQAPSLAVPERREKVLKEADYDCRQQHRWTKTFGPIAKYRILGNEFALVKMHEDVLALNYEDSFAPNAAAVQLPWQLLLYFNSKDVLLATA"
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

def fill_in_matrix(Data_Matrix,Pointer_Matrix):
    for i in range(1,length_of_sequence_two+1):
        for j in range(1,length_of_sequence_one+1):
            vertical = Data_Matrix[i-1][j] + GAP
            horizontal = Data_Matrix[i][j-1] + GAP
            diagonal = Data_Matrix[i-1][j-1] + get_match_or_mismatch_value(sequence_one[j-1],sequence_two[i-1])
            return_value = max_vaule_of_three_and_find_where_it_come_from(vertical,horizontal,diagonal)
            Data_Matrix[i][j] = return_value[0]
            Pointer_Matrix[i][j] = return_value[1]

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


if print_mode:
    pass

    #print(DataMatrix)

if timing_mode:
    start = timer()
    init_first_column_and_first_row(DataMatrix)
    end = timer()
    init_time += end - start
    #print(init_time)
else:
    init_first_column_and_first_row(DataMatrix)
if print_mode:
    #print(DataMatrix)
    pass

if timing_mode:
    start = timer()
    fill_in_matrix(DataMatrix,PointerMatrix)
    end = timer()
    computation_time = end - start
    total_time = computation_time + init_time
    print(str(total_time))
else:
    fill_in_matrix(DataMatrix,PointerMatrix)
