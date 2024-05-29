import qiskit
import numpy
import argparse
import qiskit_aer
import time

import cmpham
import cu
import pea

basis = "sto-3g"


def make_ground_state_prep(state_size, nelecs):
    qc = qiskit.QuantumCircuit(state_size, name="state_prep")
    qc.x(list(range(nelecs)))
    return qc.to_instruction()


def sim_ground_state(ham, nelecs, nbits, ntrots, bound, device, nshots):
    assert nbits >= 1
    assert ntrots >= 1
    assert bound > 0.0
    assert device in ["CPU", "GPU"]
    assert nshots >= 1
    backend = qiskit_aer.AerSimulator(method="statevector", device=device)
    state_size = max(map(len, ham.keys()))
    state_prep = make_ground_state_prep(state_size, nelecs)
    scaling_factor = (2 * numpy.pi) / (2 * bound)
    xcu = cu.make_cu(state_size, ham, scaling_factor, ntrots)
    qc = pea.make_pea_qc(nbits, state_size, state_prep, xcu)
    results = backend.run(
        qiskit.transpile(
            qc,
            backend),
        nshots=nshots).result()
    phase = pea.calc_phase(results)
    energy = -(phase - 1 if phase > 0.5 else phase) * 2 * bound
    return energy


def time_sim_ground_state(ham, nelecs, nbits, ntrots, bound, device, nshots):
    assert nbits >= 1
    assert ntrots >= 1
    assert bound > 0.0
    assert device in ["CPU", "GPU"]
    assert nshots >= 1
    total_time = 0
    for i in range(3):
        print(ntrots, nbits, i)
        backend = qiskit_aer.AerSimulator(method="statevector", device=device)
        state_size = max(map(len, ham.keys()))
        state_prep = make_ground_state_prep(state_size, nelecs)
        scaling_factor = (2 * numpy.pi) / (2 * bound)
        xcu = cu.make_cu(state_size, ham, scaling_factor, ntrots)
        qc = pea.make_pea_qc(nbits, state_size, state_prep, xcu)
        start = time.time_ns()
        backend.run(qiskit.transpile(qc, backend), nshots=nshots)
        end = time.time_ns()
        total_time += end - start
    return total_time / 3


def calc_depth_h2(length, nbits, ntrots):
    assert 0.0 < length < 3.0
    geom = (("H", (0, 0, 0)),
            ("H", (0, 0, length)))
    mult = 1
    charge = 0
    nelecs = 2
    ham = cmpham.make_ham("h2-%.f" % length, geom, basis, mult, charge)
    state_size = max(map(len, ham.keys()))
    state_prep = make_ground_state_prep(state_size, nelecs)
    xcu = cu.make_cu(state_size, ham, 1, ntrots)
    qc = pea.make_pea_qc(nbits, state_size, state_prep, xcu)
    return qc.decompose().depth()


def sim_h2_ground_state(length, nbits, ntrots, bound,
                        device="CPU", nshots=1024):
    assert 0.0 < length < 3.0
    geom = (("H", (0, 0, 0)),
            ("H", (0, 0, length)))
    mult = 1
    charge = 0
    nelecs = 2
    ham = cmpham.make_ham("h2-%.f" % length, geom, basis, mult, charge)
    return sim_ground_state(ham, nelecs, nbits, ntrots, bound, device, nshots)


def time_sim_h2_ground_state(
        length, nbits, ntrots, bound, device="CPU", nshots=1024):
    assert 0.0 < length < 3.0
    geom = (("H", (0, 0, 0)),
            ("H", (0, 0, length)))
    mult = 1
    charge = 0
    nelecs = 2
    ham = cmpham.make_ham("h2-%.f" % length, geom, basis, mult, charge)
    return time_sim_ground_state(
        ham, nelecs, nbits, ntrots, bound, device, nshots)


def calc_h2_exact(length):
    assert 0.0 < length < 3.0
    geom = (("H", (0, 0, 0)),
            ("H", (0, 0, length)))
    mult = 1
    charge = 0
    nelecs = 2
    import pathlib
    import openfermion
    import openfermionpsi4
    name = "h2"

    def ensure_folder_exists(name):
        pathlib.Path(name).mkdir(exist_ok=True)
        return
    DATA_DIR_NAME = ".data"
    ensure_folder_exists(DATA_DIR_NAME)
    mol = openfermion.MolecularData(
        geom, basis, mult, charge, filename="%s/%s" %
        (DATA_DIR_NAME, name))
    mol = openfermionpsi4.run_psi4(
        mol,
        run_mp2=True,
        run_cisd=True,
        run_ccsd=True,
        run_fci=True)
    ham = openfermion.get_sparse_operator(openfermion.jordan_wigner(
        openfermion.transforms.get_fermion_operator(
            mol.get_molecular_hamiltonian()))).todense()
    from scipy.linalg import eigh
    vals, vec = eigh(ham)
    return min(vals)


def sim_lih_ground_state(length, nbits, ntrots, bound,
                         device="CPU", nshots=1024):
    assert 0.0 < length < 3.0
    geom = (("Li", (0, 0, 0)),
            ("H", (0, 0, length)))
    mult = 1
    charge = 0
    nelecs = 4
    ham = cmpham.make_ham("lih-%.f" % length, geom, basis, mult, charge)
    return sim_ground_state(ham, nelecs, nbits, ntrots, bound, device, nshots)
