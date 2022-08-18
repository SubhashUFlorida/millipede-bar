#!/usr/bin/env python
# coding: utf-8
"""
Usage: millipede_bar.py [OPTIONS]

  Read input waveform and produce transmitted and reflected waveforms. All
  waveforms are normalized to the maximum input signal.

Options:
  --incident PATH    CSV file with first two columns as Time and Incident
                     signal.
  --parameters PATH  TOML file with material and geometric parameters.
                     [default: parameters.toml]
  --write            Flag to write results to CSV file, with suffix "_ana_1D"
                     [default: False]
  --help             Show this message and exit.
"""

from pathlib import Path

import click
import numpy as np
import pandas as pd
import toml


def get_incident_data(file):
    """
    Read incident signal from csv file.

    :param file: CSV file with first two columns as Time and Incident signal.
    :return: DataFrame with Normalized incident signal.
    """
    if type(file) is str:
        file = Path(file)
    suffix = file.suffix
    if suffix.lower() != ".csv":
        raise ValueError("Extension must be .csv")

    df = pd.read_csv(
        file, usecols=[0, 1], header=0, names=["Time", "Incident"], dtype=float
    )
    df.set_index("Time", inplace=True)
    df.dropna(inplace=True)
    max_signal = max(df["Incident"].abs().tolist())
    df["Incident"] = df.loc[:, "Incident"].div(max_signal)

    return df


def model_1d(df_incident, experimental_parameters):
    """
    Read incident DataFrame and calculate Transmitted and Reflected Signals.

    :param df_incident: DataFrame with Time (as index) and Incident signal.
    :param parameter_file: TOML file with material and geometric parameters.
    :return: DataFrame with results of 1D analytical model.
    """
    material_properties = experimental_parameters["material_properties"]
    elastic_modulus = material_properties["elastic_modulus"]
    density = material_properties["density"]
    c = np.sqrt(elastic_modulus / density)

    geometric_parameters = experimental_parameters["geometric_parameters"]
    junction_length = geometric_parameters["junction_length"]
    t_ch = junction_length / c  # Characteristic time (T_ch, s)
    try:
        gage_distance = geometric_parameters["gage_distance"]
    except KeyError:
        gage_distance = 0.0

    time = df_incident.index.to_numpy(copy=True)
    dt = np.around(np.median(np.diff(time)), 9)
    incident = df_incident["Incident"].to_numpy(copy=True)
    incident[np.where(incident > 0.0)] = 0

    # To match the time steps between incident and transmitted arrays
    if gage_distance == 0.0:
        delay = 0.0
    else:
        delay = np.around(((2 * gage_distance + junction_length) / c), decimals=9)
        delay = ((delay * 1e9) // (dt * 1e9)) * dt

    kernel = np.exp(-time / t_ch) / t_ch

    transmitted = -1 * np.convolve(kernel, incident) / np.sum(kernel)
    transmitted = transmitted[: len(incident)]
    reflected = -(incident + transmitted)
    time_output = np.around((time + delay), decimals=9)
    df_output = pd.DataFrame(
        {"Reflected": reflected, "Transmitted": transmitted}, index=time_output
    )

    df_analytical = df_incident.merge(
        df_output, how="outer", left_index=True, right_index=True
    )

    return df_analytical


@click.command()
@click.option(
    "--incident",
    type=click.Path(exists=True),
    help="CSV file with first two columns as Time and Incident signal.",
)
@click.option(
    "--parameters",
    type=click.Path(exists=True),
    default="parameters.toml",
    show_default=True,
    help="TOML file with material and geometric parameters.",
)
@click.option(
    "--write",
    is_flag=True,
    default=False,
    show_default=True,
    help='Flag to write results to CSV file, with suffix "_ana_1D"',
)
def main(incident, parameters, write):
    """
    Read input waveform and produce transmitted and reflected waveforms.
    All waveforms are normalized to the maximum input signal.
    """
    experimental_parameters = toml.load(parameters)
    df_incident = get_incident_data(file=incident)
    df_analytical = model_1d(
        df_incident=df_incident, experimental_parameters=experimental_parameters
    )

    if write:
        filename = incident.stem
        save_dir = incident.parent
        df_analytical.to_csv(save_dir / f"{filename}_ana_1D.csv")

    return df_analytical


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    main()
