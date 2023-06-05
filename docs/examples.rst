Examples
========

The `examples <https://github.com/HEPData/hepdata-submission/tree/main/examples>`_
directory contains a few example submissions, including the
:download:`TestHEPSubmission.zip <../examples/submission/TestHEPSubmission.zip>` file.
You can also easily obtain the YAML format of any existing
`HEPData <https://www.hepdata.net>`_ record by clicking "Download All" then "YAML"
or "YAML with resource files".

Note that libraries exist for a variety of programming languages that
can parse and emit the YAML standard, linked from the
`YAML <http://yaml.org>`_ homepage.  Use of these libraries is often
easier than trying to write YAML "by hand", where you need to be careful
with the indentation and spacing, whether or not strings need to be quoted, etc.

In particular, data structures in `Python <https://www.python.org>`_ can
easily be dumped to YAML using libraries like
`PyYAML <https://pyyaml.org>`_.  Here is a
:download:`simple example script <../examples/BELLE_2017_I1512299/1512299.py>`
showing how to process a
:download:`YODA file <../examples/BELLE_2017_I1512299/BELLE_2017_I1512299.yoda>`
into :download:`YAML files <../examples/BELLE_2017_I1512299/1512299.zip>`
for HEPData submission.  Here is a
:download:`more complicated example script <../examples/DESY-16-200/process_ins1496981.py>`
that downloads text files from an experiment web page and processes them into an
:download:`archive file <../examples/DESY-16-200/ins1496981.zip>` ready for
HEPData submission.

The `hepdata-validator <https://github.com/HEPData/hepdata-validator>`_
package provides a ``hepdata-validate`` command to validate a local archive file
(`.zip`, `.tar`, `.tar.gz`, `.tgz`), directory or :doc:`single YAML file <single_yaml>`.
See the `hepdata-validator docs <https://hepdata-validator.readthedocs.io/en/latest/>`_
for more details.

A library called `hepdata_lib <https://github.com/HEPData/hepdata_lib>`_
(see `hepdata-lib docs <https://hepdata-lib.readthedocs.io>`_) has been developed
independently by members of the CMS Collaboration to help with both
(i) reading data into Python from common formats such as
`ROOT <https://root.cern.ch>`_ and text files, and (ii) writing data
from Python into the HEPData YAML submission format.
Simple example scripts using the `hepdata_lib <https://github.com/HEPData/hepdata_lib>`_ library can be found in the
`APEX_ins923960 <https://github.com/HEPData/hepdata-submission/tree/main/examples/APEX_ins923960>`_ and
`ATLAS_ins1241574 <https://github.com/HEPData/hepdata-submission/tree/main/examples/ATLAS_ins1241574>`_ directories.

An `alternative library <https://gitlab.com/cholmcc/hepdata>`_
(see `(py)HEPData docs <https://cholmcc.gitlab.io/hepdata/>`_) with similar functionality
to `hepdata_lib <https://github.com/HEPData/hepdata_lib>`_ has been developed by Christian Holm Christensen.
