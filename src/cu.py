import qiskit


def make_cu_notrot(state_size, ham, arg):
    assert state_size >= 1
    ctrl_qr = qiskit.QuantumRegister(1, name="ctrl")
    state_qr = qiskit.QuantumRegister(state_size, name="state")
    qc = qiskit.QuantumCircuit(ctrl_qr, state_qr, name="cU_notrot")
    first = True
    for (term, coef) in ham.items():
        if len(term) == 0:
            qc.p(-coef * arg, ctrl_qr[0])
            continue
        if first:
            first = False
        else:
            qc.barrier()
        for (i, pauli) in term:
            assert i < state_size
            match pauli:
                case "X":
                    qc.h(state_qr[i])
                case "Y":
                    qc.sdg(state_qr[i])
                    qc.h(state_qr[i])
                case "Z":
                    pass
        indices = [i for (i, _) in term]
        for i in indices[:-1]:
            qc.cx(state_qr[i], state_qr[indices[-1]])
        qc.crz(2 * coef * arg, ctrl_qr[0], state_qr[indices[-1]])
        for i in reversed(indices[:-1]):
            qc.cx(state_qr[i], state_qr[indices[-1]])
        for (i, pauli) in term:
            match pauli:
                case "X":
                    qc.h(state_qr[i])
                case "Y":
                    qc.h(state_qr[i])
                    qc.s(state_qr[i])
                case "Z":
                    pass
    return qc.to_instruction(label="cunotrot")


def make_cu(state_size, ham, arg, ntrotsteps):
    assert ntrotsteps >= 1
    xarg = arg / ntrotsteps
    cu_notrot = make_cu_notrot(state_size, ham, xarg)
    qc = qiskit.QuantumCircuit(state_size + 1, name="cU")
    first = True
    for _ in range(ntrotsteps):
        if first:
            first = False
        else:
            qc.barrier()
        qc.append(cu_notrot, qc.qubits)
    return qc.to_instruction(label="cu")
