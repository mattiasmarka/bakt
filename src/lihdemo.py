from demos_common import *


def geomfn(length): return (("Li", (0, 0, 0)),
                            ("H", (0, 0, length)))


basis = "sto-3g"
mult = 1
charge = 0
nelecs = 4

if __name__ == "__main__":
    run_demo_common("LiH", 1.5949, geomfn, basis, mult, charge, nelecs)
