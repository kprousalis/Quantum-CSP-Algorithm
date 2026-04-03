import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit.library.standard_gates import XGate
from qiskit.circuit.library import MCMT
from qiskit.circuit.library import MCXGate
from qiskit.circuit.library import MCMTVChain
from qiskit.circuit.library import HGate


def base_enc(seq1, seq2, num_qbitsetx, num_qbitsety, qc, qr_x, qr_y):

    # print(MCXGate.get_num_ancilla_qubits(5, mode='noancilla'))

    qc.h(qr_x)
    qc.h(qr_y)
    num_qbit_index = num_qbitsetx + num_qbitsety
    # range_encx0 = list(range(0, num_qbitsetx))
    range_encx1 = list(range(0, num_qbitsetx))
    range_encx2 = list(range(0, num_qbitsetx))
    range_encx3a = list(range(0, num_qbitsetx))
    range_encx3b = list(range(0, num_qbitsetx))
    range_encx1.append(num_qbit_index + 0)
    range_encx2.append(num_qbit_index + 1)
    range_encx3a.append(num_qbit_index + 0)
    range_encx3b.append(num_qbit_index + 1)
    # range_ency0 = list(range(num_qbitsetx, num_qbit_index))
    range_ency1 = list(range(num_qbitsetx, num_qbit_index))
    range_ency2 = list(range(num_qbitsetx, num_qbit_index))
    range_ency3a = list(range(num_qbitsetx, num_qbit_index))
    range_ency3b = list(range(num_qbitsetx, num_qbit_index))
    range_ency1.append(num_qbit_index + 2)
    range_ency2.append(num_qbit_index + 3)
    range_ency3a.append(num_qbit_index + 2)
    range_ency3b.append(num_qbit_index + 3)

    listx = list(range(0, 2**num_qbitsetx))
    # print(listx)
    str_splitter = '0'+str(num_qbitsetx)+'b'
    # str_splitter='0?b' where 0? the num of bits to conserve
    # and b for conversion to binary

    for i in listx:
        token = seq1[i]
        plx = format(listx[i], str_splitter)
        # print(plx)
        if token == 'A':
            pass
        elif token == 'C':
            # mcmtx1 = MCMT(XGate().control(num_qbitsetx, None, plx), num_qbitsetx, 1).to_instruction(label='C')
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsetx, ctrl_state=plx), range_encx1)
            # qc.append(mcmtx1, range_encx1)
        elif token == 'T':
            # mcmtx1 = MCMT(XGate(label='T').control(num_qbitsetx, "T", plx), num_qbitsetx, 1).to_instruction(label='T')
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsetx, ctrl_state=plx), range_encx2)
            # qc.append(mcmtx1, range_encx2)
        elif token == 'G':
            # mcmtx1 = MCMT(XGate().control(num_qbitsetx, None, plx), num_qbitsetx, 2).to_instruction(label='G')
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsetx, ctrl_state=plx), range_encx3a)
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsetx, ctrl_state=plx), range_encx3b)
            # qc.append(mcmtx1, range_encx3)
        else:
            "There are wrong tokens !"

    qc.barrier()

    listy = list(range(0, 2 ** num_qbitsety))
    for i in listy:
        token = seq2[i]
        ply = format(listy[i], str_splitter)
        if token == 'A':
            pass
        elif token == 'C':
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsety, ctrl_state=ply), range_ency1)
            # mcmtx1 = MCMT(XGate().control(num_qbitsety, None, ply), num_qbitsety, 1).to_instruction(label='C')
            # qc.append(mcmtx1, range_ency1)
        elif token == 'T':
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsety, ctrl_state=ply), range_ency2)
            # mcmtx1 = MCMT(XGate(label='T').control(num_qbitsety, "T", ply), num_qbitsety, 1).to_instruction(label='T')
            # qc.append(mcmtx1, range_ency2)
        elif token == 'G':
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsety, ctrl_state=ply), range_ency3a)
            qc.append(MCXGate(num_ctrl_qubits=num_qbitsety, ctrl_state=ply), range_ency3b)
            # mcmtx1 = MCMT(XGate().control(num_qbitsety, None, ply), num_qbitsety, 2).to_instruction(label='G')
            # qc.append(mcmtx1, range_ency3)
        else:
            "There are wrong tokens !"

    qc.barrier()

    return qc


"""
def base_enc_dagger(dotplot2DArray, NoQubits):

    arr = dotplot2DArray.flatten()
    # print(arr)
    norm = np.linalg.norm(arr)
    SP = StatePreparation(arr / norm)
    # print(SP)
    qc_enc = QuantumCircuit(NoQubits)
    list_of_index_numbers = list(range(0, NoQubits))
    qc_enc.name = "   Embed   "
    qc_enc.append(SP, list_of_index_numbers)
    return qc_enc
"""
