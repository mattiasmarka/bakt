from demos_common import *


name = "H2"
default_length = 0.74


def geomfn(length): return (("H", (0, 0, 0)),
                            ("H", (0, 0, length)))


basis = "sto-3g"
mult = 1
charge = 0
nelecs = 2

if __name__ == "__main__":
    run_demo_common(name, default_length, geomfn, basis, mult, charge, nelecs)
