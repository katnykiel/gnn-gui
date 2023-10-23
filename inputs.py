from pymatgen.core.structure import Structure


def get_structure_from_file(filename):
    """
    Load a Structure object from a file.

    Args:
        filename (str): The name of the file to load the Structure from.

    Returns:
        pymatgen.core.structure.Structure: The loaded Structure object.
    """
    return Structure.from_file(filename)
