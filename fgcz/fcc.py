#!/usr/bin/python
# -*- coding: latin1 -*-

# $HeadURL: https://github.com/fgcz/PyFGCZ/fcc.py $
# $Id: fcc.py 7518 2015-05-27 15:20:12Z cpanse $
# $Date: 2015-05-27 17:20:12 +0200 (Wed, 27 May 2015) $
# $Author: cpanse $


# Copyright 2008-2017
# Christian Panse <cp@fgcz.ethz.ch>
# Simon Barkow-Oesterreicher 
# Witold Eryk Wolski <wew@fgcz.ethz.ch>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
NAME
    (f)gcz (c)onverter (c)ontrol

SYNOPSIS
    on Microsoft OS

    on UNIX

    arguments:
    --output writes a batch file to run later manually
    --exec automatically triggers the execution of the generated converter commands
    --loop the FCC automatically restarts after it has finished one crawling round


DESCRIPTION
    fcc is a minimalistic workflow engine.
    The specification/properties of the program are as follow:

    o converting instrument files (e.g. RAW-files) to all kinds of formats
    o being generic
    o follows fgcz granularity: project, user, instrument, time range
    o multi platform, host, task
    o configurable through xml file which means new converter by new tag in xml file NO CODE CHANGE!
    o std and error logging

AUTHOR
    Simon Barkow-Oesterreicher and Christian Panse <cp@fgcz.ethz.ch>

SEE ALSO
    https://github.com/fgcz/fcc
    doi:10.1186/1751-0473-8-3

HISTORY
    2008-10-28 2008 (SB)
    2008-10-29 2008 (CP)
    2008-10-30 (CP) revision 847
    2008-11-01 (CP) revision 863
    2088-11-03 (SB) revision 868; changed svn repo
    2010-08-10 (CP) http://fgcz-svn.uzh.ch/viewvc/fgcz/stable/proteomics/fcc/fcc.py?revision=857&view=markup
    2011-01-07 (CP) http://fgcz-svn.uzh.ch/viewvc/fgcz/stable/proteomics/fcc/fcc.py?revision=1293&view=markup
    2011-01-10 (CP,SB) refactoring fileDetails
    2011-01-11 (CP) reading only one config file
    2011-04-08 (CP)
        added --pattern option; now, e.g., we can run one fcc job for each instrument
        added --looping
    2011-07-16 added worker pool (CP)
    2011-07-21 added hostname setting for simulation run (CP)
    2012-06-07 use python logging module (CP)
    2012-06-08 check if a cmd has already run; do avoid running missconfigured task more than one time (CP)
    2012-06-18 changed from map to map_async (CP)
    2012-06-19 cleaning the code (CP) revision 3423
    2012-06-28 switched to os.walk for the crawler methode (CP)
    2012-12-04 handles dirs as files, e.g. conversion of waters.com instruments raw folders (SB,CP)
    2015-07-07 on github.com
"""
__version__ = "https://github.com/fgcz/PyFGCZ"

import os
import urllib
import signal
import platform
import socket
import subprocess
import shlex
import time
import datetime
import sys
import re
import xml.dom.minidom
import multiprocessing
import logging
import logging.handlers
import hashlib
import yaml


def create_logger(name="fcc", address=("fgcz-ms.uzh.ch", 514)):
    """
    create a logger object
    """
    syslog_handler = logging.handlers.SysLogHandler(address=address)
    formatter = logging.Formatter('%(name)s %(message)s')
    syslog_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(20)
    logger.addHandler(syslog_handler)


    return logger

logger = create_logger()

class FgczCrawl(object):


    def __init__(self, pattern=None, max_time_diff=None):
        """
        """
        self.para = {}

        self.pattern_list = pattern
        if pattern is None:
            self.pattern_list = ['/srv/www/htdocs/Data2San',
                                 'p[0-9]{3,4}',
                                 'Proteomics|Metabolomics',
                                 '(FUSION|G2HD|GCT|ORBI|QEXACTIVE|QEXACTIVEHF|QTOF|QTRAP|T100|TOFTOF|TRIPLETOF|TSQ|VELOS)_[0-9]',
                                 '[a-z]{3,18}_[0-9]{8}(_[-a-zA-Z0-9_]+){0,1}',
                                 '[-a-zA-Z0-9_]+.(raw|RAW|wiff|wiff\.scan)$']

        self.regex_list = map(lambda p: re.compile(p), self.pattern_list)

        self.para['min_time_diff'] = 300
        if not max_time_diff is None:
            self.para['max_time_diff'] = max_time_diff
        else:
            self.para['max_time_diff'] = 60 * 60 * 24 * 7 * 5  # five week
        self.para['min_size'] = 100 * 1024  # 100K Bytes

    def dfs_(self, path, idx):
        res = []

        try:
            file_list = os.listdir(path)
        except:
            print path
            res

        file_list = filter(self.regex_list[idx].match, file_list)

        for f in file_list:
            new_path = os.path.normpath("{0}/{1}".format(path, f))
            if os.path.isdir(new_path) and idx < len(self.regex_list) - 1:
                res = res + self.dfs_(new_path, idx + 1)
            elif os.path.exists(new_path):
                res.append(new_path)

        
        res = filter(lambda f: time.time() - os.path.getmtime(f) > self.para[
                     'min_time_diff'] and time.time() - os.path.getmtime(f) < self.para['max_time_diff'], res)
        res = filter(lambda f: os.path.getsize(f) >
                     self.para['min_size'] or os.path.isdir(f), res)


        return res

    @property
    def run(self):
        """
        traverse file system.

        :return: list of files
        """

        tStart = time.time()
        logger.info("crawling for files ...")
        files = self.dfs_(os.path.normpath(self.pattern_list[0]), 1)
        logger.info("crawling done|time={0:.2f} seconds.".format(time.time() - tStart))
        logger.debug("found {0} files in {1}.".format(len(files), self.pattern_list[0]))

        return files



def signal_handler(signal, frame):
    logger.error("sys exit 1; signal={0}; frame={1}".format(signal, frame))
    sys.exit(1)


def myExecWorker0(cmdLine):
    signal.signal(signal.SIGINT, signal_handler)
    myPid = "-1"
    rcode = "-1"
    try:
        logger.info("exec|cmd='" + str(cmdLine) + "'")
        tStart = time.time()
        p = subprocess.Popen(cmdLine, shell=True)
        myPid = str(p.pid)
        rcode = p.wait()
        tStop = time.time()
        p.terminate()
    except OSError as e:
        logger.warning("exception|pid=" + str(myPid) + "|OSError=" + str(e))
    logger.info(
        "completed|pid=" + str( myPid) + "|time=" + str( tStop - tStart) + "|cmd='" + str( cmdLine) + "'")
    return [cmdLine]


def walkOnError(e):
    logger.error(e)
    print(e)
    sys.exit(1)



def parseConfig(xml):
    """
    parse the XML config data.
    """

    logger.info("parsing xml")
    converterDict = dict()
    rulesList = list()

    for i in xml.getElementsByTagName("converter"):
        converter = dict()
        try:
            # hard constraints
            for a in ("converterID", "converterDir", "converterCmd", "toFileExt"):
                converter[a] = i.attributes[a].value

            # soft constraints
            for a in ("converterOptions", "fromFileExt", "hostname"):
                try:
                    converter[a] = i.attributes[a].value
                except:
                    if a == "fromFileExt":
                        converter[a] = ".RAW"
                    else:
                        converter[a] = ""
            converterDict[converter["converterID"]] = converter
        except:
            logger.debug("skipping one converter config tag {0} ...".format(i))
            continue

    for i in xml.getElementsByTagName("rule"):
        rule = dict()
        try:
            converter = converterDict[i.attributes['converterID'].value]
            for a in ("converterID", "converterDir", "converterCmd", "converterOptions", "toFileExt", "fromFileExt", "hostname"):
                rule[a] = converter[a]

            # hard constraints
            for a in ("project", "omics", "instrument", "user", "beginDate", "endDate", "keyword"):
                rule[a] = i.attributes[a].value

            rulesList.append(rule)
        except:
            logger.debug("skipping rule config tag {0} ...".format(i))
            continue

    return rulesList


def getDetailsFromFilePath(filePath):
    """
    The methode assumes standard FGCZ naming convention, meaning the project, instrument, user, date
    information are included in the path.

    example:
    /p195/Proteomics/LTQ_1/ebrunner_20081028_description/meta_info_for_exp.RAW
    """
    regex = re.compile(
        ".*(p[0-9]+)[\\\\/](Metabolomics|Proteomics)[\\\\/]([A-Z0-9]+_[0-9]+)[\\\\/]([a-z]+)_(20[0-9][0-9][01][0-9][0123][0-9])[-0-9a-zA-Z_\/\.\\\]*(\.[a-zA-Z0-9]+)$")
    fileDetails = dict()

    result = regex.match(filePath)

    if result:
        fileDetails["project"] = result.group(1)
        fileDetails["omics"] = result.group(2)
        fileDetails["instrument"] = result.group(3)
        fileDetails["user"] = result.group(4)
        fileDetails["date"] = result.group(5)
        fileDetails["extension"] = result.group(6)
        fileDetails["filePath"] = filePath
    return fileDetails


def matchFileToRules(fileDetails, rulesList, myHostname = None):
    """
    returns rules that are matched to instrument RAW-files.
    NOTE: date cmp function assumes YYYYMMDD!
    TODO: check if there are *EMPTY* elements in the returned list.
    """
    matchedRules = list()
    if myHostname is None:
        myHostname = str(socket.gethostbyaddr(socket.gethostname())[0].split('.')[0])
    try:
        filename = fileDetails["filePath"]

        if (os.path.isfile(filename) and os.path.getsize(filename) == 0):
            logger.debug("skipping" + filename + "because of file size is 0.")
            return matchedRules

        timediff = time.time() - os.path.getmtime(filename)

        # TODO(cp): should be a variable
        if timediff < 300:
            logger.warning(
                "skipping " + str(
                    filename) + " because of mtime difference=" + str(
                        timediff) + "[sec].")
            return matchedRules
    except:
        return matchedRules

    for rule in rulesList:
        try:
            regex = re.compile(".*{0}.*".format(rule["keyword"]))
            regex2 = re.compile(".*{0}.*".format(rule["converterDir"]))

            if (((fileDetails["project"] == rule["project"]) or ('' == rule["project"])) and
                (fileDetails["omics"] == rule["omics"]) and
                ((fileDetails["instrument"] == rule["instrument"]) or ('' == rule["instrument"])) and
                ((fileDetails["user"] == rule["user"]) or ('' == rule["user"])) and
                (fileDetails["date"] >= rule["beginDate"]) and
                (fileDetails["date"] <= rule["endDate"]) and
                (fileDetails["extension"] == rule["fromFileExt"]) and
                (regex.match(fileDetails["filePath"])) and
                    (re.search(myHostname, rule["hostname"]))):
                if (regex2.match(fileDetails["filePath"])):
                    logger.debug("skipping '" + filename + "' because of recursion warning." + str(
                        rule["converterDir"]) + " is already in the path.")
                    continue
                matchedRules.append(rule)
		# print rule
        except:
            pass
    return matchedRules


def createSystemBatch(fromFileName, toFileName, converter):
    return "{0} {1} {2} {3}".format(converter["converterCmd"],
                                    converter["converterOptions"], fromFileName, toFileName)


def usage():
    pass


class Fcc:
    """
    """
    parameters = {'config_url': "http://fgcz-ms.uzh.ch/config/fcc_config.xml", 'readme_url': "http://fgcz-r-021.uzh.ch/config/fcc_readme.txt",
                 'crawl_pattern': ['/srv/www/htdocs/Data2San/',
                        'p[0-9]{2,4}', 'Metabolomics',
                        '(GCT)_[0-9]',
                        '[a-z]{3,18}_[0-9]{8}(_[-a-zA-Z0-9_]{0,100}){0,1}',
                        '[-a-zA-Z0-9_]+.(raw|RAW|wiff|wiff\.scan)'],
                 'nCPU': 1,
                 'max_time_diff': 60 * 60 * 24 * 7 * 4,
                 'sleepDuration': 300,
                 'loop': False,
                 'exec': False}

    myProcessId = os.getpid()
    parameters['hostname'] = "{0}".format(socket.gethostbyaddr(socket.gethostname())[0].split('.')[0])

    signal.signal(signal.SIGINT, signal_handler)
    myRootDir = None
    myOutputFile = None
    myPattern = ".*"
    matchingRules = list()
    converterOutputs = list()

    # to save MD5 of all considered commandline
    processedCmdMD5Dict = dict()


    def __init__(self):
        logger.info("fcc started ...")
        self.processedCmdMD5Dict = dict()
        print ("using syslog as log.")

    def set_para(self, key, value):
        """ class parameter setting """
        self.parameters[key] = value
        #if key is 'pattern':
        #    self.regex = re.compile(self.parameters['pattern'])


    def read_config(self, url=''):
        """
        reads the xml config file in each iteration to
        manage updated rules of the fcc_config.xml file.
        """

        try:
            logger.info("trying to open '{0}' ... ".format(url))
            config_xml = urllib.urlopen(url).read()

            fccConfigXml = xml.dom.minidom.parseString(config_xml)
            logger.info("read {0} ... ".format(url))
        except:
            logger.error("The XML config file is missing or malformed. Error: ")
            logger.error(sys.exc_info()[1])
            print ("Unexpected error:", sys.exc_info()[1])
            raise

        # TODO(cp): use lxml
        try:
            return(parseConfig(fccConfigXml))
        except:
            logger.error("could not parse xml configuration")
            return None

    """
    write all considered cmds  into a file
    """
    def update_processed_cmd(self, filename = r'C:\FGCZ\fcc\cmds_conducted.yaml'):
        if self.parameters['exec']:
            try:
                os.rename(filename, "{}.bak".format(filename))
            except:
                pass
            with open(filename, "w") as f:
                yaml.dump(self.processedCmdMD5Dict, f, default_flow_style=False)


    def process(self, file):
        """
        computes a match and executes cmd (add to spool dir)
        
        :return:
        """
        # countDict is used for some kind of rule check. TODO(cp):??
        countDict = dict()

        file = os.path.normpath(file)
       
        # logger.info("found: {0}".format(file))
        fileDir = os.path.dirname(file)
        fileDetails = getDetailsFromFilePath(file)

         
        matchingRules = matchFileToRules(fileDetails, self.rulesList, myHostname = self.parameters['hostname'])

        if len(matchingRules) > 0:
            logger.debug(
                "found {0} rules matching rule(s) for file '{1}'.".format(len(matchingRules), file))

        for mrule in matchingRules:
            if mrule is not None:
                converterDir = os.path.normpath(
                    "{0}/{1}".format(fileDir, mrule["converterDir"]))

                """
                create the directory in the python way,
                """
                # if not os.path.exists(converterDir) and self.parameters['exec']:
                if not os.path.exists(converterDir):
                    try:
                        os.mkdir(converterDir)
                    except:
                        logger.error(
                            "mkdir {0} failed.".format(converterDir))
                        raise

                readme_filename = os.path.normpath("{0}/README.txt".format(converterDir))
                readme_content = """
the files contained in this directory have been generated using fcc applying rule #{0}.

more information can be found using the following url:

http://fgcz-data.uzh.ch/config/fcc_config.xml#converterID-{0}

or by contacting Christian Panse <cp@fgcz.ethz.ch>

if you use these files in your publication please cite:
http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3614436/


""".format(mrule["converterID"])

                if os.path.isfile(readme_filename) is False:
                    with open(readme_filename, "w") as readmef:
                        readmef.write(readme_content)

                toFileName = os.path.normpath(
                    "{0}/{1}{2}".format(converterDir,
                                        os.path.splitext(
                                        os.path.basename(file))[0],
                                        mrule["toFileExt"]))

                if not os.path.exists(toFileName):
                    if mrule["project"] in countDict:
                        countDict[mrule["project"]] = countDict[
                            mrule["project"]] + 1
                    else:
                        countDict[mrule["project"]] = 1

                    candCmdLine = createSystemBatch(
                        file, toFileName, mrule)
                    checksum = hashlib.md5()
                    checksum.update(candCmdLine.encode("utf-8"))
                    candCmdLineMD5 = checksum.hexdigest()

                    if not candCmdLineMD5 in self.processedCmdMD5Dict:

                        self.processedCmdMD5Dict[candCmdLineMD5] = candCmdLine
                        self.update_processed_cmd()
                        if self.parameters['exec']:
                            self.pool.map_async(myExecWorker0, [ candCmdLine ],
                                callback=lambda i: logger.info("callback {0}".format(i)))
                            logger.info("added|cmd='{}' to pool".format(candCmdLine))
                    else:
                        # TODO(cp): make this generic working
                        with open("C:\\FGCZ\\fcc\Cmds-problems.txt", "a") as cmdf:
                            cmdf.write("{0}\t{1}\n".format(candCmdLineMD5, candCmdLine))

    def run(self):
        """

        :return:
        """


        crawler = FgczCrawl(pattern=self.parameters['crawl_pattern'], max_time_diff=self.parameters['max_time_diff'])

        if not os.path.exists(os.path.normpath(self.parameters['crawl_pattern'][0])):
            logger.error("{0} does not exsist.".format(self.parameters('crawl_pattern')[0]))
            sys.exit(1)

        if not 'myOutputFile' in self.parameters:
            timegmt = time.gmtime(time.time())
            fmt = '__%Y%m%d-%H%M%S-runme.bat'
            self.parameters['myOutputFile'] = time.strftime(fmt, timegmt)

        """
        This is the part where the compute pool is created to utilize the compute box.
        Note that the executed jobs might run on more than one thread/cpu.
        Simon 20140227 changed nCPUs
        """
        try:
            if self.parameters['exec'] and self.parameters['nCPU'] is None:
                self.parameters['nCPU'] = multiprocessing.cpu_count() - 1


            self.pool = multiprocessing.Pool(processes=self.parameters['ncpu'])
            logger.info("created pool having {0} processes.".format(self.parameters['ncpu']))

        except:
            logger.error("could not create pool.")
            print sys.exc_info()
            sys.exit(1)

        while True:
            self.rulesList = self.read_config(self.parameters['config_url'])
            logger.debug("found {0} rules in {1}".format(len(self.rulesList), self.parameters['config_url']))


            logger.info("computing rule versus file matching ...")
            tStart = time.time()

            """TODO(cp):
            regex = re.compile(myPattern)
            FILES = filter(lambda p: regex.match(p), FILES)
            """
            map(lambda x: self.process(x), crawler.run)

            logger.info("matching done|time={0:.2f} seconds.".format(time.time() - tStart))

            if not self.parameters['exec']:
                with open(self.parameters['myOutputFile'], 'a') as f:
                    map(lambda cmd: f.write("{0}\n".format(self.processedCmdMD5Dict[cmd])), self.processedCmdMD5Dict.keys())

                msg = "wrote {0} lines to file to '{1}'.".format(len(self.processedCmdMD5Dict.keys()),
                                                               self.parameters['myOutputFile'])
                print(msg)
                logger.info(msg)

            if not self.parameters['loop']:
		return

            logger.info("sleeping||for {0} seconds ...".format(self.parameters['sleepDuration']))
            time.sleep(self.parameters['sleepDuration'])

        self.pool.close()
        self.pool.join()


# MAIN
if __name__ == "__main__":
    try:
        import yaml
        fcc = Fcc()
        print yaml.dump(fcc.read_config(url='http://fgcz-data.uzh.ch/config/fcc_config.xml'))
    except:
        print "yaml does not seems to run. exit"
        pass
    
