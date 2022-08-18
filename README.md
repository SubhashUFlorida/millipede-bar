# millipede-bar
Analytical model for a longitudinal elastic stress wave propagating through a 180° bend junction between two parallel bars.

## Install
You can simply clone the repository with the following command:

```git clone https://github.com/SubhashUFlorida/millipede-bar.git```

All functions and classes are in the `millipede_bar` module.

### Requirements
- numpy
- pandas
- toml
- click

## Usage
### Inputs

Two input files are required:
- CSV file with the incident stress wave data. The first column should be the time and the second column the stress. Example waveforms are provided in the `data` folder.
- TOML file with the following parameters (in SI units). 
  - elastic modulus
  - density
  - length of the junction
  - gage distance

  An example is provided in the `parameters.toml` file.

The gage distance is the distance between the measurement location of the waveform and the beginning of the junction. This optional parameter is used to calculate the delay between the incident and reflected/transmitted signals. If it is not provided, the delay is assumed to be zero, i.e., the waves will overlap.

### Example code

Example usage, with plots, is also demonstrated in the `Examples.ipynb` notebook.

```python
from pathlib import Path

import toml

import millipede_bar as mb

# Read the parameters from the TOML file
experimental_parameters = toml.load("parameters.toml")

# Import incident waveform from a csv file
# Example waveforms are available in the `data` folder
df_incident = mb.get_incident_data(Path('data/experimental.csv'))

# Get analytical model predictions for transmitted and reflected waveforms
# An example of the parameter file can be found in parameters.toml
df_analytical = mb.model_1d(
  df_incident=df_incident, experimental_parameters=experimental_parameters
)
df_analytical.to_csv(Path('data/analytical.csv'))
```

### Command line interface
A command line interface is also provided by the `millipede-bar` script.

```bash
python millipede_bar.py [OPTIONS]

Options:
  --incident PATH    CSV file with first two columns as Time and Incident
                     signal.
  --parameters PATH  TOML file with material and geometric parameters.
                     [default: parameters.toml]
  --write            Flag to write results to CSV file, with suffix "_ana_1D"
                     [default: False]
  --help             Show this message and exit.
```

## Citation
If using this work, please cite the following paper:
```bibtex
@article{SUBHASH2022103748,
title = {Stress wave propagation through a 180° bend junction in a square cross-sectional bar},
journal = {International Journal of Engineering Science},
volume = {180},
pages = {103748},
year = {2022},
issn = {0020-7225},
doi = {https://doi.org/10.1016/j.ijengsci.2022.103748},
url = {https://www.sciencedirect.com/science/article/pii/S0020722522001136},
author = {Ghatu Subhash and Joaquin Garcia-Suarez and Amith Cheenady and Salil Bavdekar and Wilburn Whittington and Jean-Francois Molinari},
keywords = {Solid mechanics, Wave mechanics, Stress path reversal, 180° bend},
abstract = {Longitudinal elastic stress wave propagation through a 180° bend junction connecting two square bars is analyzed using analytical and numerical approaches and validated against experiments. The aim is to identify conditions under which the one-dimensional stress propagation principles can be applied to this geometry despite complete reversal of the stress wave path and study the mechanism of wave propagation through this geometry. By assuming the junction to move as a rigid body parallel to the input wave direction, the influence of the bend is analyzed for different pulse shapes and durations. For long duration stress pulses, the bend allows the stress wave to “flow” through the junction without distortion, whereas for short duration stress pulses, the wave undergoes significant dispersion. The junction behavior was further analyzed using finite element analysis and the results compared well with those of the analytical model. The wave motion through the junction results in asymmetric deformation of the junction, which generates flexural waves of different amplitudes in both the input and output bars. In general, stress pulses with constant peak amplitude and a smooth transition to the peak value suffer minimal dispersion as they traverse the junction. It is concluded that one-dimensional stress wave theory can be used to successfully model the propagation of long-duration longitudinal stress pulses around a 180° bend junction.}
}
```