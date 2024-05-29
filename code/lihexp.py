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

from h2exp import get_args, calc_energy


def main():
    nbits, ntrots, bound, lengths, backend, nshots = get_args()
    assert len(lengths) >= 1
    for length in lengths:
        assert 0.0 < length < 3.0
        geom = (("Li", (0, 0, 0)),
                ("H", (0, 0, length)))
        basis = "sto-3g"
        mult = 1
        charge = 0
        mol = cmpham.make_mol(
            "h2-%.f" %
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
