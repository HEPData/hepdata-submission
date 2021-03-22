#!/usr/bin/env python

"""Python3 script to produce HEPData submission for arXiv:1108.2750.
Code reformatted with "black -l 79" and passes checks by "pylint" and "flake8".
Resulting HEPData record at https://www.hepdata.net/record/ins923960?version=1
"""

# See https://hepdata-lib.readthedocs.io for how to use the "hepdata_lib" tool.
from hepdata_lib import Submission, Variable, Table
from numpy import loadtxt

BINNED_DOI = "10.7484/inspirehep.data.lk95.m2gq"
UNBINNED_DOI = "10.7484/inspirehep.data.ph21.l5rg"

# Define the main Submission object and add a comment.
submission = Submission()

BINNED_DATAFILE = (
    "Input/APEX_Test_Run_Data_eplus_eminus_invariant_mass_2011June30_"
    "binned_0p05_MeV-1.txt"
)
BINNED_DESCRIPTION = (
    "The binned invariant mass spectrum of e+e- pair events in the final "
    "event sample collected by APEX. The data correspond to Figure 3 of the "
    "paper, with the 0.05 MeV binning used for the profile likelihood "
    "analysis. The original plain-text file from "
    f'<a href="https://doi.org/{BINNED_DOI}">{BINNED_DOI}</a> '
    'is accessible by clicking "Resources".'
)

# Read the binned data from a plain-text file.
binned_data = loadtxt(BINNED_DATAFILE, skiprows=1)

# Define an independent variable and construct low and high bin limits.
mass = Variable("m(e+e-)", is_binned=True, is_independent=True, units="MeV")
mass.values = list(zip(binned_data[:, 0] - 0.025, binned_data[:, 0] + 0.025))

# Define a dependent variable from the event counts given in the second column.
count = Variable("count", is_binned=False, is_independent=False)
count.values = list(map(int, binned_data[:, 1]))

# Define a table by the 'mass' and 'count' variables.
binned_table = Table("Figure 3 (binned)")
binned_table.add_variable(mass)
binned_table.add_variable(count)

# Add some metadata to the table.
binned_table.keywords["observables"] = ["N"]
binned_table.keywords["reactions"] = ["E- NUCLEUS --> E+ E- X"]
binned_table.description = BINNED_DESCRIPTION
binned_table.location = "Data from Figure 3 (binned)"

# Add a thumbnail image of the original figure from the paper.
binned_table.add_image("Input/Fig3.pdf")

# Add the original plain-text data file as a resource file.
binned_datafile = BINNED_DATAFILE.split("/")[1]
binned_table.additional_resources.append(
    {"description": binned_datafile, "location": binned_datafile}
)
submission.files_to_copy.append(BINNED_DATAFILE)

# Similarly for the unbinned data.  However, in this case, the numbers cannot
# easily be formatted as a HEPData table, so we just attach the original file.

UNBINNED_DATAFILE = (
    "Input/APEX_Test_Run_Data_eplus_eminus_invariant_mass_MeV_unbinned_"
    "values.txt.gz"
)
UNBINNED_DESCRIPTION = (
    "The unbinned invariant mass spectrum of e+e- pair events in the final "
    "event sample collected by APEX. The original data from "
    f'<a href="https://doi.org/{UNBINNED_DOI}">{UNBINNED_DOI}</a> '
    'are accessible by clicking "Resources".'
)
unbinned_table = Table("Figure 3 (unbinned)")
unbinned_table.description = UNBINNED_DESCRIPTION
unbinned_table.location = "Data from Figure 3 (unbinned)"
unbinned_table.keywords["observables"] = ["N"]
unbinned_table.keywords["reactions"] = ["E- NUCLEUS --> E+ E- X"]
unbinned_datafile = UNBINNED_DATAFILE.split("/")[1]
unbinned_table.additional_resources.append(
    {"description": unbinned_datafile, "location": unbinned_datafile}
)
submission.files_to_copy.append(UNBINNED_DATAFILE)

# Add the two tables to the Submission object.
submission.add_table(binned_table)
submission.add_table(unbinned_table)

# Create the archive file "submission.tar.gz" ready for upload.
submission.create_files("Output")
