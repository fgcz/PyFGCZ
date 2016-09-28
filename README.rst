PyFGCZ
======

*BioBeamer* helps to collect huge amounts of instrument data (M|G|TBytes).
An example configuration collecting mass spectrometric measurement of more 
than a dozen devices can be seen through
http://fgcz-data.uzh.ch/config/BioBeamer.xml.

*FCC* is a minimalistic workflow engine.
The specification/properties of the program are as follow:

- converting instrument files, e.g., RAW-files to all kinds of formats

- being generic

- follows FGCZ hierarch storage granularity: project, user, instrument, time range

- multi- platform, host, task

- configurable through xml file which means new converter by new tag in xml file NO CODE CHANGE!

- stdout and errout through syslog 

A current configugration can be found through http://fgcz-data.uzh.ch/config/fcc_config.xml.


See also
--------

- https://github.com/fgcz/BioBeamer

- https://github.com/fgcz/fcc 


References
----------

FCC - An automated rule-based processing tool for life science data,
Simon Barkow-Oesterreicher, Can Türker and Christian Panse,
Source Code for Biology and Medicine20138:3 `DOI: 10.1186/1751-0473-8-3`__.

__ http://dx.doi.org/10.1186%2F1751-0473-8-3

