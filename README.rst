
PyFGCZ
======


PyFGCZ contains BioBeamer and FCC python code.

*BioBeamer* helps to collect huge amounts of instrument data (MB/GB/TB).
An example configuration collecting mass spectrometric meassurement of  more than 
devivices can be seen through http://fgcz-data.uzh.ch/config/BioBeamer.xml.

*FCC* is a minimalistic workflow engine.
The specification/properties of the program are as follow:

- converting instrument files (e.g. RAW-files) to all kinds of formats

- being generic

- follows FGCZ hierarch storage granularity: project, user, instrument, time range

- multi- platform, host, task

- configurable through xml file which means new converter by new tag in xml file NO CODE CHANGE!

- stdout and errout through syslog 

A current configugration can be found through http://fgcz-data.uzh.ch/config/fcc_config.xml.

Installation
------------

See also
--------
- https://github.com/fgcz/BioBeamer
- https://github.com/fgcz/fcc

- `DOI: 10.1186/1751-0473-8-3`__.
__ http://dx.doi.org/10.1186%2F1751-0473-8-3






