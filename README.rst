PyFGCZ
======

*BioBeamer* helps to collect vast amounts of instrument data (M|G|TBytes).
An example configuration collecting mass spectrometric measurement of more
then a dozen devices can be seen through
http://fgcz-ms.uzh.ch/config/BioBeamer.xml.

*FCC* is a minimalistic workflow engine.
The specification/properties of the program are as follow:

- converting instrument files, e.g., RAW-files to all kinds of formats

- being generic

- follows FGCZ hierarch storage granularity: project, user, instrument, time range

- multi-platform, host, task

- configurable through XML file which means new converter by new tag in XML file NO CODE CHANGE!

- stdout and errout through Syslog

A current configuration can be found through http://fgcz-ms.uzh.ch/config/fcc_config.xml.



.. highlight:: sh
::
    fcc_run_linux.py --ncpu 1 --hostname fgcz-s-021 --output __runme.bash --exec --loop

.. highlight:: none
  
See also
--------

- https://github.com/fgcz/BioBeamer

- https://github.com/fgcz/fcc 


References
----------

*FCC - An automated rule-based processing tool for life science data*,
Simon Barkow-Oesterreicher, Can Türker and Christian Panse,
Source Code for Biology and Medicine20138:3 `DOI: 10.1186/1751-0473-8-3`__.

__ http://dx.doi.org/10.1186%2F1751-0473-8-3

