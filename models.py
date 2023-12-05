from pymatgen.core import Lattice, Structure
import matgl
import megnet.utils.models
from matgl.ext.ase import Relaxer


def get_matgl_formation_energy_bulk_mod(structure):
    """
    Predicts the formation energy and bulk modulus of a given structure using MatGL and MEGNet models.

    Args:
        structure (pymatgen.Structure): The input structure.

    Returns:
        tuple: A tuple containing the final relaxed structure (pymatgen.Structure), the final energy after relaxation (float), and the predicted formation energy (float).
    """
    # Load GNN model to predict formation energy
    pot = matgl.load_model("M3GNet-MP-2021.2.8-PES")
    # Load MEGnet model to predict bulk modulus
    bulk = megnet.utils.models.load_model("logK_MP_2018")
    
    # Relax structure with MatGL
    relaxer = Relaxer(potential=pot)
    relax_results = relaxer.relax(structure, fmax=0.01, verbose=True)

    # Extract results
    final_structure = relax_results["final_structure"]
    final_energy = relax_results["trajectory"].energies[-1]

    # Predict formation energy with MEGNet
    model = matgl.load_model("MEGNet-MP-2018.6.1-Eform")
    eform = model.predict_structure(final_structure)

    # Predict bulk modulus of the relaxed structure
    predicted_K = 10 ** bulk.predict_structure(final_structure).ravel()[0]

    return final_structure, final_energy, eform, predicted_K
