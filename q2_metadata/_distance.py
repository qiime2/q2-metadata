# ----------------------------------------------------------------------------
# Copyright (c) 2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import skbio
import qiime2
import numpy as np
import scipy
import pandas as pd


def distance_matrix(metadata: qiime2.MetadataCategory) -> skbio.DistanceMatrix:
    try:
        series = pd.to_numeric(metadata.to_series(), errors='raise')
    except ValueError as e:
        raise ValueError(
            "Encountered non-numeric values in the metadata cateogry. A "
            "distance matrix can only be computed from numeric metadata. "
            "Original error message:\n\n%s" % e)

    # TODO this check can be removed when MetadataCategory is no longer allowed
    # to be empty
    if series.empty:
        raise ValueError(
            "Encountered metadata category that is empty, i.e. there are no "
            "samples or features in the metadata to compute distances "
            "between.")

    if series.hasnans:
        raise ValueError(
            "Encountered missing value(s) in the metadata category. Computing "
            "a distance matrix from missing values is not supported.")

    # This code is derived from @jairideout's scikit-bio cookbook recipe,
    # "Exploring Microbial Community Diversity"
    # https://github.com/biocore/scikit-bio-cookbook
    distances = scipy.spatial.distance.pdist(
        series.values[:, np.newaxis], metric='euclidean')
    return skbio.DistanceMatrix(distances, ids=series.index)
