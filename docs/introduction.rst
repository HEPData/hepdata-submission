Introduction
============

`HEPData <https://www.hepdata.net>`_ submission will largely involve the
upload of archive files (``.zip``, ``.tar``, ``.tar.gz``, ``.tgz``)
containing a number of
`YAML <http://yaml.org>`_ files together with possible auxiliary files
of any format.  However, it is also possible to upload a single text
file with extension ``.oldhepdata`` (see
:download:`sample.oldhepdata <../examples/oldhepdata/sample.oldhepdata>`) containing
the "input" format that was used for data submissions from the old
HepData site.  Upon upload, the ``.oldhepdata`` file will be automatically
`converted <https://github.com/HEPData/hepdata-converter>`_ to the new
YAML format.  Basic introductions to YAML can easily be found via
`Google <https://www.google.com/search?q=YAML>`_, for example,
`Wikipedia <https://en.wikipedia.org/wiki/YAML>`_ or
`Learn X in Y minutes <https://learnxinyminutes.com/docs/yaml/>`_.

The main file for a submission is the *submission.yaml* file.
This links together all the data tables into one submission and
specifies auxiliary files such as scripts used to
create the data, ROOT files, or even links to GitHub/Bitbucket/Zenodo
etc. for more substantial pieces of code.

Publication information such as the paper title, authors and abstract,
or the journal reference and DOI, is pulled from the corresponding
`INSPIRE <http://inspirehep.net>`_ record, therefore it does not need
to be included in the *submission.yaml* file.  The publication
information is added to the HEPData record when a Coordinator first
attaches the INSPIRE ID, and it is updated when a HEPData record is
finalised by a Coordinator.  In future, we will try to automatically
update publication information from INSPIRE even after a HEPData
record has been finalised (see
`HEPData/hepdata#100 <https://github.com/HEPData/hepdata/issues/100>`_).
For now, a command can be run on the server to update publication
information for a given HEPData record; contact info@hepdata.net.

The data files for each table, in either `YAML <http://yaml.org>`_ or
`JSON <http://www.json.org>`_ format, specify the data points in terms of
independent and dependent variables.

See also Section 6 of
`arXiv:1704.05473 <https://arxiv.org/abs/1704.05473>`_ for an overview of
the submission process.

.. image:: ../assets/hepdata_root_processing.png