import qiskit
import numpy
import argparse
import qiskit_aer

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
    results = backend.run(
        qiskit.transpile(
            qc,
            backend),
        nshots=nshots).result()
    phase = pea.calc_phase(results)
    energy = -(phase - 1 if phase > 0.5 else phase) * 2 * bound
    return energy


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nbits", type=int, required=True)
    parser.add_argument("--ntrots", type=int, required=True)
    parser.add_argument("--bound", type=float, required=True)
    parser.add_argument("--device", type=str, default="CPU")
    parser.add_argument("--nshots", type=int, default=1024)
    args = parser.parse_args()
    assert args.device in ["CPU", "GPU"]
    backend = qiskit_aer.AerSimulator(method="statevector", device=args.device)
    return args.nbits, args.ntrots, args.bound, backend, args.nshots


state_size = 4
coef = 2 * numpy.pi * 0.36257 / 8
ham = {((0, "X"), (1, "X"), (2, "Y"), (3, "Y")): coef,
       ((0, "Y"), (1, "Y"), (2, "X"), (3, "X")): coef,
       ((0, "Y"), (1, "X"), (2, "X"), (3, "Y")): -coef,
       ((0, "X"), (1, "Y"), (2, "Y"), (3, "X")): -coef}


def main():
    nbits, ntrots, bound, backend, nshots = get_args()
    energy = calc_energy(ham, 2, nbits, ntrots, bound, backend, nshots)
    print(energy)


if __name__ == "__main__":
    main()
