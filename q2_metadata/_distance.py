# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018, QIIME 2 development team.
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
    series = metadata.to_series()

    if series.hasnans:
        raise ValueError(
            "Encountered missing value(s) in the metadata column. Computing "
            "a distance matrix from missing values is not supported.")

    # This code is derived from @jairideout's scikit-bio cookbook recipe,
    # "Exploring Microbial Community Diversity"
    # https://github.com/biocore/scikit-bio-cookbook
    distances = scipy.spatial.distance.pdist(
        series.values[:, np.newaxis], metric='euclidean')
    return skbio.DistanceMatrix(distances, ids=series.index)
