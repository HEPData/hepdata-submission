Analyses
========

HEPData provides some level of integration for two analysis frameworks.

.. contents:: :local:

Rivet
-----

HEPData can export data in the `YODA <https://yoda.hepforge.org>`_ format for use in a
`Rivet <https://rivet.hepforge.org>`_ analysis.  The list of `Rivet analyses
<https://rivet.hepforge.org/analyses.html>`_ (in `JSON format <https://rivet.hepforge.org/analyses.json>`_) is parsed
nightly and links are made from relevant HEPData records under "View Analyses".  Badges are also added to search results
and to the publication information of a record shown in the left panel.  A search query
`analysis:rivet <https://www.hepdata.net/search?q=analysis:rivet>`_ can be used to find HEPData records that have an
associated Rivet analysis.

A link to a Rivet analysis can manually be added to a record at the upload stage via the ``additional_resources``
of the first document of the ``submission.yaml`` file if the Rivet analysis is already released, for example,

.. code-block:: yaml

   additional_resources:
   - {location: 'https://rivet.hepforge.org/analyses/ATLAS_2016_I1424838', description: 'Rivet analysis'}

But this should not be necessary and it is not recommended, since the Rivet analysis will anyway be picked up by the
nightly harvesting after the HEPData record has been made public.

If a HEPData record has an associated Rivet analysis, then the Rivet analysis name (for example,
``ATLAS_2016_I1424838``) will appear in the YODA download.  Otherwise, if the HEPData record has an attached
INSPIRE ID, a guess is made for the Rivet analysis name using the collaboration name ("ATLAS"), the creation year
of the INSPIRE record ("2016"), and the INSPIRE ID ("1424838").  If the HEPData record has neither an associated
Rivet analysis or an INSPIRE ID, a placeholder ``RIVET_ANALYSIS_NAME`` will be written in the YODA download.
It is possible to override the automatic Rivet analysis name by passing an extra URL argument for the YODA download.
This can be done for either of the two download URL formats:

1. Copy the download link and append the Rivet analysis name (``/ATLAS_2016_I1424838``) at the end after ``/yoda``, e.g.
   https://www.hepdata.net/download/submission/ins1424838/1/yoda/ATLAS_2016_I1424838

2. Add ``?format=yoda&rivet=ATLAS_2016_I1424838`` to the normal record URL, e.g.
   https://www.hepdata.net/record/ins1424838?format=yoda&rivet=ATLAS_2016_I1424838

Similarly, an explicit Rivet analysis name can be passed when downloading individual tables in the YODA format.

The Rivet identifier (e.g. ``d01-x01-y01``) written in the path of the YODA file is generated from the table number
(``d01``) and the index of the dependent variable within a table (``y01``), while ``x01`` always takes the same value.
The Rivet analysis should preferably be written using the same numbering scheme, but if this is not possible, a custom
Rivet identifier can be specified as a qualifier for a particular dependent variable and subsequently used in the YODA
conversion:

.. code-block:: yaml

   qualifiers:
   - {name: 'Custom Rivet identifier', value: 'd01-x01-y01'}


pyhf
----

HEPData provides similar highlighting of additional resource files corresponding to statistical models provided in the
HistFactory JSON (`pyhf <https://pyhf.readthedocs.io>`_) format.  Multiple HistFactory JSON files should preferably
be packaged in an archive file (``.zip``, ``.tar``, ``.tar.gz``, ``.tgz``, ``.tar.xz``) together with an explanatory
README file.  However, a single ``.json`` file can also be uploaded.  HistFactory JSON files are identified by the
``description`` of the additional resource file containing one of a number of case-insensitive trigger words
(``histfactory``, ``pyhf``, ``likelihoods``, ``workspaces``).  To avoid relying on trigger words, a
``type: HistFactory`` field (case-insensitive) can be added to the ``additional_resources`` of the first document of
the ``submission.yaml`` file, for example,

.. code-block:: yaml

   additional_resources:
   - location: "Likelihoods.tar.gz"
     description: "Archive of full likelihoods in the HistFactory JSON format"
     type: "HistFactory" # (optional) currently supports 'HistFactory' type to allow HistFactory JSON (pyhf) files to be highlighted

Links are made from relevant HEPData records with attached HistFactory JSON files under "View Analyses".  Badges are
also added to search results and to the publication information of a record shown in the left panel.  A search query
`analysis:HistFactory <https://www.hepdata.net/search?q=analysis:HistFactory>`_ can be used to find HEPData records
that have associated HistFactory JSON files.

HEPData makes no checks of the formatting of the HistFactory JSON files.  In case of questions, please contact either
experts within your experiment or the pyhf developers.