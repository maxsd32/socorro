==================================
Socorro - Crash ingestion pipeline
==================================

Socorro is a set of components for collecting, processing, and analyzing crash
data. It is used by Mozilla for analyzing crash data for Mozilla products.
Mozilla's crash analysis tool is hosted at
`<https://crash-stats.mozilla.com/>`_.


:Free software: Mozilla Public License version 2.0
:Code: https://github.com/mozilla-services/socorro/ and https://github.com/mozilla-services/antenna
:Documentation: https://socorro.readthedocs.io/
:Documentation: https://crash-stats.mozilla.com/documentation/
:Mailing list: https://lists.mozilla.org/listinfo/tools-socorro
:IRC: `<irc://irc.mozilla.org/breakpad>`_
:New bugs: https://bugzilla.mozilla.org/enter_bug.cgi?format=__standard__&product=Socorro
:View all bugs: https://bugzilla.mozilla.org/buglist.cgi?quicksearch=product%3Asocorro


.. toctree::
   :caption: Crash Stats service
   :numbered:
   :includehidden:
   :maxdepth: 1
   :glob:

   overview
   signaturegeneration
   topcrashersbysignature


Crash Stats site documentation covering API docs, getting access to memory dumps,
and Supersearch is located at `<https://crash-stats.mozilla.com/documentation/>`_.


.. toctree::
   :caption: Developers
   :numbered:
   :includehidden:
   :maxdepth: 1
   :glob:

   localdevenvironment
   contributing
   service/*
   flows/*
   stackwalker
   schemas
   crashstorage/*
   tests/*
   socorro_app
   deploy
   howto
