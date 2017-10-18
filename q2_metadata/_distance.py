# ----------------------------------------------------------------------------
# Copyright (c) 2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources
import shutil

import skbio
import qiime2
import numpy
import scipy
import pandas as pd


def _metadata_distance(metadata: pd.Series) -> skbio.DistanceMatrix:
    # This code is derived from @jairideout's scikit-bio cookbook recipe,
    # "Exploring Microbial Community Diversity"
    # https://github.com/biocore/scikit-bio-cookbook
    distances = scipy.spatial.distance.pdist(
        metadata.values[:, numpy.newaxis], metric='euclidean')
    return skbio.DistanceMatrix(distances, ids=metadata.index)


def distance_matrix(metadata: qiime2.MetadataCategory) -> skbio.DistanceMatrix:
    try:
        metadata = pd.to_numeric(metadata.to_series(), errors='raise')
    except ValueError as e:
        raise ValueError('Only numeric data can be used with the Mantel test. '
                         'Non-numeric data was encountered in the sample '
                         'metadata. Orignal error message follows:\n%s' %
                         str(e))

    metadata = metadata.replace(r'', numpy.nan).dropna()

    return _metadata_distance(metadata)
