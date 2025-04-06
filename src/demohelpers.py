import numpy
import qiskit
import qiskit_aer
import time

import cu
import pea
import cmpham

CHEMICAL_ACC = 1.59e-3


def lower_pow2(x):
    assert x > 0
    a = int(x // 2)
    while x < 2**a:
        a -= 1
    return a


def get_ham(basis, name, geom, length, mult, charge):
    mol = cmpham.make_mol(
        "%s-%s-%.10f-%d-%d" % (basis, name, length, mult, charge),
        geom(length),
        basis,
        mult,
        charge)
    fci_E = mol.fci_energy
    ham = cmpham.make_jw_ham(mol)
    return ham, fci_E


def calc_scaling_factor(E_l, E_h):
    t = 1 / (E_h - E_l)

    def phase_to_energy(phase):
        return (1 - phase) / t + E_l

    nbits = -int(lower_pow2(CHEMICAL_ACC * t))
    return t, nbits, phase_to_energy

def ham_with_shift(ham, E_l, E_h):
    if tuple() not in ham:
        ham[tuple()] = 0.0
    ham[tuple()] -= E_l
    return ham


def make_qc(ham, nelecs, nbits, ntrots, E_l, E_h):
    ham = ham_with_shift(ham, E_l, E_h)
    state_size = max(map(len, ham.keys()))
    state_prep_qc = qiskit.QuantumCircuit(state_size, name="state_prep")
    state_prep_qc.x(list(range(nelecs)))
    state_prep = state_prep_qc.to_instruction()
    t, xnbits, phase_to_energy = calc_scaling_factor(E_l, E_h)
    if nbits is None:
        nbits = xnbits
    xcu = cu.make_cu(state_size, ham, 2 * numpy.pi * t, ntrots)
    qc = pea.make_pea_qc(nbits, state_size, state_prep, xcu)
    depth = qc.decompose("cu").decompose(
        "cunotrot").decompose(["qft", "qftdg"]).depth()

    def results_to_energy(results):
        phase = pea.calc_phase(results)
        return phase_to_energy(phase)
    return qc, results_to_energy, depth


def run_qc(qc, backend, nshots):
    transp_start = time.time_ns()
    transpiled_qc = qiskit.transpile(qc, backend)
    transp_stop = time.time_ns()
    run_start = time.time_ns()
    results = backend.run(transpiled_qc, nshots=nshots).result()
    run_end = time.time_ns()
    transp_time = transp_stop - transp_start
    run_time = run_end - run_start
    return results, transp_time, run_time


def get_backend(device):
    assert device in ["CPU", "GPU"]
    return qiskit_aer.AerSimulator(method="statevector", device=device)
