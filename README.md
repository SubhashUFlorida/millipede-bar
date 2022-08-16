# millipede-bar
Analytical model for a longitudinal elastic stress wave propagating through a 180° bend junction between two parallel bars.

# Install
You can simply clone the repository with the following command:

```git clone https://github.com/SubhashUFlorida/millipede-bar.git```

All functions and classes are in the `millipede_bar` module.

## Requirements
- numpy
- pandas
- toml
- click

# Usage
## Inputs

Two input files are required:
- CSV file with the incident stress wave data. The first column should be the time and the second column the stress. Example waveforms are provided in the `data` folder.
- TOML file with the following parameters. 
  - elastic modulus
  - density
  - length of the junction
  - gage distance

  An example is provided in the `parameters.toml` file.

The gage distance is the distance between the measurement location of the waveform and the beginning of the junction. This optional parameter is used to calculate the delay between the incident and reflected/transmitted signals. If it is not provided, the delay is assumed to be zero, i.e., the waves will overlap.

## Example code
```python
from millipede_bar import get_incident_data, model_1d


# Import incident waveform from a csv file
# Example waveforms are available in the `data` folder
df_exp = get_incident_data(path_to_csv)

# Get analytical model predictions for transmitted and reflected waveforms
# An example of the parameter file can be found in parameters.toml
df_analytical = model_1d(df_incident=df_exp, parameter_file=path_to_toml_file)
df_analytical.to_csv(path_to_new_csv)
```
Example usage, with plots, is demonstrated in the `Examples.ipynb` notebook.

## Command line interface
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

# Citation
If using this work, please cite the following paper:
```citation
Ghatu Subhash, Joachin Garcia-Suarez, Amith Cheenady, Salil Bavdekar,, Jean-Francois Molinari, Wil Whittington,
Elastic stress wave propagation through a 180° bend in a square cross-sectional bar,
International Journal of Engineering Science,
2022,
In press.
```