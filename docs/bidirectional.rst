Bidirectional linking
=====================

Linking tables
--------------

It is now possible (from 22nd August 2023) to enable bidirectional links between HEPData tables possibly in different
records.  Applications might include linking theoretical predictions or covariance matrices to their related
measurements.  The YAML document specifying the table metadata in the input ``submission.yaml`` file should contain a
new field ``related_to_table_dois`` comprising a list of table DOIs:

.. code-block:: yaml

   related_to_table_dois:
   - 10.17182/hepdata.12345.v1/t2
   - 10.17182/hepdata.67890.v3/t4

**Please note:** This field should not be used for self-referencing, the DOIs inserted should be for OTHER related tables.

You can find the desired table DOI displayed next to the table name on the relevant HEPData record page.  It is built
from a common prefix (``10.17182/hepdata``), the HEPData record identifier (for example, ``12345`` or ``67890``), the
HEPData record version (``v1``, ``v2``, etc.), and the table number within the HEPData record (``t1``, ``t2``, etc.).

After upload, the ``related_to_table_dois`` field is persisted to the database and rendered above the table description
with links to the related tables.  The name of the linked tables will be displayed instead of the DOI, with a tooltip
containing their description displayed when the user hovers over the table name.

The linked tables will also display links back to the referring tables, but only *after* the records containing the
referring tables have been finalised.  The backward link is only displayed if the referring record is the most
recent finalised version.  The ``related_to_table_dois`` field is *ignored* for uploads to the HEPData Sandbox.

An example record is https://www.hepdata.net/record/ins2729396?version=1.  However, note that the links between tables
are automatically *bidirectional* so that, for example, if specifying the ``related_to_table_dois`` field in Table 1
(linked to Table 11), then the ``related_to_table_dois`` field does *not* also need to be specified in Table 11 (linked
to Table 1).  Doing so will result in duplicate links.  Note that a HEPData software `bug`_ currently means that the
links will only be rendered after a record has been finalised.

The `hepdata_lib`_ tool can be used to write the ``related_to_table_dois`` field (see `Adding links to related tables
<https://hepdata-lib.readthedocs.io/en/latest/usage.html#adding-links-to-related-tables>`_).

.. _`bug`: https://github.com/HEPData/hepdata/issues/796
.. _`hepdata_lib`: https://github.com/HEPData/hepdata_lib

Linking records
---------------

In a similar way, bidirectional links can be made between HEPData records, rather than individual tables, via a new
field ``related_to_hepdata_records`` added to the first YAML document of the ``submission.yaml`` file, for example,
alongside the ``comment`` and ``additional_resources``.  It should be given as a list of HEPData record identifiers:

.. code-block:: yaml

   related_to_hepdata_records:
   - 12345
   - 67890

**Please note:** This field should not be used for self-referencing, the IDs inserted should be for OTHER related records.

Note that the HEPData record identifier must be given as an integer (not a string) and it differs from the INSPIRE
record identifier often found after ``ins`` in a HEPData record URL.  You can find the HEPData record identifier from
the integer after the prefix ``10.17182/hepdata`` in the HEPData record DOI displayed alongside the publication
information in the left-hand panel of a HEPData record.

Again, after upload, the ``related_to_hepdata_records`` field is persisted to the database and rendered in the
left-hand panel of a HEPData record with links to the related records.  A tooltip containing the title of the linked
record is displayed when the user hovers over the record identifier.  The linked records will also display links back
to the referring records, but only *after* the referring records have been finalised and if the referring record is the
most recent version.  The ``related_to_hepdata_records`` field is *ignored* for uploads to the HEPData Sandbox.

The `hepdata_lib`_ tool can be used to write the ``related_to_hepdata_records`` field (see `Adding links to related
records <https://hepdata-lib.readthedocs.io/en/latest/usage.html#adding-links-to-related-records>`_).