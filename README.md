# BioBeamer
Collecting instrument data using BioBeamer

[![Project Stats](https://www.openhub.net/p/BioBeamer/widgets/project_thin_badge.gif)](https://www.openhub.net/p/BioBeamer)


## Install 
* ensure you have python 2.7.* 
* ```pip install lxml==3.4.2``` or newer
* ```git clone git@github.com:fgcz/BioBeamer.git```

## Configure 

### BioBeamer xml configuration file

```xml
<?xml-stylesheet type="text/xsl" href="BioBeamer.xsl"?>
<BioBeamerHosts>
<host name="fgcz-i-180" 
    instrument="TRIPLETOF_1"
    min_size="1024" 
    min_time_diff="10800" 
    max_time_diff="2419200" 
    simulate='false' 
    func_target_mapping="map_data_analyst_tripletof1" 
    robocopy_args="/E /Z /NP /R:0 /LOG+:C:\\Progra~1\\BioBeamer\\robocopy.log"
    pattern=".+" 
    source_path="D:/Analyst Data/Projects/" 
    target_path="\\130.60.81.21\\Data2San">
    <b-fabric>
        <applicationID>93</applicationID>
    </b-fabric>
</host>
</BioBeamerHosts>
```

the xml can be validated using
```bash
xmllint --noout --schema BioBeamer.xsd BioBeamer.xml
```
or 
```bash
xmlstarlet val --xsd BioBeamer.xsd BioBeamer.xml
```

### Deploy @ new location
* change syslog host
* change configuration url

### Configure Syslog '/etc/rsyslog.conf' 

```syslog
$template tplremote,"%timegenerated% %HOSTNAME% %fromhost-ip% %syslogtag%%msg:::drop-last-lf%\n"
$template RemoteHost,"/var/log/remote/%HOSTNAME%_%fromhost-ip%.log"

if ($fromhost-ip != '127.0.0.1') then ?RemoteHost;tplremote  
& ~
```

### Configure logrotate '/etc/logrotate.d/remote'
```conf
/var/log/remote/*
{
        rotate 13
        monthly
        missingok
        notifempty
        compress
}
```

## Run

### @ FGCZ
just 'run as administrator' justBeamFiles.exe.

justBeamFiles.exe is an [autoitscript](https://www.autoitscript.com/site/autoit/).
In our case the justBeamFiles.exe maps the storage and runs the fgcz_biobeamer.py script which uses robocopy.exe on Micorsoft installed PCs to sync the files.

### otherwise
* ensure that SAN is mounted 
```cmd
python BioBeamer.py
```

## BioBeamer class
![BioBeamer UML](/images/classes_No_Name.png)


## Author
[Christian Panse](http://www.fgcz.ch/the-center/people/panse.html) :rocket:

## See also
* [fgcz-intranet wiki page](http://fgcz-intranet.uzh.ch/tiki-index.php?page=BioBeamer)
* [FGCZ configuration](http://fgcz-data.uzh.ch/config/BioBeamer.xml)

## TODO
* munin plugin





# FCC - [FGCZ](http://www.fgcz.ethz.ch) Converter Control

## Description
FCC is a minimalistic workflow engine.
The specification/properties of the program are as follow:
- converting instrument files (e.g. RAW-files) to all kinds of formats
- being generic
- follows FGCZ hierarch storage granularity: project, user, instrument, time range
- multi- platform, host, task
- configurable through xml file which means new converter by new tag in xml file NO CODE CHANGE!
- stdout and errout through syslog 

## Synopsis
## on Microsoft OS
```
c:\Python27\python.exe fcc_run_windows.py --output __runme.bat --ncpu 2 --exec
```

### on UNIX

```sh
# use python 2.7.x
$ python fcc_run_linux.py --hostname fgcz-s-021 --output out-20150824.bash --ncpu 1 --exec --loop
```
### Arguments:

- `--output <file>` writes a batch file to run later manually
- `--exec` automatically triggers the execution of the generated converter commands
- `--loop` the FCC automatically restarts after it has finished one crawling round
- `--ncpu` number of jobs should be used
- `--hostname <host configuration>` tells fcc which host configuration should be used.


## Authors

Simon Barkow-Oesterreicher <simon@uberchord.com> and Christian Panse <cp@fgcz.ethz.ch>
    
#maintainer

<cp@fgcz.ethz.ch>


## Configuration

[the current FCGZ configuration can be found here.](http://fgcz-data.uzh.ch/config/fcc_config.xml)

```xml
 <controllerRuleSet>
    <rule converterID='000' 
    project='p103' 
    omics='Proteomics' 
    user='' instrument='ORBI_2' 
    beginDate='20080901' 
    endDate='20990101' 
    keyword="iTRAQ">
    </rule>
</controllerRuleSet>
    
<converterList>
    <converter converterID='000' 
    converterDir= 'mgf__low_res_MS2_iTRAQ' 
    converterCmd='cscript "C:\FGCZ\fgcz-proteomics\stage\mascot_distiller\fgczRaw2Mgf.vbs"'         converterOptions='"C:\FGCZ\fgcz-proteomics\stage\generalRawFileConverterRobot\MascotDistillerOPTs\Orbitrap_low_res_MS2_iTRAQ.opt"' 
    toFileExt='.mgf' 
    hostname='fgcz-s-034'> 
    </converter>
</converterList>
```

## TODO
- provide cmd argv for log file name
- unit test - no glue how to do that 
- ensure that no process is killed by CTRL-C. add a `pool wait` at the right position on the code when CTRL-C is pressed or give at least a warning.
- write a  pid file to ensure that only one fcc is running


## See also 

- FCC - An automated rule-based processing tool for life science data.
Barkow-Oesterreicher S1, Türker C, Panse C. Source Code Biol Med. 2013 Jan 11;8(1):3.  [doi:10.1186/1751-0473-8-3](http://www.scfbm.org/content/8/1/3/abstract), [PMC3614436](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3614436/),
PMID: 23311610
- [FCC configuration @ FGCZ](http://fgcz-data.uzh.ch/config/fcc_config.xml)


