# ----------------------------------------------------------------------------
# Copyright (c) 2017-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2
import numpy as np
import pandas as pd


def merge(metadata: qiime2.Metadata) -> pd.DataFrame:
    raise NotImplementedError