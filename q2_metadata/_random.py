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


def shuffle_groups(metadata: qiime2.CategoricalMetadataColumn,
                   n_columns: int = 3,
                   column_name_prefix: str = 'shuffled.grouping.',
                   # Suggest renaming this variable to sample_value_prefix for
                   # clarity
                   column_value_prefix: str = 'fake.group.',
                   encode_sample_size: bool = False
                   ) -> pd.DataFrame:

    input_column_name = metadata.name
    df = metadata.to_dataframe()
    group_sample_size = df[input_column_name].value_counts()

    value_mapping = {}
    for i, value in enumerate(df[input_column_name].unique()):
        if encode_sample_size is True:
            value_mapping[value] = '%s%d%s' % (column_value_prefix, i,
                                               f'.n={group_sample_size[value]}')
        else:
            value_mapping[value] = '%s%d' % (column_value_prefix, i)

    first_column_id = '%s0' % column_name_prefix
    df[first_column_id] = df[input_column_name].map(value_mapping)

    df[first_column_id] = \
        np.random.permutation(df[first_column_id].values)

    for i in range(1, n_columns):
        column_id = '%s%d' % (column_name_prefix, i)

        df[column_id] = \
            np.random.permutation(df[first_column_id].values)

    df = df.drop(input_column_name, axis=1)

    return df
