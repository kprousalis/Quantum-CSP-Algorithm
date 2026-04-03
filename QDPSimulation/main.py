# Project: Quantum Dot Plot Constructor
# Author: Konstantinos Prousalis
# Two Steps:
# Step 1. Amplitude encoding
# Step 2. Parallel XOR

# Libraries ============================================================================================================
# Standard python libraries
import matplotlib.pyplot as plt
import numpy as np
import math
import seaborn as sns
import time

# Qiskit Libraries
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, Aer, transpile
from qiskit.visualization import plot_histogram

# BioPython libraries
from Bio.Seq import Seq

# Implemented functions ================================================================================================
from base_enc import base_enc
from entanglement_circuit import entanglement_circuit
from xor_circuit import xor_circuit

# Manual example input parameters ======================================================================================

# 04 qubits embed a sequence of 16
# seq1 = Seq("CTTTGTCACAACCCAT")
# seq2 = Seq("AGGACGTAGCTGAACT")
# Perfect match
# seq1 = Seq("ACTTTGGTGGCATCGA")
# seq2 = Seq("ACTTTGGTGGCATCGA")
# Perfect match with repetitive patterns
# seq1 = Seq("ACTGACTGACTGACTG")
# seq2 = Seq("ACTGACTGACTGACTG")
# Perfect match with repetitive patterns
# seq1 = Seq("ACTGCCGTACTGCCGT")
# seq2 = Seq("ACTGCCGTACTGCCGT")

# 05 qubits embed a sequence of 32
# Perfect match without repetitive patterns
# [::-1]
seq1 = Seq("AGATTATGCAGCGATGCTAGCAGAGTGTAGAA")
seq2 = Seq("AGATTATGCAGCGATGCTAGCAGAGTGTAGAA")
# Full Dissimilarity
# seq1 = Seq("AGATTATGCAGCGATGCTAGCAGAGTGTAGAA")
# seq2 = Seq("GTGACTAGCTTGTACAGCGATGCTGATGCAGC")
# Homologous (partial match)
# seq1 = Seq("AGATGATGCAGCGATGCTAGCAGAGTGTAGAA")
# seq2 = Seq("CCCCGTTGCAGCGATGCTAGCACGCTAGCTGA")
# Perfect unmatch
# seq1 = Seq("AGATGATCCTGTGACCCTGTCGGAGTGTAGAA")
# seq2 = Seq("CCCCGTTGCAGCGATGCTAGCACGCTAGCTGA")
# Perfect match with repetitive pattern
# seq1 = Seq("ACTGACTGACTGACTGACTGACTGACTGACTG")
# seq2 = Seq("ACTGACTGACTGACTGACTGACTGACTGACTG")
# Perfect match with no repetitive patterns
# seq1 = Seq("AGCTGACTAGGACGTACTAGCTAGTCGAGTAC")
# seq2 = Seq("AGCTGACTAGGACGTACTAGCTAGTCGAGTAC")

# 06 qubits embed a sequence of 64
# seq1 = Seq("ACAAAGGCTGCTGCCGGATCGGTCAGTATTCTAACTGGTATCGATCTAGCATCTGCTGAGCTAG")
# seq2 = Seq("ACAAAGGCTGCTGCCGGATCGGTCAGTATTCTAACTGGTATCGATCTAGCATCTGCTGAGCTAG")
# seq1 = Seq("ACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTG")
# seq2 = Seq("ACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTG")
# seq1 = Seq("ACTGACTGACTGACTGACTGGAACGACCCACGCTACCTAGTCGATGCTAGTCGATGCTGATCGC")
# seq2 = Seq("ACTGACTGACTGACTGACTGGAACGACCCACGCCTGACTGACTGACTGACTGACTGACTGACTG")

# 07 qubits embed a sequence of 128
# seq1 = Seq("ACAAAAGCTGCTGATCGATCGGTCAGTATTCTATCGACTATCGATCTAGCATCTGCTGAGCTAGACAAAAGCTGCTGATCGATCGGTCAGTATTCTATCGACTATCGATCTAGCATCTGCTGAGCTAG")
# seq2 = Seq("ACAAAAGCTGCTGATCGATCGGTCAGTATTCTATCGACTATCGATCTAGCATCTGCTGAGCTAGACAAAAGCTGCTGATCGATCGGTCAGTATTCTATCGACTATCGATCTAGCATCTGCTGAGCTAG")
# seq1 = Seq("ACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTG")
# seq2 = Seq("ACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTGACTG")


print(seq1)
print(seq2)
seq1_len = len(seq1)
seq2_len = len(seq2)
num_qbitSetX = int(math.log(seq1_len, 2))
num_qbitSetY = int(math.log(seq2_len, 2))
# NoQubits = int(math.log(seq1_length, 2))*2
print('The required number of qubits to embed both sequences is: ', num_qbitSetX + num_qbitSetY)

# start timer
st = time.time()

# QCircuit Construction ================================================================================================
# Building the Memory Space
qr_x = QuantumRegister(num_qbitSetX, 'x')
qr_y = QuantumRegister(num_qbitSetY, 'y')
qr_encX = QuantumRegister(2, 'eX')  # used for base encoding of seq
qr_encY = QuantumRegister(2, 'eY')
qr_f = QuantumRegister(1, 'f')
cr_QFT = ClassicalRegister(num_qbitSetX+num_qbitSetY, 'c')
cr_f = ClassicalRegister(1, 'c_f')

qc = QuantumCircuit()
qc.add_register(qr_x)
qc.add_register(qr_y)
qc.add_register(qr_encX)
qc.add_register(qr_encY)
qc.add_register(qr_f)
qc.add_register(cr_QFT)
qc.add_register(cr_f)

# Base/Amp Encoding of dot-matrix ==============================================================================
base_enc(seq1, seq2, num_qbitSetX, num_qbitSetY, qc, qr_x, qr_y)
# amp_enc_dagger() alternative encoding scheme, it works but not compatible with the rest code

# Entanglement circuit =========================================================================================
entanglement_circuit(qc, num_qbitSetX, num_qbitSetY)

# XOR circuit / dotplot generation =============================================================================
xor_circuit(qc, num_qbitSetX, num_qbitSetY)

# Measuring f ==================================================================================================
qc.measure(num_qbitSetX+num_qbitSetY+4, num_qbitSetX+num_qbitSetY)
qc.barrier()

qc.measure(range(0, num_qbitSetX+num_qbitSetY), range(0, num_qbitSetX+num_qbitSetY))
# qc.measure(0, 0)
# qc.measure(1, 1)

# Visualizations ===============================================================================================

# Dot matrix view
# dotplot_view(dotplot2DArray, winSize)

# Circuit drawing and view
qc.draw(output='mpl')
# print(circuit) # it works only for console

# st = time.process_time() # only for cpu time consumption

# Prepare QASM simulator for histogram of amplitudes ===========================================================
# It presupposes to apply measurements to the circuit
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = backend_sim.run(transpile(qc, backend_sim),   shots=10000)
result_sim = job_sim.result()
counts = result_sim.get_counts(qc)
# print(len(counts))
# print("Dictionary of counts:", counts)

# Get the executionCPU  time ===================================================================================
# et = time.process_time()
# res = et - st
# print('CPU Execution time:', res, 'seconds')

# Dot-matrix preparation =======================================================================================
res_dot_matrix = np.zeros((seq1_len, seq2_len))
keyList = list(range(seq1_len*seq2_len))
valList = [0]*(seq1_len*seq2_len)
str_keeper = num_qbitSetX+num_qbitSetY+2
for key, value in counts.items():
    if key[0:1] == '1':
        sliced_key_dec = int(key[2:str_keeper], 2)
        x = int((sliced_key_dec - (sliced_key_dec % seq1_len)) / seq1_len)
        y = int(sliced_key_dec % seq1_len)
        res_dot_matrix[x][y] = value * 0.00001
        valList[sliced_key_dec] = value
    else:
        pass

# print(len(keyList))
# print(len(valList))
kv_Dict = dict(list(zip(keyList, valList)))

# Creating Heatmap =============================================================================================
fig2 = plt.figure()
colormap = sns.color_palette("Greens")

sns.heatmap(res_dot_matrix, cmap=colormap, annot=False, annot_kws={"size": 7})

# Creating histogram ===========================================================================================
fig3 = plt.figure()
ax3 = fig3.add_subplot(111)
plt.xlabel('Probability per Quantum State')
print("edw1",kv_Dict)
kv_Dict2 = {k: (v if k % 33 == 0 else 0) for k, v in kv_Dict.items()}
print("edw2",kv_Dict2)
keyss = list(kv_Dict2.keys())
num_to_erase = len(keyss)// 2
for key in keyss[num_to_erase:]:
    kv_Dict2[key] = 0
plot_histogram(kv_Dict2, title="Q State Amplitudes", ax=ax3)
plt.xticks(ticks=range(0, len(kv_Dict2), 100))

# Sort dictionary ==============================================================================================
# converted_dict = dict(sorted_footballers_by_goals)
new_dict = {}
for kk, vv in kv_Dict.items():
    if 50 < vv:
        new_dict[kk] = vv

sorted_dict = dict(sorted(new_dict.items(), key=lambda x:x[1], reverse=True))
print(sorted_dict)

counter = 0
for kkk in sorted_dict:
    if (kkk % (seq1_len/2)) == 0.0:
        counter = counter + 1
print("Found ", counter, " out of ", len(sorted_dict))

# Get the elapsed time =========================================================================================
et = time.time()
elapsed_time = et - st
print('Execution time:', elapsed_time, 'seconds')

plt.show()
