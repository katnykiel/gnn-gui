from pymatgen.core import Lattice, Structure
import matgl
from matgl.ext.ase import Relaxer


def get_matgl_formation_energy(structure):
    """
    Predicts the formation energy of a given structure using MatGL and MEGNet models.

    Args:
        structure (pymatgen.Structure): The input structure.

    Returns:
        tuple: A tuple containing the final relaxed structure (pymatgen.Structure), the final energy after relaxation (float), and the predicted formation energy (float).
    """
    # Load GNN model
    pot = matgl.load_model("M3GNet-MP-2021.2.8-PES")

    # Relax structure with MatGL
    relaxer = Relaxer(potential=pot)
    relax_results = relaxer.relax(structure, fmax=0.01, verbose=True)

    # Extract results
    final_structure = relax_results["final_structure"]
    final_energy = relax_results["trajectory"].energies[-1]

    # Predict formation energy with MEGNet
    model = matgl.load_model("MEGNet-MP-2018.6.1-Eform")
    eform = model.predict_structure(final_structure)

    return final_structure, final_energy, eform
