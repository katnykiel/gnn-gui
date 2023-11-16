# gnn-gui

A visualization tool for graph neural networks in materials science

Created for Purdue CS 501

- Nethra Balachandar^[balachn@purdue.edu]

- Satarupa Gupta^[gupta872@purdue.edu]

- Ethan Holbrook^[holbrooe@purdue.edu]

- Kat Nykiel^[knykiel@purdue.edu]

## Installation

TODO: get OS-independent installation. This only seems to work on OS X.

### Using Conda

Build the conda environment from the environment file:

```conda env create -f environment.yml```

Load the new environment

``` conda activate gnn-gui ```

And test the GUI

```python main.py```

Congratulations!

## TODOs

### GUI (Nethra)

- [ ] fix the scaling of the GUI
- [ ] clean up GUI (remove extra buttons)
- [ ] add place to show property predictions in the GUI

### GNNs (Satarupa)

- [ ] connect GNNs other than MatGL (ALIGN, etc)
- [ ] determine which properties we want to predict

### Inputs (Ethan)

- [ ] let users upload crystal structures
- [ ] let users query materials project
- [ ] other crystal sources?

### Visualization (Kat)

- [ ] add structure vis to GUI
- [ ] add embedding vis to GUI
- [ ] add neural network vis?

### Other

- [ ] get stable, reproducible python env
- [ ] structure paper
- [X] set up on overleaf
