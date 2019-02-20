#!/usr/bin/env python

"""Python script to produce HEPData submission for arXiv:1611.03421.
Write YAML files from text files linked on H1 web page, together with
numbers given in Tables 12 and 13 of LaTeX source downloaded from arXiv.

Tested with python2 and python3.  Run with: "python process_ins1496981.py".
Reformatted with "black -l 79".  Code passes all checks with "flake8".
Running "pylint -d C0330" (some indentation conflict with black) gives code
rating of 9.80/10 (pylint suggests refactoring to make functions smaller).
"""

from __future__ import print_function

import os
import re

import pandas as pd  # Install with: pip install pandas

import yaml  # Install with: pip install pyyaml

# We try to dump using the CSafeDumper for speed improvements.
try:
    from yaml import CSafeDumper as Dumper
except ImportError:
    from yaml import SafeDumper as Dumper


__author__ = "Graeme Watt"


def main():
    """Main function of script."""

    print(__doc__)  # docstring from top of file

    input_dir = "Input"  # input directory
    # Create the input directory if it does not already exist.
    if not os.path.exists(input_dir):
        print("Creating directory {}".format(input_dir))
        os.mkdir(input_dir)
        print("Downloading files to {}".format(input_dir))
        download_files(input_dir)  # download files to input directory

    output_dir = "Output"  # output directory
    # Create the output directory if it does not already exist.
    if not os.path.exists(output_dir):
        print("Creating directory {}".format(output_dir))
        os.mkdir(output_dir)

    # List of Python dictionaries to be written to submission.yaml file.
    # initial_metadata() contains metadata for the whole submission.
    submission = [initial_metadata()]

    # Counter for the data table number.
    num_tables = 0

    # Write data tables for the low Q2 measurement (main topic of the paper).
    correlation_bins = []
    filenames = [
        "d16-200.table-cs.hInclJet.txt",
        "d16-200.table-cs.hDijet.txt",
        "d16-200.table-cs.hTrijet.txt",
        "d16-200.table-cs.hNormInclJet.txt",
        "d16-200.table-cs.hNormDijet.txt",
        "d16-200.table-cs.hNormTrijet.txt",
    ]
    for input_file in filenames:
        print("Processing {}".format(input_file))
        submission_tables, correlation_bins = write_lowq2_tables(
            input_dir, input_file, output_dir, correlation_bins, num_tables
        )
        submission += submission_tables
        num_tables += len(submission_tables)

    # Write correlation matrices for the low Q2 measurement.
    filenames = ["d16-200.table-rhoij.abs.txt", "d16-200.table-rhoij.norm.txt"]
    for input_file in filenames:
        print("Processing {}".format(input_file))
        submission_table = write_correlation_table(
            input_dir, input_file, output_dir, correlation_bins, num_tables
        )
        submission.append(submission_table)
        num_tables += 1

    # Write data tables for the high Q2 measurement (Tables 12-13 of paper).
    correlation_bins = []
    input_file = "desy16-200.tex"
    print("Processing {}".format(input_file))
    submission_tables, correlation_bins = write_highq2_tables(
        input_dir, input_file, output_dir, correlation_bins, num_tables
    )
    submission += submission_tables
    num_tables += len(submission_tables)

    # Write correlation matrices for the high Q2 measurement.
    filenames = [
        "d16-200.table-rhoij.highQ2.2016.abs.txt",
        "d16-200.table-rhoij.highQ2.2016.norm.txt",
    ]
    for input_file in filenames:
        print("Processing {}".format(input_file))
        submission_table = write_correlation_table(
            input_dir, input_file, output_dir, correlation_bins, num_tables
        )
        submission.append(submission_table)
        num_tables += 1

    # Write data tables for the alpha_s extraction.
    input_file = "d16-200.table-alphas_mur.txt"
    print("Processing {}".format(input_file))
    submission_table = write_alphas_table(
        input_dir, input_file, output_dir, num_tables
    )
    submission.append(submission_table)
    num_tables += 1

    # Write submission.yaml file containing main metadata for all tables.
    submission_file = os.path.join(output_dir, "submission.yaml")
    print("Dumping {}".format(submission_file))
    with open(submission_file, "w") as submission_stream:
        yaml.dump_all(submission, submission_stream, Dumper=Dumper)

    # Write all YAML files and resource files to a .zip file for upload.
    zipfilename = os.path.join(output_dir, "ins1496981.zip")
    print("Creating {}".format(zipfilename))
    write_zipfile(input_dir, output_dir, submission, zipfilename)


def download_files(input_dir):
    """Download the input files to a directory "input_dir"."""

    import requests  # Install with: pip install requests
    from bs4 import BeautifulSoup  # Install with: pip install beautifulsoup4
    from shutil import copy
    import tarfile
    from io import BytesIO

    # Parse the file names from the H1 web page for the paper.
    base_url = "http://www-h1.desy.de"
    req = requests.get(
        base_url
        + "/h1/www/publications/htmlsplit/"
        + "DESY-16-200.long.poster.html"
    )
    soup = BeautifulSoup(req.text, "html.parser")

    # Download the text files containing the data.
    links = [element.get("href") for element in soup.find_all("a")]
    for link in links:
        if link and link.endswith(".txt"):
            req = requests.get(base_url + link)
            txt_filename = os.path.join(input_dir, link.split("/")[-1])
            with open(txt_filename, "w") as txt_file:
                print("Writing {}".format(txt_filename))
                txt_file.write(req.text)

    # Download the image files (and make copies to use as thumbnails).
    images = [element.get("src") for element in soup.find_all("img")]
    for image in images:
        if image.endswith(".gif"):
            req = requests.get(base_url + image)
            gif_filename = os.path.join(input_dir, image.split("/")[-1])
            thumb_filename = os.path.join(
                input_dir, "thumb_" + image.split("/")[-1]
            )
            with open(gif_filename, "wb") as gif_file:
                print("Writing {}".format(gif_filename))
                gif_file.write(req.content)
            copy(gif_filename, thumb_filename)

    # Download the LaTeX source for the paper from the arXiv.
    tar = tarfile.open(
        fileobj=BytesIO(
            requests.get("https://arxiv.org/e-print/1611.03421").content
        )
    )
    for name in tar.getnames():
        if name.endswith(".tex"):
            print("Writing {}/{}".format(input_dir, name))
            tar.extract(name, path=input_dir)


def initial_metadata():
    """Return initial metadata for whole submission as a Python dictionary
    (intended as first YAML document of submission.yaml).
    """

    metadata = {}
    metadata["additional_resources"] = []
    metadata["additional_resources"].append(
        {
            "description": "H1 web page with data points",
            "location": "http://www-h1.desy.de/h1/www/publications/htmlsplit/"
            + "DESY-16-200.long.poster.html",
        }
    )
    metadata["additional_resources"].append(
        {
            "description": "Python script to prepare HEPData submission",
            "location": os.path.basename(__file__),  # this Python script
        }
    )
    return metadata


def write_lowq2_tables(
    input_dir, input_file, output_dir, correlation_bins, num_tables
):
    """Write YAML data tables for a given input text file and return
    the corresponding Python dictionaries for submission.yaml.
    """

    norm = "Norm" in input_file  # switch for normalised cross section

    filename = os.path.join(input_dir, input_file)

    # Read the input file into a Pandas DataFrame, leaving numbers as strings.
    df_str = pd.read_csv(filename, delim_whitespace=True, dtype=str)
    df_str.rename(
        columns={"RW402+": "ModelRW+", "RW402-": "ModelRW-"}, inplace=True
    )  # rename RW402 to ModelRW

    # Define another Pandas DataFrame with numbers converted to ints or floats.
    df_num = pd.read_csv(filename, delim_whitespace=True)
    df_num.rename(
        columns={"RW402+": "ModelRW+", "RW402-": "ModelRW-"}, inplace=True
    )  # rename RW402 to ModelRW

    # Get systematic error labels and make some checks of the summed errors.
    syst_labels = check_errors(df_str, df_num)
    if not syst_labels:
        print("Aborting: problem with errors.")
        exit(-1)

    # Define metadata for this data table.
    keywords = []
    keywords.append({"name": "cmenergies", "values": [319.0]})
    keywords.append(
        {"name": "observables", "values": ["SIG/SIG" if norm else "SIG"]}
    )
    keywords.append(
        {
            "name": "phrases",
            "values": [
                "Inclusive",
                "Double Differential Cross Section",
                "Jet Production",
                "Neutral Current",
                "Deep Inelastic Scattering",
            ],
        }
    )
    additional_resources = []
    if "Trijet" in input_file:
        njet = 3
        variable = r"$\langle P_T \rangle_3$"
        keywords.append(
            {
                "name": "reactions",
                "values": ["E+ P --> E+ .GE.3JET X", "E- P --> E- .GE.3JET X"],
            }
        )
        measurement = "Normalised trijet" if norm else "Trijet"
        table_num = 11 if norm else 8
        figure_num = 19 if norm else 17
    elif "Dijet" in input_file:
        njet = 2
        variable = r"$\langle P_T \rangle_2$"
        keywords.append(
            {
                "name": "reactions",
                "values": ["E+ P --> E+ JETS X", "E- P --> E- JETS X"],
            }
        )
        measurement = "Normalised dijet" if norm else "Dijet"
        table_num = 10 if norm else 7
        figure_num = 15 if norm else 13
    else:
        njet = 1
        variable = r"$P_T^{\rm jet}$"
        keywords.append(
            {
                "name": "reactions",
                "values": ["E+ P --> E+ JET(S) X", "E- P --> E- JET(S) X"],
            }
        )
        measurement = "Normalised inclusive jet" if norm else "Inclusive jet"
        table_num = 9 if norm else 6
        figure_num = 11 if norm else 8
    location = "Table {}, Figure {}".format(table_num, figure_num)
    additional_resources.append(
        {
            "description": "Figure {} from paper".format(figure_num),
            "location": "d16-200f{}.gif".format(figure_num),
        }
    )
    additional_resources.append(
        {
            "description": "Thumbnail Figure {} from paper".format(figure_num),
            "location": "thumb_d16-200f{}.gif".format(figure_num),
        }
    )
    additional_resources.append(
        {"description": "Original text file", "location": input_file}
    )

    submission_tables = []  # list of Python dictionaries to be returned

    # Iterate over each Q2 bin, writing a separate data table for each one.
    q2mins = df_str.q2min.unique()
    q2maxs = df_str.q2max.unique()
    for iq2, q2min in enumerate(q2mins):
        independent_variables = []
        independent_variables.append(
            {"header": {"name": variable, "units": "GeV"}, "values": []}
        )
        dependent_variables = [{}]
        dependent_variables[0]["header"] = (
            {"name": r"$\sigma/\sigma_{\rm NC}$"}
            if norm
            else {"name": r"$\sigma$", "units": "pb"}
        )
        dependent_variables.append({"header": {"name": r"$c^{\rm had}$"}})
        dependent_variables.append({"header": {"name": r"$c^{\rm rad}$"}})
        for dependent_variable in dependent_variables:
            dependent_variable["values"] = []
            dependent_variable["qualifiers"] = []
            dependent_variable["qualifiers"].append(
                {
                    "name": "$Q^2$",
                    "value": q2mins[iq2] + "-" + q2maxs[iq2],
                    "units": "GeV$^2$",
                }
            )
            dependent_variable["qualifiers"].append(
                {"name": "$y$", "value": "0.2-0.6"}
            )
            dependent_variable["qualifiers"].append(
                {"name": r"$\sqrt{s}$", "value": 319.0, "units": "GeV"}
            )
            dependent_variable["qualifiers"].append(
                {
                    "name": "RE",
                    "value": r"$e^\pm\,p \to "
                    + r"e^\pm\,(\ge {}\,{{\rm jet{}}})\,X$".format(
                        njet, "s" if njet > 1 else ""
                    ),
                }
            )
            dependent_variable["qualifiers"].append(
                {"name": r"$\eta_{\rm lab}^{\rm jet}$", "value": "-1.0-2.5"}
            )
            dependent_variable["qualifiers"].append(
                {"name": r"$P_T^{\rm jet}$", "value": "> 4", "units": "GeV"}
            )
            dependent_variable["qualifiers"].append(
                {"name": r"$N_{\rm jet}$", "value": r"$\ge {}$".format(njet)}
            )
            dependent_variable["qualifiers"].append(
                {
                    "name": r"{}".format(variable),
                    "value": "{}-{}".format(
                        df_num.Pt_min.min(), df_num.Pt_max.max()
                    ),
                    "units": "GeV",
                }
            )
        # Iterate over each P_T bin.
        for ipt, pt_min in enumerate(df_str.Pt_min.unique()):
            row = df_str[
                (df_str.q2min == q2min) & (df_str.Pt_min == pt_min)
            ].iloc[0]
            # Save the independent variable value.
            independent_variables[0]["values"].append(
                {"low": float(row["Pt_min"]), "high": float(row["Pt_max"])}
            )
            if norm:
                # Save the bin values, used later in the correlation matrix.
                # Avoid LaTeX encoding to reduce MathJax typesetting.
                correlation_bins.append(
                    "{} = {} {}, {} = {}-{} {}".format(
                        dependent_variables[0]["qualifiers"][0]["name"].strip(
                            "$"
                        ),
                        dependent_variables[0]["qualifiers"][0]["value"],
                        dependent_variables[0]["qualifiers"][0][
                            "units"
                        ].replace("$", ""),
                        independent_variables[0]["header"]["name"]
                        .strip("$")
                        .replace(r"\rm ", "")
                        .replace(r"\langle ", "<")
                        .replace(r" \rangle", ">"),
                        row["Pt_min"],
                        row["Pt_max"],
                        independent_variables[0]["header"]["units"],
                    )
                )
            # Save the cross-section value and the statistical error.
            dependent_variables[0]["values"].append(
                {
                    "value": row["Sigma"],
                    "errors": [
                        {"symerror": row["stat(%)"] + "%", "label": "stat"}
                    ],
                }
            )
            # Iterate over the individual systematic errors.
            for syst in syst_labels:
                if row[syst + "+"] == "0.00" and row[syst + "-"] == "-0.00":
                    # Skip systematic errors that are zero.
                    continue
                elif row[syst + "+"] == row[syst + "-"].replace("-", ""):
                    # Save a symmetric error (without a sign).
                    dependent_variables[0]["values"][ipt]["errors"].append(
                        {"symerror": row[syst + "+"] + "%", "label": syst}
                    )
                else:
                    # Save an asymmetric error (including the sign).
                    dependent_variables[0]["values"][ipt]["errors"].append(
                        {
                            "asymerror": {
                                "plus": row[syst + "+"] + "%",
                                "minus": row[syst + "-"] + "%",
                            },
                            "label": syst,
                        }
                    )
            # Save the correction factor on the theoretical cross section.
            dependent_variables[1]["values"].append(
                {
                    "value": row["HadCorr"],
                    "errors": [{"symerror": row["HadErr"] + "%"}],
                }
            )
            # Save the radiative correction factor.
            dependent_variables[2]["values"].append({"value": row["RadCorr"]})

        # Write independent_variables and dependent_variables to a YAML file.
        data_document = {
            "independent_variables": independent_variables,
            "dependent_variables": dependent_variables,
        }
        data_file = "data{}.yaml".format(num_tables + iq2 + 1)
        print("Dumping {}".format(os.path.join(output_dir, data_file)))
        with open(os.path.join(output_dir, data_file), "w") as data_stream:
            yaml.dump(data_document, data_stream, Dumper=Dumper)

        # Define more metadata for this data table specific to this Q2 bin.
        name = "{}s for $Q^2$ = {} GeV$^2$".format(
            measurement, dependent_variables[0]["qualifiers"][0]["value"]
        )
        description = "{} cross sections measured ".format(measurement)
        description += "as a function of {} for $Q^2$ = {} GeV$^2$.".format(
            variable, dependent_variables[0]["qualifiers"][0]["value"]
        )
        description += "  The correction factors on the theoretical cross "
        description += r"sections $c^{\rm had}$ are listed together with their"
        description += " uncertainties.  The radiative correction factors "
        description += r"$c^{\rm rad}$ are already included in the quoted "
        description += "cross sections.  "
        description += "Note that the uncertainties labelled "
        description += r"$\delta^{E_{e^\prime}}$ and "
        description += r"$\delta^{\theta_{e^\prime}}$"
        description += " in Table {} of the paper ".format(table_num)
        description += "(arXiv:1611.03421v3) should be swapped."
        description += "  See Table 5 of arXiv:1406.4709v2 for "
        description += "details of the correlation model."

        # Append a Python dictionary to the list of submission tables.
        submission_tables.append(
            {
                "name": name,
                "description": description,
                "keywords": keywords,
                "data_file": data_file,
                "location": location,
                "additional_resources": additional_resources,
            }
        )

    return submission_tables, correlation_bins


def check_errors(df_str, df_num):
    """Check that the calculated total errors roughly agree with those
    stored in the input text file.  Return the systematic error labels.
    """

    # Some (not all) symmetric errors have the "-" error without an explicit
    # minus sign.  If this is the case, insert an explicit minus sign.
    syst_labels = []
    for column in df_str.columns:
        if column.endswith("+"):
            column_minus = column[:-1] + "-"
            if column_minus in df_str:
                syst_labels.append(column[:-1])
                if df_str[column].equals(df_str[column_minus]):
                    df_str[column_minus] = "-" + df_str[column_minus]
                    df_num[column_minus] = -df_num[column_minus]

    # Calculate the sum of all systematic errors added in quadrature.
    df_num["calc_syst+"] = 0.0
    df_num["calc_syst-"] = 0.0
    df_num["zeros"] = 0.0
    for syst in syst_labels:
        df_num["calc_syst+"] += (
            df_num[[syst + "+", syst + "-", "zeros"]].max(axis=1) ** 2
        )
        df_num["calc_syst-"] += (
            df_num[[syst + "+", syst + "-", "zeros"]].min(axis=1) ** 2
        )
    df_num["calc_syst+"] = df_num["calc_syst+"] ** 0.5
    df_num["calc_syst-"] = -df_num["calc_syst-"] ** 0.5

    # Also add the statistical error in quadrature to get a total error.
    df_num["calc_tot+"] = (
        df_num["stat(%)"] ** 2 + df_num["calc_syst+"] ** 2
    ) ** 0.5
    df_num["calc_tot-"] = (
        -(df_num["stat(%)"] ** 2 + df_num["calc_syst-"] ** 2) ** 0.5
    )

    # Define the ratio of the calculated errors to those from the input file.
    df_num["ratio_syst+"] = df_num["calc_syst+"] / df_num["syst+(%)"]
    df_num["ratio_syst-"] = df_num["calc_syst-"] / df_num["syst-(%)"]
    df_num["ratio_tot+"] = df_num["calc_tot+"] / df_num["tot+(%)"]
    df_num["ratio_tot-"] = df_num["calc_tot-"] / df_num["tot-(%)"]

    # Check that all these ratios are in the range from 0.9 to 1.1.
    # Print out the calculated error, the stored error, and the ratio.
    print(df_num[["calc_syst+", "syst+(%)", "ratio_syst+"]])
    if not (df_num["ratio_syst+"].between(0.9, 1.1)).all():
        return []
    print(df_num[["calc_syst-", "syst-(%)", "ratio_syst-"]])
    if not (df_num["ratio_syst-"].between(0.9, 1.1)).all():
        return []
    print(df_num[["calc_tot+", "tot+(%)", "ratio_tot+"]])
    if not (df_num["ratio_tot+"].between(0.9, 1.1)).all():
        return []
    print(df_num[["calc_tot-", "tot-(%)", "ratio_tot-"]])
    if not (df_num["ratio_tot-"].between(0.9, 1.1)).all():
        return []

    return syst_labels


def write_correlation_table(
    input_dir, input_file, output_dir, correlation_bins, num_tables
):
    """Write YAML correlation table and return the
    corresponding Python dictionary for submission.yaml.
    """

    norm = "norm" in input_file  # switch for normalised cross section
    highq2 = "highQ2" in input_file  # switch for high-Q2 data

    filename = os.path.join(input_dir, input_file)

    # Read the input file into a Pandas DataFrame, with each line as a row.
    df_str = pd.read_csv(filename, names=["line"])

    # Create two independent variables, specifying the bins.
    independent_variables = []
    independent_variables.append({"header": {"name": "Bin"}, "values": []})
    independent_variables.append({"header": {"name": "Bin"}, "values": []})

    # Create one dependent variable, specifying the correlation coefficients.
    dependent_variables = []
    dependent_variables.append(
        {"header": {"name": "Correlation coefficient"}, "values": []}
    )
    dependent_variables[0]["qualifiers"] = []
    dependent_variables[0]["qualifiers"].append(
        {
            "name": "$Q^2$",
            "value": "150-15000" if highq2 else "5.5-80.0",
            "units": "GeV$^2$",
        }
    )
    dependent_variables[0]["qualifiers"].append(
        {"name": "$y$", "value": "0.2-0.6"}
    )
    dependent_variables[0]["qualifiers"].append(
        {"name": r"$\sqrt{s}$", "value": 319.0, "units": "GeV"}
    )
    dependent_variables[0]["qualifiers"].append(
        {
            "name": "RE",
            "value": r"$e^\pm\,p \to e^\pm\,(\ge \{1, 2, 3\}\,{\rm jets})\,X$",
        }
    )
    dependent_variables[0]["qualifiers"].append(
        {"name": r"$N_{\rm jet}$", "value": r"$\ge \{1, 2, 3\}$"}
    )
    dependent_variables[0]["qualifiers"].append(
        {"name": r"$\eta_{\rm lab}^{\rm jet}$", "value": "-1.0-2.5"}
    )
    dependent_variables[0]["qualifiers"].append(
        {
            "name": r"$P_T^{\rm jet}$",
            "value": "5.0-50.0" if highq2 else "> 4",
            "units": "GeV",
        }
    )

    # Iterate over each row of the Pandas DataFrame.
    for index_i, row in df_str.iterrows():
        elements = row["line"].split()  # split the row on whitespace
        for index_j, element in enumerate(elements):
            independent_variables[0]["values"].append(
                {"value": correlation_bins[index_i]}
            )
            independent_variables[1]["values"].append(
                {"value": correlation_bins[index_j]}
            )
            dependent_variables[0]["values"].append({"value": element})

    # Write independent_variables and dependent_variables to a YAML file.
    data_document = {
        "independent_variables": independent_variables,
        "dependent_variables": dependent_variables,
    }
    data_file = "data{}.yaml".format(num_tables + 1)
    print("Dumping {}".format(os.path.join(output_dir, data_file)))
    with open(os.path.join(output_dir, data_file), "w") as data_stream:
        yaml.dump(data_document, data_stream, Dumper=Dumper)

    # Define metadata for this data table such as keywords.

    keywords = []
    keywords.append({"name": "cmenergies", "values": [319.0]})
    keywords.append(
        {"name": "observables", "values": ["SIG/SIG" if norm else "SIG"]}
    )
    keywords.append(
        {
            "name": "phrases",
            "values": [
                "Inclusive",
                "Double Differential Cross Section",
                "Jet Production",
                "Neutral Current",
                "Deep Inelastic Scattering",
            ],
        }
    )
    keywords.append(
        {
            "name": "reactions",
            "values": [
                "E+ P --> E+ JET(S) X",
                "E- P --> E- JET(S) X",
                "E+ P --> E+ JETS X",
                "E- P --> E- JETS X",
                "E+ P --> E+ .GE.3JET X",
                "E- P --> E- .GE.3JET X",
            ],
        }
    )

    figure_num = 7 if norm is False and highq2 is False else 0
    location = "Figure {}".format(figure_num) if figure_num else ""
    additional_resources = []
    if figure_num:
        additional_resources.append(
            {
                "description": "Figure {} from paper".format(figure_num),
                "location": "d16-200f{}.gif".format(figure_num),
            }
        )
        additional_resources.append(
            {
                "description": "Thumbnail Figure {} from paper".format(
                    figure_num
                ),
                "location": "thumb_d16-200f{}.gif".format(figure_num),
            }
        )
    additional_resources.append(
        {"description": "Original text file", "location": input_file}
    )

    name = "Correlations for " + "{}jets at {} $Q^2$".format(
        "normalised " if norm else "", "high" if highq2 else "low"
    )

    description = (
        "Matrix of statistical correlation coefficients of the "
        + "unfolded {}jet cross sections at {} $Q^2$.".format(
            "normalised " if norm else "", "high" if highq2 else "low"
        )
    )
    if highq2:
        description += (
            r"  The statistical correlations have "
            + "been determined in the scope of the analysis of an "
            + 'earlier H1 publication (<a href="'
            + 'https://inspirehep.net/record/1301218">INSPIRE</a>'
            + ', <a href="https://www.hepdata.net/record/'
            + 'ins1301218">HEPData</a>).'
        )

    # Define the Python dictionary with metadata to be returned.
    submission_table = {
        "name": name,
        "description": description,
        "keywords": keywords,
        "data_file": data_file,
        "additional_resources": additional_resources,
    }
    if location:
        submission_table["location"] = location

    return submission_table


def write_highq2_tables(
    input_dir, input_file, output_dir, correlation_bins, num_tables
):
    """Write YAML data tables for high Q2 data from LaTeX source file and
    return the corresponding Python dictionary for submission.yaml.
    """

    # Read the lines of the LaTeX source file.
    filename = os.path.join(input_dir, input_file)
    with open(filename, "r") as texfile:
        lines = texfile.readlines()

    inside_table = False  # variable specifying if inside relevant lines
    lines_abs = []  # numerical data points of Table 12
    lines_norm = []  # numerical data points of Table 13

    # Iterate over lines of the LaTeX source file.
    for line in lines:
        if "High-Q2 INCLUSIVE JETS" in line:  # trigger to start
            inside_table = True
        elif r"\label{tab:NormIncJetHQ}" in line:  # trigger to finish
            inside_table = False
        if inside_table:
            line = line.strip()  # remove whitespace from either side
            if line and line[0].isdigit():
                # First character of trimmed line is a digit.
                # Remove unnecessary characters from line to extract numbers.
                line = line.replace("--", " ").replace("10^", "e")
                line = line.replace("&", " ").replace("_", " ")
                line = line.replace("+ ", "+").replace(r"\,", "")
                line = re.sub(r"[^\d+-. ]", "", line).split()
                if len(line) == 20:  # Table 12
                    lines_abs.append(line)
                elif len(line) == 17:  # Table 13
                    lines_norm.append(line)
                else:
                    print("Error: len(line) = {}".format(len(line)))
                    break

    submission_tables = []  # list of Python dictionaries to be returned

    # Iterate over unnormalised and normalised cross sections.
    for norm in [False, True]:

        # Define metadata for this data table such as keywords.
        keywords = []
        keywords.append({"name": "cmenergies", "values": [319.0]})
        keywords.append(
            {
                "name": "phrases",
                "values": [
                    "Inclusive",
                    "Double Differential Cross Section",
                    "Jet Production",
                    "Neutral Current",
                    "Deep Inelastic Scattering",
                ],
            }
        )
        keywords.append(
            {
                "name": "reactions",
                "values": ["E+ P --> E+ JET(S) X", "E- P --> E- JET(S) X"],
            }
        )
        keywords.append(
            {"name": "observables", "values": ["SIG/SIG" if norm else "SIG"]}
        )
        table_num = 13 if norm else 12
        figure_num = 11 if norm else 8
        location = "Table {}, Figure {}".format(table_num, figure_num)
        additional_resources = []
        additional_resources.append(
            {
                "description": "Figure {} from paper".format(figure_num),
                "location": "d16-200f{}.gif".format(figure_num),
            }
        )
        additional_resources.append(
            {
                "description": "Thumbnail Figure {} from paper".format(
                    figure_num
                ),
                "location": "thumb_d16-200f{}.gif".format(figure_num),
            }
        )
        additional_resources.append(
            {"description": "Original text file", "location": input_file}
        )

        # Define the independent variables and dependent variables.
        independent_variables = [
            {"header": {"name": "$Q^2$", "units": "GeV$^2$"}, "values": []}
        ]
        dependent_variables = [{}]
        dependent_variables[0]["header"] = (
            {"name": r"$\sigma/\sigma_{\rm NC}$"}
            if norm
            else {"name": r"$\sigma$", "units": "pb"}
        )
        dependent_variables.append({"header": {"name": r"$c^{\rm had}$"}})
        if not norm:
            dependent_variables.append({"header": {"name": r"$c^{\rm ew}$"}})
        for dependent_variable in dependent_variables:
            dependent_variable["values"] = []
            dependent_variable["qualifiers"] = []
            dependent_variable["qualifiers"].append(
                {"name": "$Q^2$", "value": "150-15000", "units": "GeV$^2$"}
            )
            dependent_variable["qualifiers"].append(
                {"name": "$y$", "value": "0.2-0.6"}
            )
            dependent_variable["qualifiers"].append(
                {"name": r"$\sqrt{s}$", "value": 319.0, "units": "GeV"}
            )
            dependent_variable["qualifiers"].append(
                {
                    "name": "RE",
                    "value": r"$e^\pm\,p \to e^\pm\,(\ge 1\,{\rm jet{}})\,X$",
                }
            )
            dependent_variable["qualifiers"].append(
                {"name": r"$\eta_{\rm lab}^{\rm jet}$", "value": "-1.0-2.5"}
            )
            dependent_variable["qualifiers"].append(
                {"name": r"$N_{\rm jet}$", "value": r"$\ge 1$"}
            )
            dependent_variable["qualifiers"].append(
                {
                    "name": r"$P_T^{\rm jet}$",
                    "value": "5.0-7.0",
                    "units": "GeV",
                }
            )

        # Specify the lines and systematic error labels for this data table.
        lines = lines_norm if norm else lines_abs
        syst_labels = [
            "JES",
            "RCES",
            r"$E_{e^\prime}$",
            r"$\theta_{e^\prime}$",
        ]
        if not norm:
            syst_labels.append("ID(e)")

        q2lo = []
        q2hi = []

        # Iterate over the table lines, corresponding to the Q2 bins.
        for iq2, line in enumerate(lines):
            q2lo.append(line[0])
            q2hi.append(line[1])
            independent_variables[0]["values"].append(
                {"low": float(line[0]), "high": float(line[1])}
            )
            dependent_variables[0]["values"].append(
                {
                    "value": float(line[2] + "e" + line[3]),
                    "errors": [{"symerror": line[4] + "%", "label": "stat"}],
                }
            )

            # Need to write the "Model" uncertainty as an asymmetric error.
            model_p = line[6]
            if model_p[0].isdigit():
                model_p = "+" + model_p
                model_m = "-" + line[6]
            elif model_p[0] == "+":
                model_m = model_p.replace("+", "-")
            elif model_p[0] == "-":
                model_m = model_p.replace("-", "+")
            dependent_variables[0]["values"][iq2]["errors"].append(
                {
                    "asymerror": {
                        "plus": model_p + "%",
                        "minus": model_m + "%",
                    },
                    "label": "Model",
                }
            )

            # Sum individual systematic errors in quadrature as a check.
            syst_p = max(float(model_p), float(model_m), 0.0) ** 2
            syst_m = min(float(model_p), float(model_m), 0.0) ** 2

            # Iterate over the other systematic errors.
            for isyst, syst in enumerate(syst_labels):
                dependent_variables[0]["values"][iq2]["errors"].append(
                    {
                        "asymerror": {
                            "plus": line[7 + 2 * isyst] + "%",
                            "minus": line[8 + 2 * isyst] + "%",
                        },
                        "label": syst,
                    }
                )
                syst_p += (
                    max(
                        float(line[7 + 2 * isyst]),
                        float(line[8 + 2 * isyst]),
                        0.0,
                    )
                    ** 2
                )
                syst_m += (
                    min(
                        float(line[7 + 2 * isyst]),
                        float(line[8 + 2 * isyst]),
                        0.0,
                    )
                    ** 2
                )
            dependent_variables[0]["values"][iq2]["errors"].append(
                {"symerror": "0.5%", "label": "LArNoise"}
            )
            syst_p += 0.5 ** 2
            syst_m += 0.5 ** 2
            if not norm:
                dependent_variables[0]["values"][iq2]["errors"].append(
                    {"symerror": "2.5%", "label": "Norm"}
                )
                syst_p += 2.5 ** 2
                syst_m += 2.5 ** 2
            syst_p = syst_p ** 0.5
            syst_m = syst_m ** 0.5

            # Compare the calculated total systematic error with that given.
            print(
                "Table {}, Q2 bin {}, sys = {}, cf. ".format(
                    table_num, iq2 + 1, line[5]
                )
                + "calculated +{:.1f},-{:.1f}".format(syst_p, syst_m)
            )

            # Write hadronisation correction factor as a dependent variable.
            dependent_variables[1]["values"].append(
                {
                    "value": line[15 if norm else 17],
                    "errors": [{"symerror": line[16 if norm else 18] + "%"}],
                }
            )
            if not norm:
                # Write correction factor for electroweak effects.
                dependent_variables[2]["values"].append({"value": line[19]})

        # Write independent_variables and dependent_variables to a YAML file.
        data_document = {
            "independent_variables": independent_variables,
            "dependent_variables": dependent_variables,
        }
        data_file = "data{}.yaml".format(num_tables + (2 if norm else 1))
        print("Dumping {}".format(os.path.join(output_dir, data_file)))
        with open(os.path.join(output_dir, data_file), "w") as data_stream:
            yaml.dump(data_document, data_stream, Dumper=Dumper)

        # Define more metadata for this data table.
        measurement = "Normalised inclusive jet" if norm else "Inclusive jet"
        name = r"{}s for $Q^2$ = {} GeV$^2$".format(
            measurement, dependent_variables[0]["qualifiers"][0]["value"]
        )
        description = (
            r"{} cross sections for $P_T^{{\rm jet}}$ = 5-7 ".format(
                measurement
            )
            + "GeV$^2$ measured as a "
            + "function of $Q^2$ in the range {} GeV$^2$.  ".format(
                dependent_variables[0]["qualifiers"][0]["value"]
            )
        )
        description += (
            r"The cross section values and uncertainties have "
            + "been determined in the scope of the analysis of an "
            + 'earlier H1 publication (<a href="'
            + 'https://inspirehep.net/record/1301218">INSPIRE</a>'
            + ', <a href="https://www.hepdata.net/record/'
            + 'ins1301218">HEPData</a>).'
        )
        description += "  See Table 5 of arXiv:1406.4709v2 for "
        description += "details of the correlation model."

        # Append a Python dictionary to the list of submission tables.
        submission_tables.append(
            {
                "name": name,
                "description": description,
                "keywords": keywords,
                "data_file": data_file,
                "location": location,
                "additional_resources": additional_resources,
            }
        )

    # Store the bin values, used later in the correlation matrix.
    # These need to be inferred from the previous paper (arXiv:1406.4709).
    # Avoid LaTeX encoding to reduce MathJax typesetting when loading page.
    ptlo = ["5", "7", "11", "18", "30"]
    pthi = ["7", "11", "18", "30", "50"]
    for variable in ["P_T^{jet}", "<P_T>_2", "<P_T>_3"]:
        for iq2, _ in enumerate(q2lo):
            for ipt, _ in enumerate(ptlo):
                if ipt == 0 and variable != "P_T^{jet}":
                    continue
                elif ipt == 4 and variable == "<P_T>_3":
                    continue
                correlation_bins.append(
                    "Q^2 = {}-{} GeV^2, {} = {}-{} GeV".format(
                        q2lo[iq2], q2hi[iq2], variable, ptlo[ipt], pthi[ipt]
                    )
                )

    return submission_tables, correlation_bins


def write_alphas_table(input_dir, input_file, output_dir, num_tables):
    """Write YAML data table for strong coupling values and return
    the corresponding Python dictionary for submission.yaml.
    """

    from numpy import roll

    filename = os.path.join(input_dir, input_file)

    # Read the input file into a Pandas DataFrame, leaving numbers as strings.
    # Ignore the first 18 lines, taking the column headers from line 19.
    df_str = pd.read_csv(filename, delim_whitespace=True, dtype=str, header=18)

    # Shift columns to get rid of first header "#" .
    df_str.columns = roll(df_str.columns, len(df_str.columns) - 1)
    df_str.dropna(how="all", axis=1, inplace=True)

    # Create one independent variable and two dependent variables.
    independent_variables = []
    independent_variables.append(
        {"header": {"name": r"$\mu_r$", "units": "GeV"}, "values": []}
    )
    dependent_variables = []
    dependent_variables.append(
        {"header": {"name": r"$\alpha_s(M_Z)$"}, "values": []}
    )
    dependent_variables.append(
        {"header": {"name": r"$\alpha_s(\mu_r)$"}, "values": []}
    )

    # Iterate over each row of the Pandas DataFrame.
    for index, row in df_str.iterrows():
        independent_variables[0]["values"].append({"value": row["mu_r"]})
        dependent_variables[0]["values"].append(
            {"value": row["alpha_s(MZ)"], "errors": []}
        )
        dependent_variables[0]["values"][index]["errors"].append(
            {"symerror": row["exp(MZ)"], "label": "exp"}
        )
        dependent_variables[0]["values"][index]["errors"].append(
            {
                "asymerror": {
                    "plus": row["theoup(MZ)"],
                    "minus": "-" + row["theodn(MZ)"],
                },
                "label": "th",
            }
        )
        dependent_variables[1]["values"].append(
            {"value": row["alpha_s(mur)"], "errors": []}
        )
        dependent_variables[1]["values"][index]["errors"].append(
            {"symerror": row["exp(mur)"], "label": "exp"}
        )
        dependent_variables[1]["values"][index]["errors"].append(
            {
                "asymerror": {
                    "plus": row["theoup(mur)"],
                    "minus": "-" + row["theodn(mur)"],
                },
                "label": "th",
            }
        )

    # Write independent_variables and dependent_variables to a YAML file.
    data_document = {
        "independent_variables": independent_variables,
        "dependent_variables": dependent_variables,
    }
    data_file = "data{}.yaml".format(num_tables + 1)
    print("Dumping {}".format(os.path.join(output_dir, data_file)))
    with open(os.path.join(output_dir, data_file), "w") as data_stream:
        yaml.dump(data_document, data_stream, Dumper=Dumper)

    # Define metadata for this data table such as keywords.

    keywords = []
    keywords.append({"name": "cmenergies", "values": [319.0]})
    keywords.append({"name": "observables", "values": ["ALPHAS"]})
    keywords.append(
        {
            "name": "phrases",
            "values": [
                "Strong Coupling",
                "Jet Production",
                "Neutral Current",
                "Deep Inelastic Scattering",
            ],
        }
    )
    keywords.append(
        {
            "name": "reactions",
            "values": [
                "E+ P --> E+ JET(S) X",
                "E- P --> E- JET(S) X",
                "E+ P --> E+ JETS X",
                "E- P --> E- JETS X",
                "E+ P --> E+ .GE.3JET X",
                "E- P --> E- .GE.3JET X",
            ],
        }
    )

    table_num = 14
    figure_num = 21
    location = "Table {}, Figure {}".format(table_num, figure_num)
    additional_resources = []
    additional_resources.append(
        {
            "description": "Figure {} from paper".format(figure_num),
            "location": "d16-200f{}.gif".format(figure_num),
        }
    )
    additional_resources.append(
        {
            "description": "Thumbnail Figure {} from paper".format(figure_num),
            "location": "thumb_d16-200f{}.gif".format(figure_num),
        }
    )
    additional_resources.append(
        {"description": "Original text file", "location": input_file}
    )
    name = "Strong coupling values"
    description = (
        "The strong coupling extracted from the normalised "
        + "inclusive jet, dijet and trijet data at NLO as a "
        + r"function of the renormalisation scale $\mu_r$.  For "
        + r"each $\mu_r$ the values of the strong coupling "
        + r"$\alpha_s(\mu_r)$ and the equivalent values "
        + r"$\alpha_s(M_Z)$ are given with experimental (exp) and "
        + "theoretical (th) uncertainties."
    )

    # Define the Python dictionary with metadata to be returned.
    submission_table = {
        "name": name,
        "description": description,
        "keywords": keywords,
        "data_file": data_file,
        "additional_resources": additional_resources,
        "location": location,
    }

    return submission_table


def write_zipfile(input_dir, output_dir, submission, zipfilename):
    """Write all YAML files and resource files to a .zip file for upload."""

    # Get a list of files (possible duplicates) to be added to the .zip file.
    zipfiles = []
    for yamlfile in os.listdir(output_dir):
        if yamlfile.endswith(".yaml"):
            zipfiles.append(os.path.join(output_dir, yamlfile))
    for submission_table in submission:
        for resource in submission_table["additional_resources"]:
            location = resource["location"]
            if location == os.path.basename(__file__):
                zipfiles.append(__file__)  # this Python script
            elif not location.startswith("http"):
                zipfiles.append(os.path.join(input_dir, location))

    # Write all files (excluding duplicates) to the .zip file.
    from zipfile import ZipFile

    with ZipFile(zipfilename, "w") as zip_file:
        for zfile in set(zipfiles):  # use "set" to remove duplicates
            print("Writing {} to {}".format(zfile, zipfilename))
            zip_file.write(zfile, os.path.basename(zfile))


if __name__ == "__main__":
    main()
