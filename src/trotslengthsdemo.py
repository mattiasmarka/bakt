import logging
import argparse
import time
import sys

from demodata import *
from demohelpers import *

name = "trotslengthsdemo"

example_text = """example: %(prog)s --mol H2 --ntrots 2 4 8 --lengths 0.25 0.5 1 1.5 2 2.5 3 --lower -2 --higher 1 --device CPU

Results are printed to stdout, logging info to stderr."""


def get_args():
    parser = argparse.ArgumentParser(
        prog=name,
        epilog=example_text,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "--device",
        type=str,
        default="CPU",
        help="simulation device: GPU or CPU")
    parser.add_argument(
        "--lengths",
        type=float,
        nargs="+",
        default=None,
        help="bond length: positive float or list of floats")
    parser.add_argument(
        "--mol",
        type=str,
        required=True,
        help="molecular system: H2, LiH or BeH2")
    parser.add_argument(
        "--nbits",
        type=float,
        default=None,
        help="number of measurment bits: positive int or None (automatic)")
    parser.add_argument(
        "--nshots",
        type=float,
        default=1024,
        help="number of simulation shots: positive int")
    parser.add_argument(
        "--ntrots",
        type=int,
        nargs="+",
        help="number of trotter steps: positive int list of ints")
    parser.add_argument(
        "--lower",
        type=float,
        required=True,
        help="lower bound of energy: float")
    parser.add_argument(
        "--higher",
        type=float,
        required=True,
        help="higher bound of energy: float")
    args = parser.parse_args()
    assert args.mol in data.keys()
    assert args.ntrots is not None and len(
        args.ntrots) > 0 and all(
        nt > 0 for nt in args.ntrots)
    if args.lengths is None:
        args.lengths = [data[args.mol]["eqlbrm"]]
    assert len(args.lengths) > 0 and all(length > 0 for length in args.lengths)
    assert args.nbits is None or args.nbits > 0
    assert args.lower <= args.higher
    assert args.device in ["CPU", "GPU"]
    assert args.nshots > 0
    return args


def main():
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    args = get_args()
    logger = logging.getLogger("mol = %s" % args.mol)
    backend = get_backend(args.device)
    logger.info("E_l = %.10f", args.lower)
    logger.info("E_h = %.10f", args.higher)
    if args.nbits is None:
        logger.info("nbits = automatic")
    else:
        logger.info("nbits = %.10f", args.nbits)
    ddata = data[args.mol]
    for nt in args.ntrots:
        llogger = logger.getChild("ntrots = %d" % nt)
        for length in args.lengths:
            lllogger = llogger.getChild("length = %.10f" % length)
            lllogger.info("getting hamiltoninan...")
            ham, fci_E = get_ham(
                basis, args.mol, ddata["geom", length, ddata["mult"], ddata["charge"])
            lllogger.info("...done")
            lllogger.info("making circuit...")
            make_start = time.time_ns()
            qc, results_to_energy, depth = make_qc(
                ham, ddata["nelecs"], args.nbits, nt, args.lower, args.higher)
            make_stop = time.time_ns()
            make_time = make_stop - make_start
            lllogger.info(
                "...done (qubits = %d, depth = %d, time = %f min)",
                qc.num_qubits,
                depth,
                make_time / 60e9)
            lllogger.info("simulating circuit...")
            results, transp_time, run_time = run_qc(qc, backend, args.nshots)
            lllogger.info(
                "...done (transp time = %f min, run time = %f min)",
                transp_time / 60e9,
                run_time / 60e9)
            E = results_to_energy(results)
            lllogger.info("E = %.10f (fci_E = %.10f)", E, fci_E)
            print(
                "%s %f %f %f %d %d %f %f %f" %
                (args.mol,
                 length,
                 args.lower,
                 args.higher,
                 nt,
                 E,
                 fci_E,
                 depth,
                 make_time,
                 transp_time,
                 run_time))
    logger.info("all done")


if __name__ == "__main__":
    main()
