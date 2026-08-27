# ----------------------------------------------------------------------------
# Copyright (c) 2017-2026, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import re
import warnings

import qiime2
from qiime2.core.exceptions import RachisWarning


def select(
    metadata: qiime2.Metadata,
    columns: list[str],
    use_regex: bool = False,
    keep: bool = True,
) -> qiime2.Metadata:
    '''
    Retain or remove columns in the metadata.

    Parameters
    ----------
    metadata : Metadata
        The metadata from which to select columns.
    columns : list[str]
        The columns to retain or remove.
    use_regex : bool
        If true, then column names will be interpreted as regexes and each
        name can match any number of columns.
    keep : bool
        Whether to keep only (if true) or remove (if false) the columns
        in `columns`.

    Returns
    -------
    Metadata
        The selected metadata.
    '''
    if len(metadata.columns) == 0:
        raise ValueError(
            'No columns were provided in the metadata.'
        )

    metadata = metadata.to_dataframe()

    if use_regex:
        matched_columns = []
        for pattern in columns:
            try:
                re.compile(pattern)
            except re.error as e:
                raise ValueError(
                    'An invalid regular expression was given.'
                ) from e

            for column in metadata.columns:
                if re.search(pattern, column):
                    matched_columns.append(column)

        columns = matched_columns
    else:
        for column in columns:
            if column not in metadata.columns:
                raise ValueError(
                    f'Column "{column}" was not found in the metadata.'
                )

    if keep and set(columns) == set(metadata.columns):
        warnings.warn(
            'The metadata was unchanged (all columns were retained).',
            RachisWarning
        )

    if keep:
        remove = list(set(metadata.columns) - set(columns))
    else:
        remove = columns

    metadata.drop(remove, axis=1, inplace=True)

    if len(metadata.columns) == 0:
        raise ValueError(
            'No columns remained in the metadata after selecting.'
        )

    return qiime2.Metadata(metadata)
