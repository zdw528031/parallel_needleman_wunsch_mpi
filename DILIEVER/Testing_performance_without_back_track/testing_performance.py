import subprocess
import csv
my_dict_1 = dict()
my_dict_2 = dict()

for i in range(8,3200,32):
        cmd1 = subprocess.Popen(["python","testing_sequencial_performance.py",str(i)], stdout=subprocess.PIPE)
        for line in cmd1.stdout:
                my_dict_1[i] = str(line).replace("\r\n","")

with open('mycsvfile_1.csv','wb') as f:
    w = csv.writer(f)
    w.writerow(my_dict_1.keys())
    w.writerow(my_dict_1.values())

for i in range(8,3200,32):
        cmd2 = subprocess.Popen(["mpiexec",r"/np","8","python","testing_with_parallel_solution.py",str(i)], stdout=subprocess.PIPE)
        for line in cmd2.stdout:
                my_dict_2[i] = str(line).replace("\r\n","")

with open('mycsvfile_2.csv','wb') as f:
    w = csv.writer(f)
    w.writerow(my_dict_2.keys())
    w.writerow(my_dict_2.values())

