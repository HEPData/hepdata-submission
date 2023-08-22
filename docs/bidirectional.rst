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

You can find the desired table DOI displayed next to the table name on the relevant HEPData record page.  It is built
from a common prefix (``10.17182/hepdata``), the HEPData record identifier (for example, ``12345`` or ``67890``), the
HEPData record version (``v1``, ``v2``, etc.), and the table number within the HEPData record (``t1``, ``t2``, etc.).

After upload, the ``related_to_table_dois`` field is persisted to the database and rendered above the table description
with links to the related tables.  The linked tables will also display links back to the referring tables, but only
*after* the records containing the referring tables have been finalised.  The ``related_to_table_dois`` field is
*ignored* for uploads to the HEPData Sandbox.

Linking records
---------------

In a similar way, bidirectional links can be made between HEPData records, rather than individual tables, via a new
field ``related_to_hepdata_records`` added to the first YAML document of the ``submission.yaml`` file, for example,
alongside the ``comment`` and ``additional_resources``.  It should be given as a list of HEPData record identifiers:

.. code-block:: yaml

   related_to_hepdata_records:
   - 12345
   - 67890

Note that the HEPData record identifier must be given as an integer (not a string) and it differs from the INSPIRE
record identifier often found after ``ins`` in a HEPData record URL.  You can find the HEPData record identifier from
the integer after the prefix ``10.17182/hepdata`` in the HEPData record DOI displayed alongside the publication
information in the left-hand panel of a HEPData record.

Again, after upload, the ``related_to_hepdata_records`` field is persisted to the database and rendered in the
left-hand panel of a HEPData record with links to the related records.  The linked records will also display links back
to the referring records, but only *after* the referring records have been finalised.  The
``related_to_hepdata_records`` field is *ignored* for uploads to the HEPData Sandbox.