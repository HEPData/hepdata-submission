#!/usr/bin/env python

"""Python3 script to produce HEPData submission for arXiv:1307.1427.
Code reformatted with "black -l 79" and passes checks by "pylint" and "flake8".
Resulting HEPData record at https://www.hepdata.net/record/ins1241574?version=2
"""

# See https://hepdata-lib.readthedocs.io for how to use the "hepdata_lib" tool.
from hepdata_lib import Submission, Variable, Table
from numpy import loadtxt

DOIS = [
    "10.7484/inspirehep.data.a78c.hk44",
    "10.7484/inspirehep.data.rf5p.6m3k",
    "10.7484/inspirehep.data.26b4.ty5f",
]
CHANNELS = ["2ph", "4l", "lvlv"]
FINAL_STATES = [r"\gamma\gamma", r"ZZ^*\to 4\ell", r"WW^*\to\ell\nu\ell\nu"]

# Define the main Submission object and add a comment.
submission = Submission()

for ichannel, channel in enumerate(CHANNELS):

    DATAFILE = f"Input/atlas_prodModes_ggFttH_VBFVH_{channel}.hep.dat"
    ROOTFILE = f"Input/atlas_prodModes_ggFttH_VBFVH_{channel}.root"

    description = (
        r"-2 log Likelihood in the $(\mu^f_{{\mathrm{{ggF}}+ttH}}, "
        r"\mu^f_{{\mathrm{{VBF}}+VH}})$ plane for the $f=H\to "
        rf"{FINAL_STATES[ichannel]}$ channel "
        r"and a Higgs boson mass $m_H = 125.5$ GeV."
    )
    if channel == "4l":
        description += (
            " The sharp lower edge is due to the small number of events "
            "in this channel and the requirement of a positive pdf."
        )
    description += (
        " The original plain-text and ROOT files from "
        f'<a href="https://doi.org/{DOIS[ichannel]}">{DOIS[ichannel]}</a> '
        'are accessible by clicking "Resources".'
    )

    # Read the data from a plain-text file.
    data = loadtxt(DATAFILE, skiprows=6)

    # Define two independent variables.
    mu1 = Variable(
        r"$\mu^f_{{\mathrm{{ggF}}+ttH}}$", is_binned=False, is_independent=True
    )
    mu1.values = list(data[:, 0])
    mu2 = Variable(
        r"$\mu^f_{{\mathrm{{VBF}}+VH}}$", is_binned=False, is_independent=True
    )
    mu2.values = list(data[:, 1])

    # Define a dependent variable.
    likelihood = Variable(
        r"$-2\ln\Lambda$", is_binned=False, is_independent=False
    )
    likelihood.values = list(data[:, 2])
    likelihood.add_qualifier(
        "RE", rf"$p p\to H (\to {FINAL_STATES[ichannel]})\,X$"
    )

    # Define a table by the independent and dependent variables.
    table = Table(f"Figure 7 ({channel})")
    table.add_variable(mu1)
    table.add_variable(mu2)
    table.add_variable(likelihood)

    # Add some metadata to the table.
    table.description = description
    table.location = rf"Data from Figure 7 ($H\to {FINAL_STATES[ichannel]}$)"
    table.keywords["reactions"] = ["P P --> HIGGS X"]
    table.keywords["cmenergies"] = [7000, 8000]
    table.keywords["phrases"] = ["Higgs"]

    # Add a thumbnail image of the original figure from the paper.
    table.add_image("Input/MuTMuW_comb_ggwwllll.pdf")

    # Add the original plain-text and ROOT data files as resource files.
    for path in (DATAFILE, ROOTFILE):
        file = path.split("/")[1]
        table.additional_resources.append(
            {"description": file, "location": file}
        )
        submission.files_to_copy.append(path)

    # Add the table to the Submission object.
    submission.add_table(table)

# Add the v1 tarball containing HTML-formatted data migrated from old HepData.
RESOURCE_DESCRIPTION = (
    "ins1241574_resources.tar.gz (unpack then view insert.html)"
)
RESOURCE_LOCATION = "Input/ins1241574_resources.tar.gz"
submission.add_additional_resource(
    RESOURCE_DESCRIPTION, RESOURCE_LOCATION, copy_file=True
)

# Create the archive file "submission.tar.gz" ready for upload.
submission.create_files("Output")
