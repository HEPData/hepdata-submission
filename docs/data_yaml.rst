Data Files
==========

Data files can be encoded as either `YAML <http://yaml.org>`_ or
`JSON <http://www.json.org>`_: the software deals with both the same way.
We define the data file in two parts which describe:

a) the *independent variables* (e.g. the x-axis of a plot);
b) the *dependent variables* (the thing you're measuring, e.g. the y-axis of a plot).

Each table can have any number of independent and dependent variables
(columns), but each must have the same number of data points (rows).
Independent variables consist of a list of values, each of which generally comprises
``low`` and ``high`` bin limits, together with a central ``value``.  However, the
central ``value`` can be omitted if it coincides with the bin midpoint, while the
``low`` and ``high`` bin limits can be omitted if they are not applicable.

It is not possible to give a ``low`` bin limit without a ``high`` bin limit
(or vice versa), but one-sided bin limits are supported by specifying an
infinite bin limit, for example, ``low: -.inf`` for an underflow bin (with
``high`` finite) or ``high: .inf`` for an overflow bin (with ``low`` finite).
These one-sided bins will be written to appropriate underflow/overflow bins in
the ROOT/YODA export.  Note that the presence of an underflow/overflow bin
requires at least one finite bin for the ROOT/YODA export to be successful.

If there are no independent variables, for example, an inclusive cross-section
measurement, an empty list should be specified, ``independent_variables: []``.
Specifying one or more ``independent_variables`` and an empty list for the
``dependent_variables`` is not supported.  An empty table can be given with
``{independent_variables: [], dependent_variables: []}`` if only metadata and
``additional__resources`` are needed for a particular dataset.

Each variable comprises a header (the column name) and a list of values
(the rows in your table).  The header should define the variable
including units unless the variable is dimensionless.
For the dependent variables, you can also
define *qualifiers*.  These are extra metadata describing the
measurement, such as the energy, the reaction type, and possible
kinematic cuts on variables such as transverse momentum and
(pseudo)rapidity.


YAML data file example
----------------------

.. code-block:: yaml

   independent_variables:
   - header: {name: Leading dilepton PT, units: GEV}
     values:
     - {low: 0, high: 60}
     - {low: 60, high: 100}
     - {low: 100, high: 200}
     - {low: 200, high: 600}
   dependent_variables:
   - header: {name: 10**6 * 1/SIG(fiducial) * D(SIG(fiducial))/DPT, units: GEV**-1}
     qualifiers:
     - {name: RE, value: P P --> Z0 < LEPTON+ LEPTON- > Z0 < LEPTON+ LEPTON- > X}
     - {name: SQRT(S), units: GEV, value: 7000}
     values:
     - value: 7000
       errors:
       - {symerror: 1100, label: stat}
       - {symerror: 79, label: 'sys,detector'}
       - {symerror: 15, label: 'sys,background'}
     - value: 9800
       errors:
       - {symerror: 1600, label: stat}
       - {symerror: 75, label: 'sys,detector'}
       - {symerror: 15, label: 'sys,background'}
     - value: 1600
       errors:
       - {symerror: 490, label: stat}
       - {symerror: 41, label: 'sys,detector'}
       - {symerror: 2, label: 'sys,background'}
     - value: 80
       errors:
       - {symerror: 60, label: stat}
       - {symerror: 2, label: 'sys,detector'}
       - {symerror: 0, label: 'sys,background'}


Uncertainties
-------------

Multiple uncertainties can be assigned to each data point, each with
an optional label to distinguish them.  There are two main classes
of uncertainty that can be encoded: symmetric errors and
asymmetric errors.  A symmetric error allows you to specify plus
and minus errors using one value, e.g. ``symerror: 0.4``, while an
asymmetric error allows both plus and minus errors to be explicitly
encoded, e.g. ``asymerror: {plus: 0.4, minus: -0.3}``.  Note that here
"plus" and "minus" can refer to "up" and "down" variations of the
source of uncertainty, and do not necessarily match the sign of the
resultant uncertainty on the measurement (which can change sign along a
distribution).  Note that ``symerror: 0.4`` is equivalent to
``asymerror: {plus: 0.4, minus: -0.4}``.  The opposite-sign case,
``symerror: -0.4`` is equivalent to ``asymerror: {plus: -0.4, minus: 0.4}``.
A one-sided uncertainty can be represented
using an empty string, e.g. ``asymerror: {plus: '', minus: -0.3}``.
Error values are normally taken as absolute, but relative errors
can be specified by including a ``%`` symbol after the number to define
the error as a percentage of the central ``value``.

The `hepdata-validator <https://github.com/HEPData/hepdata-validator>`_ (v0.2.0 or greater)
code will invalidate bins where all uncertainties are zero.  This check was introduced to
avoid `problems <https://gitlab.com/hepcedar/rivet/-/issues/69>`_ in fitting applications.
Bins with zero content should preferably be omitted completely from the HEPData table.
Alternatively, missing bins can be indicated with a non-numeric central value like ``'-'``
or an empty string ``''`` and no uncertainties.  In this case, the ``errors`` key should
either be omitted completely or specified as an empty list ``errors: []``.

Within the context of the
`LHC Electroweak Working Group <https://twiki.cern.ch/twiki/bin/view/LHCPhysics/LHCEW>`_,
it has been proposed (see
`talk <https://indico.cern.ch/event/779259/contributions/3242594/attachments/1770317/2876299/LCorpe_LHCEWWG_Correlations_131218.pdf>`_)
to provide a breakdown of individual uncertainty contributions rather
than a correlation/covariance matrix for systematic uncertainties.
However, a statistical correlation matrix will still be needed.

Note that only ``dependent_variables`` can have ``errors``, not ``independent_variables``.  If you want to express
uncertainty in an independent variable, it can be given ``low`` and ``high`` limits.  But it is often better to instead
encode the variable as a dependent variable with ``errors``, and assign a dummy independent variable like a bin index.
This means that the generated plot may not match the publication plot if the latter plots two dependent
variables against each other.  (It is an open `issue <https://github.com/HEPData/hepdata/issues/212>`_ to provide an
option for such a generated plot.)


Correlation/covariance matrices
-------------------------------

Correlation/covariance matrices can be encoded in a format with two
independent variables (giving the bins) and one dependent variable
(giving the covariance/correlation), e.g.

.. code-block:: yaml

   independent_variables:
   - header: {name: PTjet, units: GeV}
     values:
     - {low: 25, high: 45}
     - {low: 45, high: 65}
     - {low: 45, high: 65}
     ...
   - header: {name: PTjet, units: GeV}
     values:
     - {low: 25, high: 45}
     - {low: 25, high: 45}
     - {low: 45, high: 65}
     ...
   dependent_variables:
   - header: {name: Correlation}
     values:
     - {value: 1.0000}
     - {value: 0.8727}
     - {value: 1.0000}
     ...

The current heatmap visualisation code does not cope well for tables with more than, say, 5000 rows, corresponding to a
correlation/covariance matrix with 50-100 bins (see
`HEPData Forum post <https://hepdata-forum.cern.ch/t/large-correlation-matrix-data-require-excessive-cpu-and-memory-resources-when-browsing/28/1>`_).
A workaround is to provide a large matrix not as a data table, but as ``additional_resources`` attached to either a whole
submission or to a specific (possibly empty) table.


Two-dimensional measurements
----------------------------

Two-dimensional measurements can be encoded in a similar way to
correlation/covariance matrices with two independent variables and one
dependent variable.  For example, suppose we have:

========= ========= =======
ind_var_1 ind_var_2 dep_var
========= ========= =======
x         a         1
y         a         2
x         b         3
y         b         4
========= ========= =======

The YAML encoding would be:

.. code-block:: yaml

   independent_variables:
   - header: {name: ind_var_1}
     values:
     - {value: x}
     - {value: y}
     - {value: x}
     - {value: y}
   - header: {name: ind_var_2}
     values:
     - {value: a}
     - {value: a}
     - {value: b}
     - {value: b}
   dependent_variables:
   - header: {name: dep_var}
     values:
     - {value: 1}
     - {value: 2}
     - {value: 3}
     - {value: 4}

Note that each independent variable must contain the same number of
values as the dependent variable.  The ordering is not important, for
example, we might choose to loop over the second independent variable
before the first:

.. code-block:: yaml

   independent_variables:
   - header: {name: ind_var_1}
     values:
     - {value: x}
     - {value: x}
     - {value: y}
     - {value: y}
   - header: {name: ind_var_2}
     values:
     - {value: a}
     - {value: b}
     - {value: a}
     - {value: b}
   dependent_variables:
   - header: {name: dep_var}
     values:
     - {value: 1}
     - {value: 3}
     - {value: 2}
     - {value: 4}

Such a representation will give a heat map visualisation, while export
to ROOT will use ``TH2F`` and ``TGraph2DErrors`` objects, and export to
YODA will use ``Scatter3D`` objects.

However, often a more appropriate representation is to encode a
two-dimensional measurement in a format with one independent variable
and multiple dependent variables (one for each value of the second
independent variable).  Then export to ROOT will use ``TH1F`` and
``TGraphAsymmErrors`` objects, and export to YODA will use ``Scatter2D``
objects.  For example, the table above could be encoded with the
dependent variable as a function of the first independent variable
(with the second independent variable acting as a qualifier):

.. code-block:: yaml

   independent_variables:
   - header: {name: ind_var_1}
     values:
     - {value: x}
     - {value: y}
   dependent_variables:
   - header: {name: dep_var}
     qualifiers:
     - {name: ind_var_2, value: a}
     values:
     - {value: 1}
     - {value: 2}
   - header: {name: dep_var}
     qualifiers:
     - {name: ind_var_2, value: b}
     values:
     - {value: 3}
     - {value: 4}

or with the dependent variable as a function of the second independent
variable (with the first independent variable acting as a qualifier):

.. code-block:: yaml

   independent_variables:
   - header: {name: ind_var_2}
     values:
     - {value: a}
     - {value: b}
   dependent_variables:
   - header: {name: dep_var}
     qualifiers:
     - {name: ind_var_1, value: x}
     values:
     - {value: 1}
     - {value: 3}
   - header: {name: dep_var}
     qualifiers:
     - {name: ind_var_1, value: y}
     values:
     - {value: 2}
     - {value: 4}