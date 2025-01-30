import pathlib
import openfermion
import openfermionpsi4
import numpy


def ensure_folder_exists(name):
    pathlib.Path(name).mkdir(exist_ok=True)
    return


DATA_DIR_NAME = ".data"


def make_mol(name, geom, basis, mult, charge):
    fname = "%s/%s" % (DATA_DIR_NAME, name)
    ensure_folder_exists(DATA_DIR_NAME)
    mol = openfermion.MolecularData(
        geom, basis, mult, charge, filename=fname)
    mol = openfermionpsi4.run_psi4(
        mol,
        run_mp2=True,
        run_cisd=True,
        run_ccsd=True,
        run_fci=True)
    return mol


def make_jw_ham(mol):
    ham = openfermion.jordan_wigner(
        openfermion.transforms.get_fermion_operator(
            mol.get_molecular_hamiltonian())).terms
    for key in ham:
        assert numpy.imag(ham[key]) == 0
        ham[key] = numpy.real(ham[key])
    return ham
