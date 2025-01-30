import qiskit
import numpy

import qft


def make_pea_qc(pea_size, state_size, state_prep, cu):
    assert pea_size >= 1
    assert state_size >= 1
    pea_qr = qiskit.QuantumRegister(pea_size, "qPEA")
    state_qr = qiskit.QuantumRegister(state_size, "state")
    pea_cr = qiskit.ClassicalRegister(pea_size, "cPEA")
    qc = qiskit.QuantumCircuit(pea_qr, state_qr, pea_cr, name="PEA")
    qc.append(qft.make_qft(pea_size), pea_qr)
    qc.barrier()
    qc.append(state_prep, state_qr)
    qc.barrier()
    first = True
    for i in range(pea_size):
        if first:
            first = False
        else:
            qc.barrier()
        for _ in range(2**i):
            qc.append(cu, [pea_qr[pea_size - 1 - i], *state_qr])
    qc.barrier()
    qc.append(qft.make_qftdg(pea_size), pea_qr)
    qc.barrier()
    qc.measure(pea_qr, pea_cr)
    return qc


def calc_phase(results):
    counts = results.get_counts()
    x = max(counts, key=counts.get)[::-1]
    return int(x, 2) / 2**len(x)
