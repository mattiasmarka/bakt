import numpy
from numpy import random

from demos_common import *
import h2demo


def lower_pow2(x):
    assert x > 0
    a = int(x // 2)
    while x < 2**a:
        a -= 1
    return a


chemical_accuracy = 1.59e-3


def get_args(name="boundsdemo", default_length=float("NaN"),
             default_center=float("NaN")):
    parser = argparse.ArgumentParser(prog=name)
    parser.add_argument("--ntrots", type=int, nargs="+")
    parser.add_argument("--length", type=float, default=default_length)
    parser.add_argument("--device", type=str, default="CPU")
    parser.add_argument("--center", type=float, default=default_center)
    parser.add_argument("--base", type=float, default=2)
    parser.add_argument("--start", type=float, required=True)
    parser.add_argument("--stop", type=float, required=True)
    parser.add_argument("--steps", type=int, required=True)
    parser.add_argument("--seed", type=float, default=0)
    parser.add_argument("--nshots", type=int, default=1024)
    args = parser.parse_args()
    assert args.length > 0
    assert args.device in ["CPU", "GPU"]
    assert args.nshots > 1
    backend = qiskit_aer.AerSimulator(method="statevector", device=args.device)
    return args.ntrots, args.length, args.device, args.center, args.base, args.start, args.stop, args.steps, args.seed, backend, args.nshots


def run_bounds_demo(name, default_length, default_center):
    ntrots, length, device, center, base, start, stop, steps, seed, backend, nshots = get_args(
        name, default_length, default_center)
    random.seed(seed)
    s = base**numpy.linspace(start, stop, steps)
    c = numpy.array([center + (random.rand() - 0.5) * x for x in s])
    l = numpy.array([x - 0.5 * y for x, y in zip(c, s)])
    h = numpy.array([x + 0.5 * y for x, y in zip(c, s)])
    ham, fci_E = get_ham(name, h2demo.geomfn, length,
                         h2demo.basis, h2demo.mult, h2demo.charge)
    print("NBITS        NTROTS  L       H       LEN     E       FCIE    STATESIZ        DEPTH   TIME")
    for nt in ntrots:
        for (x, y) in zip(l, h):
            nbits = -lower_pow2(chemical_accuracy / (y - x))
            E, state_size, depth, _time = calc_energy(
                ham, h2demo.nelecs, nbits, nt, x, y, backend, nshots)
            print(
                nbits,
                nt,
                x,
                y,
                length,
                E,
                fci_E,
                state_size,
                depth,
                _time,
                sep="\t")


if __name__ == "__main__":
    run_bounds_demo(h2demo.name, h2demo.default_length, -1.13)
