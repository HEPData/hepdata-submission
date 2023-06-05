Single YAML files
=================

For submissions with no auxiliary files, it is possible to upload a single YAML file rather than
an archive file comprising a ``submission.yaml`` file and multiple YAML data files.
The single-YAML-file format was used for migration from the old HepData site in 2016.
It is identical to the usual ``submission.yaml`` file, but the ``independent_variables``
and ``dependent_variables`` (that would normally be included in a separate YAML data file) are instead
given directly in the relevant YAML document of the ``submission.yaml`` file, replacing the ``data_file`` key in
that YAML document. (Note that the ``name``, ``description`` and ``keywords`` properties must be present in
addition to ``independent_variables`` and ``dependent_variables``.)

Here is an :download:`example single YAML file <../examples/BELLE_2017_I1512299/1512299.yaml>`.
Upon upload, the single-YAML-file format will be split automatically into the usual ``submission.yaml`` file and
multiple YAML data files.