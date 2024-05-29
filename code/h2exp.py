import qiskit
import numpy
import argparse
import qiskit_aer
import qiskit_aer
import time
import sys

import cmpham
import cu
import pea


def calc_energy(ham, nelecs, nbits, ntrots, bound, backend, nshots):
    assert nbits >= 1
    assert ntrots >= 1
    assert bound > 0.0
    assert nshots >= 1
    state_size = max(map(len, ham.keys()))
    state_prep_qc = qiskit.QuantumCircuit(state_size, name="state_prep")
    state_prep_qc.x(list(range(nelecs)))
    state_prep = state_prep_qc.to_instruction()
    scaling_factor = (2 * numpy.pi) / (2 * bound)
    xcu = cu.make_cu(state_size, ham, scaling_factor, ntrots)
    qc = pea.make_pea_qc(nbits, state_size, state_prep, xcu)
    depth = qc.decompose().decompose().depth()
    start = time.time_ns()
    results = backend.run(
        qiskit.transpile(
            qc,
            backend),
        nshots=nshots).result()
    end = time.time_ns()
    avg_time = (end - start) / nshots
    phase = pea.calc_phase(results)
    energy = -(phase - 1 if phase > 0.5 else phase) * 2 * bound
    return energy, state_size, depth, avg_time


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nbits", type=int, required=True)
    parser.add_argument("--ntrots", type=int, required=True)
    parser.add_argument("--bound", type=float, required=True)
    parser.add_argument("--lengths", type=float, nargs="+", default=0.74)
    parser.add_argument("--device", type=str, default="CPU")
    parser.add_argument("--nshots", type=int, default=1024)
    args = parser.parse_args()
    assert args.device in ["CPU", "GPU"]
    backend = qiskit_aer.AerSimulator(method="statevector", device=args.device)
    return args.nbits, args.ntrots, args.bound, args.lengths, backend, args.nshots


def main():
    nbits, ntrots, bound, lengths, backend, nshots = get_args()
    assert len(lengths) >= 1
    for length in lengths:
        assert 0.0 < length < 3.0
        geom = (("H", (0, 0, 0)),
                ("H", (0, 0, length)))
        basis = "sto-3g"
        mult = 1
        charge = 0
        mol = cmpham.make_mol(
            "h2-%s" %
            hash(
                (length,
                 basis,
                 mult,
                 charge)),
            geom,
            basis,
            mult,
            charge)
        fci_energy = mol.fci_energy
        ham = cmpham.make_jw_ham(mol)
        energy, state_size, depth, time = calc_energy(
            ham, 2, nbits, ntrots, bound, backend, nshots)
        print(
            nbits,
            ntrots,
            bound,
            length,
            energy,
            fci_energy,
            state_size,
            depth,
            time,
            sep="\t")
    return


if __name__ == "__main__":
    main()
