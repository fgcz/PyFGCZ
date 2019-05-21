
#!/usr/bin/python
# -*- coding: latin1 -*-

"""
Copyright 2006-2019 Functional Genomics Center Zurich

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
Author / Maintainer: Christian Panse <cp@fgcz.ethz.ch>, Witold E. Wolski <wew@fgcz.ethz.ch>
"""

from fgcz import biobeamer
import socket
import time

if __name__ == "__main__":
    configuration_url = "http://fgcz-ms.uzh.ch/config/"
    print ("hostname is {0}.".format(socket.gethostname()))
    bio_beamer = biobeamer.Robocopy()
    biobeamer_xsd = "{0}/BioBeamer.xsd".format(configuration_url)
    biobeamer_xml = "{0}/BioBeamer.xml".format(configuration_url)

    bio_beamer.para_from_url(xsd=biobeamer_xsd, xml=biobeamer_xml)
                     
    bio_beamer.run()
    
    time.sleep(5)
    
    BBChecker = Checker()
    BBChecker.para_from_url(xsd=biobeamer_xsd,
                            xml=biobeamer_xml)
    BBChecker.run()

    sys.stdout.write("done. exit 0\n")
    time.sleep(5)
