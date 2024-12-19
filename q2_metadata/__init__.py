# ----------------------------------------------------------------------------
# Copyright (c) 2017-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._tabulate import tabulate
from ._distance import distance_matrix
from ._random import shuffle_groups
from ._merge import merge

try:
    from ._version import __version__
except ModuleNotFoundError:
    __version__ = '0.0.0+notfound'

__all__ = ['tabulate', 'distance_matrix', 'shuffle_groups', 'merge']
