from demos_common import *


def geomfn(length): return (("Be", (0, 0, 0)),
                            ("H", (0, 0, -length)),
                            ("H", (0, 0, length)))


basis = "sto-3g"
mult = 1
charge = 0
nelecs = 6

if __name__ == "__main__":
    run_demo_common("BeH2", 1.3264, geomfn, basis, mult, charge, nelecs)
