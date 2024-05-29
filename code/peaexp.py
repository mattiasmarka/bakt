import qiskit
import numpy
import argparse
import qiskit_aer

import pea
import cu


def calc_phase(nbits, arg, bound, backend, nshots):
    assert nbits >= 1
    assert nshots >= 0
    assert bound > 0.0
    state_prep_qc = qiskit.QuantumCircuit(1, name="state_prep")
    state_prep_qc.x(0)
    state_prep = state_prep_qc.to_instruction()
    scaling_factor = 2 * numpy.pi / (2 * bound)
    cu_qc = qiskit.QuantumCircuit(2, name="cU")
    cu_qc.cp(arg * scaling_factor, 0, 1)
    xcu = cu_qc.to_instruction()
    qc = pea.make_pea_qc(nbits, 1, state_prep, xcu)
    print(qc)
    results = backend.run(
        qiskit.transpile(
            qc,
            backend),
        nshots=nshots).result()
    raw_phase = pea.calc_phase(results)
    return (raw_phase - 1 if raw_phase > 0.5 else raw_phase) * 2 * bound


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--nbits", type=int, required=True)
    parser.add_argument("--arg", type=float, required=True)
    parser.add_argument("--bound", type=float, required=True)
    parser.add_argument("--device", type=str, default="CPU")
    parser.add_argument("--nshots", default=1024)
    args = parser.parse_args()
    assert args.device in ["CPU", "GPU"]
    backend = qiskit_aer.AerSimulator(method="statevector", device=args.device)
    return args.nbits, args.arg, args.bound, backend, args.nshots


def main():
    nbits, arg, bound, backend, nshots = get_args()
    phase = calc_phase(nbits, arg, bound, backend, nshots)
    print(phase)


if __name__ == "__main__":
    main()
