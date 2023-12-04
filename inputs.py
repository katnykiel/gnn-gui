# from pymatgen.core.structure import Structure
from mp_api.client import MPRester
import matplotlib.pyplot as plt
from ase.io import read
from ase.visualize import view
from ase.visualize.plot import plot_atoms
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.cif import CifParser

def get_structure_from_MatProj(API_key, mp_id):
    mpr = MPRester(API_key)
    structure = mpr.get_structure_by_material_id(mp_id)
    ase_atoms = AseAtomsAdaptor().get_atoms(structure)

    return structure, ase_atoms

def make_structure_image(ase_atoms, img="ase_temp.png"):
    fig, ax = plt.subplots()
    plot_atoms(ase_atoms, ax, radii=0.3, rotation=("0x,0y,0z"))
    plt.show()
    fig.savefig(img)

def get_structure_from_file(file):
    """
    Load a Structure object from a file. Also output ase_atoms object. 

    Args:
        filename (str): The name of the file to load the Structure from.

    Returns:
        pymatgen.core.structure.Structure: The loaded Structure object.
    """
    parser = CifParser(file)
    structure = parser.parse_structures()[0]
    ase_atoms = AseAtomsAdaptor().get_atoms(structure)

    return structure, ase_atoms

def load_API_key():
    '''From text box or file.'''
    with open('../api_key.txt','r') as api_file:
        API_KEY = api_file.readlines()[0].strip()
    
    return API_KEY
    
def Ethan():
    API_key = API_KEY
    mp_id = "mp-22897"

    s1, ase1 = get_structure_from_MatProj(API_key, mp_id)

