#!/usr/bin/python
# -*- coding: latin1 -*-

"""
$HeadURL: http://fgcz-svn.uzh.ch/repos/fgcz/stable/proteomics/BioBeamer/fgcz_biobeamer.py $
$Id: fgcz_biobeamer.py 7915 2015-12-21 08:16:17Z cpanse $
$Date: 2015-12-21 09:16:17 +0100 (Mon, 21 Dec 2015) $

Copyright 2006-2015 Functional Genomics Center Zurich

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


class TestTargetMapping(unittest.TestCase):
    """
    run
        python -m unittest -v fgcz_biobeamer
    """
    def setUp(self):
        pass

    def test_tripletof(self):
        desired_result = os.path.normpath('p1000/Proteomics/TRIPLETOF_1/selevsek_20150119')
        self.assertTrue(desired_result == map_data_analyst_tripletof_1('p1000\Data\selevsek_20150119'))
        self.assertTrue(map_data_analyst_tripletof_1('p1000\data\selevsek_20150119') is None)
