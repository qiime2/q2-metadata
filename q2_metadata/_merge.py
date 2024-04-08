# ----------------------------------------------------------------------------
# Copyright (c) 2017-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2
import pandas as pd


def merge(metadata1: qiime2.Metadata,
          metadata2: qiime2.Metadata) -> qiime2.Metadata:
    # Ultimately it would make sense for this action to take
    # List[qiime2.Metadata] as input, but this isn't possible right now
    overlapping_ids = set(metadata1.ids) & set(metadata2.ids)
    overlapping_columns = set(metadata1.columns) & set(metadata2.columns)
    n_overlapping_ids = len(overlapping_ids)
    n_overlapping_columns = len(overlapping_columns)

    if n_overlapping_ids and n_overlapping_columns:
        raise ValueError(
            "Merging can currently handle overlapping ids or overlapping"
            f"but not both. {n_overlapping_ids} overlapping ids were "
            f"identified ({', '.join(overlapping_ids)}) and"
            f"{n_overlapping_columns} overlapping columns were identified "
            f"{', '.join(overlapping_columns)}."
        )

    df1 = metadata1.to_dataframe()
    df2 = metadata2.to_dataframe()

    if df1.index.name != df2.index.name:
        raise ValueError(
            "Metadata files contain different ID column names. First "
            f"metadata file contains '{df1.index.name}' and the second "
            f"contains '{df2.index.name}'. These column names must match."
        )

    if not n_overlapping_columns:
        result = pd.merge(df1, df2, how='outer', left_index=True,
                          right_index=True)

    else:  # i.e., n_overlapping_ids == 0
        result = pd.merge(df1, df2, how='outer', left_index=True,
                          right_index=True, suffixes=('', '_'))
        for c in overlapping_columns:
            result[c] = result[c].combine_first(result[f"{c}_"])
            result = result.drop(columns=[f"{c}_"])

    return qiime2.Metadata(result)
