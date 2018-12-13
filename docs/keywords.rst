Keywords
========

Current keywords are ``cmenergies`` (in units of GeV),
``observables``, ``phrases``, and ``reactions``.  Individual keywords can be
omitted if they are not relevant.  Each keyword is associated with a
list of possibly multiple values, e.g.

.. code-block:: yaml

   keywords: # used for searching, possibly multiple values for each keyword
   - {name: reactions, values: [P P --> Z0 Z0 X]}
   - {name: observables, values: [SIG]}
   - {name: cmenergies, values: [7000.0]}
   - {name: phrases, values: [Inclusive, Integrated Cross Section, Cross Section, Proton-Proton Scattering, Z Production, Z pair Production]}

Each *reaction* should consist of initial- and final-state particles
separated by ``-->``, with particles on each side of the arrow separated
by spaces.  The right-hand side should usually have an ``X`` to
indicate an inclusive reaction (as opposed to exclusive where all
final-state particles are known, e.g. elastic proton scattering).  A
standard :doc:`notation <keywords/partlist>` should be used for each
particle.  Omit the decay products or give them as a separate reaction.

Each *observable* should consist of only a single word, for example,
use ``SIG`` for a cross section, ``DSIG/DPT`` for a differential cross
section, ``N`` for number of events, etc., again using a standard
:doc:`notation <keywords/observables>`.

Each *phrase* should be preferably be selected from a :doc:`list <keywords/phrases>`.

Note that the linked lists of :doc:`particles <keywords/partlist>`,
:doc:`observables <keywords/observables>` and :doc:`phrases <keywords/phrases>` were
created a few years ago from the old HepData site and may not be relevant.  Assigning
keywords unique to a particular HEPData record is of little value, therefore keywords
should be omitted if in doubt.  It is an open issue
(`HEPData/hepdata#60 <https://github.com/HEPData/hepdata/issues/60>`_) to make it
easier to select keywords by developing appropriate software.