#    This file is part of OnDA.
#
#    OnDA is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OnDA is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OnDA.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import namedtuple
from time import strptime, mktime
from scipy.constants import h, c, electron_volt

SlabShape = namedtuple('SlabShape', ['ss', 'fs'])
NativeShape = namedtuple('NativeShape', ['ss', 'fs'])

slab_shape = (2527, 2463)
native_shape = (2527, 2463)

file_extensions = ['.cbf']


def raw_data(evt):
    return evt['filehandle'].data


def num_events_in_file(_):
    return 1


def timestamp(evt):
    return evt['filectime']


def beam_energy(evt):
    try:
        header_data_list = evt['filehandle'].header[u'_array_data.header_contents'].split('\r\n')
        wavelength = float(header_data_list[15].split()[2])
        return float(h * c / (wavelength * electron_volt))
    except (AttributeError, IndexError, ValueError):
        return float(evt['monitor_params']['General']['fallback_beam_energy'])


def detector_distance(evt):
    try:
        header_data_list = evt['filehandle'].header[u'_array_data.header_contents'].split('\r\n')
        return float(header_data_list[16].split()[2])
    except (AttributeError, IndexError, ValueError):
        return float(evt['monitor_params']['General']['fallback_detector_distance'])


def filename_and_event(evt):
    return (evt['filename'], 0)
