# ----------------------------------------------------------------------------
# Copyright (c) 2017-2026, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2


def select(
    metadata: qiime2.Metadata,
    columns: list[str],
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
    keep : bool
        Whether to keep only (if true) or remove (if false) the columns
        in `columns`.

    Returns
    -------
    Metadata
        The selected metadata.
    '''
    metadata = metadata.to_dataframe()

    for column in columns:
        if column not in metadata.columns:
            raise ValueError(
                f'Column "{column}" was not found in the metadata.'
            )

    if keep:
        remove = list(set(metadata.columns) - set(columns))
    else:
        remove = columns

    metadata.drop(remove, axis=1, inplace=True)

    return qiime2.Metadata(metadata)
