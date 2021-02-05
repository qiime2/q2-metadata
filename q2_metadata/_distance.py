# ----------------------------------------------------------------------------
# Copyright (c) 2017-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import skbio
import qiime2
import numpy as np
import scipy


def distance_matrix(metadata: qiime2.NumericMetadataColumn)\
        -> skbio.DistanceMatrix:
    if metadata.has_missing_values():
        missing = metadata.get_ids(where_values_missing=True)
        raise ValueError(
            "Encountered missing value(s) in the metadata column. Computing "
            "a distance matrix from missing values is not supported. IDs with "
            "missing values: %s" % ', '.join(sorted(missing)))

    # This code is derived from @jairideout's scikit-bio cookbook recipe,
    # "Exploring Microbial Community Diversity"
    # https://github.com/biocore/scikit-bio-cookbook
    series = metadata.to_series()
    distances = scipy.spatial.distance.pdist(
        series.values[:, np.newaxis], metric='euclidean')
    return skbio.DistanceMatrix(distances, ids=series.index)
