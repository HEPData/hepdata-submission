Analyses
========

HEPData provides some level of integration for eight analysis frameworks: :ref:`Rivet<Rivet section>`,
:ref:`MadAnalysis 5<MadAnalysis 5 section>`, :ref:`SModelS<SModelS section>`, :ref:`CheckMATE<CheckMATE section>`,
:ref:`HackAnalysis<HackAnalysis section>`, :ref:`Combine<Combine section>`,
:ref:`pyhf<pyhf section>` and :ref:`NUISANCE<NUISANCE section>`.  For the first six, :ref:`Rivet<Rivet section>`,
:ref:`MadAnalysis 5<MadAnalysis 5 section>`, :ref:`SModelS<SModelS section>`, :ref:`CheckMATE<CheckMATE section>`,
:ref:`HackAnalysis<HackAnalysis section>` and :ref:`Combine<Combine section>`,
the analysis code is
hosted externally, while for the latter two, :ref:`pyhf<pyhf section>` and :ref:`NUISANCE<NUISANCE section>`, files are
stored as additional resources in HEPData itself.  In each case, links are made from relevant HEPData records under
"View Analyses".  Badges are also added to search results and to the publication information of a record shown in the
left panel.

Externally hosted analyses are exposed to HEPData via an :ref:`analyses JSON file<analysesJSON section>`.
For these, a bulk subscription feature means that analysis framework authors can receive automatic HEPData record update notifications if they desire.
Contact `info@hepdata.net <mailto:info@hepdata.net>`_ to request bulk subscription.

.. contents:: :local:

.. _Tools section:

Analyses tools
++++++++++++++

.. _Rivet section:

Rivet
-----

HEPData can export data in the `YODA <https://yoda.hepforge.org>`_ format for use in a `Rivet
<https://rivet.hepforge.org>`_ analysis.  The list of `Rivet analyses <https://rivet.hepforge.org/analyses.html>`_ (in
`JSON format <https://cedar-tools.web.cern.ch/rivet/analyses.json>`_) is parsed nightly.  A search query
`analysis:rivet <https://www.hepdata.net/search?q=analysis:rivet>`_ can be used to find HEPData records that have an
associated Rivet analysis.

A link to a Rivet analysis can manually be added to a record at the upload stage via the ``additional_resources``
of the first document of the ``submission.yaml`` file if the Rivet analysis is already released, for example,

.. code-block:: yaml

   additional_resources:
   - {location: 'http://rivet.hepforge.org/analyses/ATLAS_2016_I1424838', description: 'Rivet analysis'}

But this should not be necessary and it is **not recommended**, since the Rivet analysis will anyway be picked up by the
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

Similarly, an explicit Rivet analysis name can be passed when downloading individual *tables* in the YODA format.

The Rivet identifier (e.g. ``d01-x01-y01``) written in the path of the YODA file is generated from the table number
(``d01``) and the index of the dependent variable within a table (``y01``), while ``x01`` always takes the same value.
The Rivet analysis should preferably be written using the same numbering scheme, but if this is not possible, a custom
Rivet identifier can be specified as a qualifier for a particular dependent variable and subsequently used in the YODA
conversion:

.. code-block:: yaml

   qualifiers:
   - {name: 'Custom Rivet identifier', value: 'd01-x01-y01'}


.. _MadAnalysis 5 section:

MadAnalysis 5
-------------

Similarly to the Rivet case, a list of `MadAnalysis 5 analyses
<https://madanalysis.irmp.ucl.ac.be/wiki/PublicAnalysisDatabase#AvailableAnalyses>`_ (as `JSON
<https://madanalysis.irmp.ucl.ac.be/attachment/wiki/MA5SandBox/analyses.json>`_) is parsed nightly.  A search query
`analysis:MadAnalysis <https://www.hepdata.net/search?q=analysis:MadAnalysis>`_ can be used to find HEPData records
that have an associated MadAnalysis 5 analysis.


.. _SModelS section:

SModelS
-------

Similarly to the Rivet and MadAnalysis 5 cases, a list of `SModelS analyses
<https://smodels.github.io/docs/ListOfAnalyses>`_ (`as JSON
<https://smodels.github.io/docs/smodels-analyses.hepdata.json>`_) is parsed nightly.  A search query
`analysis:SModelS <https://www.hepdata.net/search?q=analysis:SModelS>`_ can be used to find HEPData records
that have an associated SModelS analysis.


.. _CheckMATE section:

CheckMATE
---------

Similarly to the Rivet, MadAnalysis 5 and SModelS cases, a list of `CheckMATE <https://checkmate.hepforge.org>`_
analyses (`in JSON format <https://checkmate.hepforge.org/AnalysesList/analyses.json>`_) is parsed nightly.  A search
query `analysis:CheckMATE <https://www.hepdata.net/search?q=analysis:CheckMATE>`_ can be used to find HEPData records
that have an associated CheckMATE analysis.


.. _HackAnalysis section:

HackAnalysis
------------

Similarly to the Rivet, MadAnalysis 5, SModelS and CheckMATE cases, a list of `HackAnalysis
<https://goodsell.pages.in2p3.fr/hackanalysis/>`_ analyses
`(in JSON format) <https://goodsell.pages.in2p3.fr/hackanalysis/json/HackAnalysis_HEPData.json>`_ is parsed nightly.  A
search query `analysis:HackAnalysis <https://www.hepdata.net/search?q=analysis:HackAnalysis>`_ can be used to find
HEPData records that have an associated HackAnalysis analysis.


.. _Combine section:

Combine
-------

Similarly to the Rivet, MadAnalysis 5, SModelS, CheckMATE and HackAnalysis cases, a list of `CMS statistical models
<https://repository.cern/communities/cms-statistical-models>`_ in the `Combine
<https://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/>`_ format is parsed nightly via a
`simplified JSON file <https://cms-public-likelihoods-list.web.cern.ch>`_.  A search query
`analysis:Combine <https://www.hepdata.net/search?q=analysis:Combine>`_ can be used to find HEPData records
that have associated statistical models in the ``Combine`` format.


.. _pyhf section:

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

If using the ``hepdata_lib`` package, pass ``file_type = "HistFactory"`` to the `add_additional_resource`_ function.
Links are made from relevant HEPData records (after finalisation) with attached HistFactory JSON files under
"View Analyses".  A search query `analysis:HistFactory <https://www.hepdata.net/search?q=analysis:HistFactory>`_
can be used to find HEPData records that have associated HistFactory JSON files.

HEPData makes no checks of the formatting of the HistFactory JSON files.  In case of questions, please contact either
experts within your experiment or the pyhf developers.

.. _`add_additional_resource`: https://hepdata-lib.readthedocs.io/en/latest/source/hepdata_lib.html#hepdata_lib.AdditionalResourceMixin.add_additional_resource


.. _NUISANCE section:

NUISANCE
--------

`NUISANCE <https://nuisance.hepforge.org>`_ is a framework for event generators in neutrino physics that plays a
similar role to Rivet in collider physics.  Analysis code provided as C++ snippets in the
`ProSelecta <https://github.com/NUISANCEMC/ProSelecta>`_ format can be attached to HEPData records as
``additional_resources`` with ``type: ProSelecta``, for example,

.. code-block:: yaml

   additional_resources:
   - location: analysis.cxx
     description: "Selection and projection function examples. Can be executed in the ProSelecta environment v1.0."
     type: ProSelecta

If using the ``hepdata_lib`` package, pass ``file_type = "ProSelecta"`` to the `add_additional_resource`_ function.
Links are made from relevant HEPData records (after finalisation) with attached ProSelecta C++ files under
"View Analyses".  A search query `analysis:NUISANCE <https://www.hepdata.net/search?q=analysis:NUISANCE>`_
can be used to find HEPData records that have associated ProSelecta C++ snippets for use with NUISANCE.

.. _analysesJSON section:

Analyses JSON schema
++++++++++++++++++++

A JSON format was defined which is used by reinterpretation tools to communicate to HEPData which analyses are implemented in that tool and where to find the implementations such that this information is *Findable* on HEPData.
The current standard is version 1.0.0, usage of the previous standard is deprecated at this point.

The goals of v1.0.0 are

- **Self-descriptiveness**: the JSON format includes information about the tool and tool version it's valid for as well as basic information of the analyses implemented in the tool. It also allows tools to include very rough human-readable information instead of just bare identifiers.

- **Standardisation**: a common standard for everyone ensures easy exchange and *Findability* of information.

- **Future-proofness**: the standard aims to foresee future needs such that it doesn't require frequent updates.

- **Redundancy reduction**: the JSON format allows to codify URLs such that the URL stem doesn't have to be repeated. This makes it more compact, better human-readable and better maintainable.

A JSON file exposed by a tool to HEPData could look as follows

.. code-block:: JSON

   {
      "schema_version": "1.0.0",
      "tool": "SModelS",
      "version": "3.0.0",
      "date_created": "2018-11-13T20:20:39+00:00",
      "implementations_description": "SModelS analysis",
      "url_templates": {
         "main_url": "https://github.com/SModelS/smodels-database-release/tree/main/{name}"
      },
      "analyses": [
         {
            "inspire_id": 1795076,
            "implementations": [
               {
                  "name": "ATLAS-EXOT-2018-48",
               }
            ]
         }
      ]
   }

License information can be added if it differs from the default `CC0 <https://creativecommons.org/publicdomain/zero/1.0/legalcode>`_ license mentioned in the HEPData
`Terms of Use <https://www.hepdata.net/terms>`_.
For more details on the standard, see `the HEPData repository <https://github.com/HEPData/hepdata/tree/main/hepdata/templates/analyses_schema/1.0.0>`_!
Contact `info@hepdata.net <mailto:info@hepdata.net>`_ to request being added to the list of supported tools.