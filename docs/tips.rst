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
  `schema <https://github.com/HEPData/hepdata-validator/tree/main/hepdata_validator/schemas>`_.
  You can then validate a zip, directory or :doc:`single YAML file <single_yaml>`
  using the ``hepdata-validate`` command. See the
  `hepdata-validator docs <https://hepdata-validator.readthedocs.io/en/latest/>`_
  for more details.

  The validator will be run automatically if you create your submission using the
  `hepdata-lib <https://github.com/HEPData/hepdata-lib>`_ package.

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
  If a separate thumbnail image file is not specified, the original image file
  will also be used as the thumbnail image.  Valid image file types that will
  be displayed as thumbnails are ``png``, ``jpeg``, ``jpg``, ``tiff`` or ``gif``,
  but *not* ``pdf``.

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

**Check that your submission is not too large**
  HEPData was designed for interactive visualisation and conversion of mostly tabular data.
  This means that the size of submissions is restricted.  A limit of 50 MB is currently imposed on each uploaded
  archive file.  There is a client-side timeout on each request (such as a file upload) of 298s to avoid the 300s
  server timeout.  Each YAML data file should be less than 10 MB in size.  It should be checked that data tables close
  to this upper limit can be rendered sufficiently quickly in a web browser.  The Uploader should also check that large
  submissions can be converted to other formats (YAML, YODA, ROOT, CSV) within the converter timeout limit of 220s.
  Large data tables can alternatively be provided as ``additional_resources`` attached to either a whole submission or
  to a specific (possibly empty) table.

**Remove unused files from the submission archive**
  The HEPData validation code will check that all files specified via the ``data_file`` and ``additional_resources``
  fields of the ``submission.yaml`` file are included in the uploaded submission archive file.  It will also check that
  there are no included extra files, so it is important when creating the archive file that no hidden system files are
  inadvertently included.  For example, when using the ``tar`` command on macOS, extra files starting with ``._`` can
  be included in the archive file, but this behaviour can be switched off by setting the ``COPYFILE_DISABLE``
  environment variable, for example, ``export COPYFILE_DISABLE=1``.