# -*- coding: UTF-8 -*-

# Neahttadigisánit — online, inflectional dictionary
# Copyright (C) 2013–2017 University of Tromsø
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Morphology module.
"""

from morphology import ( Tagsets
                       , Tagset
                       , Tag
                       , HFST
                       , XFST
                       , OBT
                       , Morphology
                       , generation_overrides
                       )


__all__ = [ 'XFST'
          , 'HFST'
          , 'OBT'
          , 'Morphology'
          , 'generation_overrides'
          , 'Tag'
          , 'Tagsets'
          , 'Tagset'
          ]
