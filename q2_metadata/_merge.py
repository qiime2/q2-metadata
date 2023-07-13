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


def merge(metadata1: qiime2.Metadata,
          metadata2: qiime2.Metadata) -> pd.DataFrame:
    # Ultimately it would make sense for this action to take
    # List[qiime2.Metadata] as input, but this isn't possible right now as
    overlapping_ids = set(metadata1.ids) & set(metadata2.ids)
    overlapping_columns = set(metadata1.columns) & set(metadata2.columns)
    n_overlapping_ids = len(overlapping_ids)
    n_overlapping_columns = len(overlapping_columns)

    if len(overlapping_ids) > 0 and len(overlapping_columns) > 0:
        raise ValueError(f"Merging can currently handle overlapping ids "
                         f"or overlapping columns, but not both. "
                         f"{n_overlapping_ids} overlapping ids were "
                         f"identified ({', '.join(overlapping_ids)}) and"
                         f"{n_overlapping_columns} overlapping columns "
                         f"were identified {', '.join(overlapping_columns)}.")
    elif n_overlapping_columns == 0:
        df1 = metadata1.to_dataframe()
        df2 = metadata2.to_dataframe()
        return pd.merge(df1, df2, how='outer', left_index=True,
                            right_index=True)
    else: # i.e., n_overlapping_ids == 0
        df1 = metadata1.to_dataframe()
        df2 = metadata2.to_dataframe()
        result = pd.merge(df1, df2, how='outer', left_index=True,
                          right_index=True, suffixes=('','_'))
        for c in overlapping_columns:
            result[c] = result[c].combine_first(result[f"{c}_"])
            result = result.drop(columns=[f"{c}_"])
        return result

