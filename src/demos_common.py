import argparse
import qiskit_aer
import time
import qiskit
import numpy
import hashlib

import cu
import pea
import cmpham


def get_args_common(name="demo", default_length=float("NaN")):
    parser = argparse.ArgumentParser(prog=name)
    parser.add_argument("--nbits", type=int, required=True)
    parser.add_argument("--ntrots", type=int, nargs="+")
    parser.add_argument("--lowerbound", type=float, required=True)
    parser.add_argument("--higherbound", type=float, required=True)
    parser.add_argument(
        "--lengths",
        type=float,
        nargs="+",
        default=[default_length])
    parser.add_argument("--device", type=str, default="CPU")
    parser.add_argument("--nshots", type=int, default=1024)
    args = parser.parse_args()
    assert args.nbits >= 1
    assert len(args.ntrots) > 0
    assert all(nt >= 1 for nt in args.ntrots)
    assert args.lowerbound < args.higherbound
    assert len(args.lengths) >= 1
    assert all(length > 0 for length in args.lengths)
    assert args.device in ["CPU", "GPU"]
    assert args.nshots > 1
    backend = qiskit_aer.AerSimulator(method="statevector", device=args.device)
    return args.nbits, args.ntrots, args.lowerbound, args.higherbound, args.lengths, backend, args.nshots


def get_ham(name, geomfn, length, basis, mult, charge):
    geom = geomfn(length)
    data = "%f %s %d %f" % (length, basis, mult, charge)
    hash = hashlib.sha256(data.encode("utf-8"))
    mol = cmpham.make_mol(
        "%s-%s" %
        (name,
         hash.hexdigest()),
        geom,
        basis,
        mult,
        charge)
    fci_E = mol.fci_energy
    ham = cmpham.make_jw_ham(mol)
    return ham, fci_E


def calc_energy(ham, nelecs, nbits, ntrots, l, h, backend, nshots):
    state_size = max(map(len, ham.keys()))
    state_prep_qc = qiskit.QuantumCircuit(state_size, name="state_prep")
    state_prep_qc.x(list(range(nelecs)))
    state_prep = state_prep_qc.to_instruction()
    t = 1 / (h - l)
    xcu = cu.make_cu(state_size, ham, 2 * numpy.pi * t, ntrots)
    qc = pea.make_pea_qc(nbits, state_size, state_prep, xcu)
    depth = qc.decompose("cu").decmpose("cunotrot").decompose(["qft", qftdg"])
    start = time.time_ns()
    results = backend.run(
        qiskit.transpile(
            qc,
            backend),
        nshots=nshots).result()
    end = time.time_ns()
    _time = end - start
    phase = pea.calc_phase(results)
    lt = l * t
    ht = h * t
    x = -phase
    y = x - (x - ht + 1) // 1
    E = y / t
    return E, state_size, depth, _time


def run_demo_common(name, default_length, geomfn, basis, mult, charge, nelecs):
    nbits, ntrots, l, h, lengths, backend, nshots = get_args_common(
        name, default_length)
    print("NBITS	NTROTS	L	H	LEN	E	FCIE	STATESIZ	DEPTH	TIME")
    for length in lengths:
        for nt in ntrots:
            ham, fci_E = get_ham(name, geomfn, length, basis, mult, charge)
            E, state_size, depth, _time = calc_energy(
                ham, nelecs, nbits, nt, l, h, backend, nshots)
            print(
                nbits,
                nt,
                l,
                h,
                length,
                E,
                fci_E,
                state_size,
                depth,
                _time,
                sep="\t")
    return
