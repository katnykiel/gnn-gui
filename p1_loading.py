# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 00:39:28 2023

@author: eholb
"""
# pip install mp-api
# pip install ase
# pip install matplotlib
# no pip install pymatgen

from mp_api.client import MPRester
import matplotlib.pyplot as plt
from ase.io import read
from ase.visualize import view
from ase.visualize.plot import plot_atoms
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.io.cif import CifParser

API_KEY = "" # from file
mp_id = "mp-749"

# Another Conversion Method

# mpr = MPRester(API_KEY)
# structure = mpr.get_structure_by_material_id(mp_id)
# file_contents = structure.to(filename="temp.cif")  # Convert structure to CIF format for visualization
# ase_atoms = AseAtomsAdaptor().get_atoms(structure)
# fig, ax = plt.subplots()
# plot_atoms(ase_atoms, ax, radii=0.3, rotation=('0x,0y,0z'))
# plt.show()
# fig.savefig('uhh.png')

# atoms = read('temp.cif')


def get_structure_from_MatProj(API_key, mp_id):
    # API_KEY = 'sqYeL3B93wHlJpdauje7XxlySnwrf9Vx'
    # mp_id = 'mp-749'
    mpr = MPRester(API_key)
    structure = mpr.get_structure_by_material_id(mp_id)
    ase_atoms = AseAtomsAdaptor().get_atoms(structure)

    return structure, ase_atoms


def visualize_structure(ase_atoms, img="ase_temp.png"):
    fig, ax = plt.subplots()
    plot_atoms(ase_atoms, ax, radii=0.3, rotation=("0x,0y,0z"))
    plt.show()
    fig.savefig(img)


def cif_to_structure(file):
    # with open(file,'r') as f:
    #   f.readlines()
    parser = CifParser(file)
    structure = parser.get_structures()[0]
    ase_atoms = AseAtomsAdaptor().get_atoms(structure)

    return structure, ase_atoms


def Ethan():
    API_key = "sqYeL3B93wHlJpdauje7XxlySnwrf9Vx"
    mp_id = "mp-22897"

    s1, ase1 = get_structure_from_MatProj(API_key, mp_id)

    visualize_structure(ase1, img="s1.png")

    s2, ase2 = cif_to_structure("temp.cif")

    visualize_structure(ase2, img="s2.png")


Ethan()
