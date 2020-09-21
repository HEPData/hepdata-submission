Tips
====

`YAML <http://yaml.org>`_ has its idiosyncrasies, like all input formats.
We attempt to list some common problems here.

**Validate your files offline before uploading.**
  Try pasting your text into an online YAML validator (find several with
  Google) like `YAML Lint <http://www.yamllint.com>`_ .  Or write some code that
  parses YAML using one of the available `libraries <http://yaml.org>`_
  for different languages.

  Even better: install the Python
  `hepdata-validator <https://github.com/HEPData/hepdata-validator>`_
  package which checks that the YAML files match the HEPData
  `schema <https://github.com/HEPData/hepdata-validator/tree/master/hepdata_validator/schemas>`_.
  Then write a script to validate your YAML files offline.  Here is a
  simple :download:`example <../scripts/check.py>` which validates the
  *submission.yaml* file and all data files against the HEPData schema
  if the `hepdata-validator <https://github.com/HEPData/hepdata-validator>`_
  package is installed, otherwise it performs a more basic (but still
  useful) check that the files are valid YAML.

  An :download:`alternative validation script <../scripts/validate.py>` has been written in Python 3
  by Christian Holm Christensen (see `#8 <https://github.com/HEPData/hepdata-submission/issues/8>`_),
  which reimplements (and attempts to improve) the main functionality of the
  `hepdata-validator <https://github.com/HEPData/hepdata-validator>`_ package.

**Escape special characters.**
  Some characters in YAML need to be escaped, otherwise they cause
  errors when parsing.  The two characters that cause most trouble for
  YAML are ``:`` and ``-``.  Other problematic characters are ``{``, ``}``, and
  ``%``.  So if you use these characters in some description string,
  please make sure you put quotes around the whole string.

**Ensure spaces after colons.**
  Another annoyance can be with spacing. ``{symerror:0.4, label:stat}``
  will give you an error.  Change this to ``{symerror: 0.4, label: stat}``
  however and everything will work nicely.

**Use** ``---`` **to separate tables in the submission.yaml file.**
  A line ``---`` separates YAML documents in the same file and is used to
  denote the start of a new table in the *submission.yaml* file.  But
  don't end the *submission.yaml* file with ``---`` otherwise a final
  (empty) table will be created, which might cause some problems.

**Optionally include thumbnail images.**
  Thumbnail images of the original figures can be displayed alongside
  the tables as in the example above:

  .. code-block:: yaml

     additional_resources:
     - {description: Image file, location: figFigure8A.png}
     - {description: Thumbnail image file, location: thumb_figFigure8A.png}

  The image files should be included in the submitted archive.  Note
  that thumbnail images need to have a filename beginning with ``thumb_``.

**The table** ``name`` **should not be too lengthy.**
  There are no formal restrictions imposed on the ``name`` of a table,
  other than requiring it to be 64 characters or less.  The
  standard convention is to use "Table 1", "Table 2", etc.  However,
  it might be useful to give more descriptive ``name`` values.  Complex
  table names, in particular, containing special characters, were
  initially not completely supported by the HEPData code.  These
  initial problems should now have been resolved.

**Use only simple HTML in comments and descriptions**
  Limited HTML markup is allowed in the ``comment`` and ``description`` fields,
  as shown in the following table. Disallowed HTML tags will be escaped, and
  disallowed HTML attributes will be removed. In some cases your HTML may not
  appear as expected; in this case please remove any disallowed tags and
  attributes and try again. If you are using < or > signs and they do not
  appear as expected, try escaping them, i.e. replace **<** with ``&lt;`` and
  **>** with ``&gt;``.

.. list-table:: Allowed HTML tags and attributes
   :widths: 50 50
   :header-rows: 1

   * - Tag
     - Allowed attributes
   * - ``a``
     - ``href``, ``title``, ``name``, ``rel``
   * - ``abbr``
     - ``title``
   * - ``acronym``
     - ``title``
   * - ``b``
     -
   * - ``blockquote``
     -
   * - ``br``
     -
   * - ``code``
     -
   * - ``div``
     -
   * - ``em``
     -
   * - ``i``
     -
   * - ``li``
     -
   * - ``ol``
     -
   * - ``p``
     -
   * - ``pre``
     -
   * - ``span``
     -
   * - ``strike``
     -
   * - ``strong``
     -
   * - ``sub``
     -
   * - ``sup``
     -
   * - ``u``
     -
   * - ``ul``
     -
