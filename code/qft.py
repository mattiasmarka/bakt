import qiskit
import numpy


def make_qft(size):
    assert size >= 1
    qr = qiskit.QuantumRegister(size)
    qc = qiskit.QuantumCircuit(qr, name="QFT")
    first = True
    for i in range(size):
        if first:
            first = False
        else:
            qc.barrier()
        qc.h(qr[i])
        for j in range(i + 1, size):
            arg = 2 * numpy.pi / 2**(j - i + 1)
            qc.cp(arg, qr[i], qr[j])
    qc.barrier()
    for i in range(size // 2):
        qc.swap(qr[i], qr[size - i - 1])
    return qc.to_instruction()


def make_qftdg(size):
    assert size >= 1
    qr = qiskit.QuantumRegister(size)
    qc = qiskit.QuantumCircuit(qr, name="QFT")
    for i in reversed(range(size // 2)):
        qc.swap(qr[i], qr[size - i - 1])
    qc.barrier()
    first = True
    for i in reversed(range(size)):
        if first:
            first = False
        else:
            qc.barrier()
        for j in reversed(range(i + 1, size)):
            arg = -2 * numpy.pi / 2**(j - i + 1)
            qc.cp(arg, qr[i], qr[j])
        qc.h(qr[i])
    return qc.to_instruction()
