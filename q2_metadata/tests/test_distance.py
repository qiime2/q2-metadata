# ----------------------------------------------------------------------------
# Copyright (c) 2017, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from unittest import TestCase, main

import pandas as pd
import numpy as np
import skbio
import qiime2

from q2_metadata import distance_matrix
from q2_metadata._distance import _metadata_distance


class DistanceMatrixTests(TestCase):

    def test_metadata_distance_int(self):
        md = pd.Series([1, 2, 3], name='number',
                       index=['sample1', 'sample2', 'sample3'])
        exp = skbio.DistanceMatrix([[0, 1, 2],
                                    [1, 0, 1],
                                    [2, 1, 0]],
                                   ids=['sample1', 'sample2', 'sample3'])
        obs = _metadata_distance(md)
        self.assertEqual(exp, obs)

    def test_metadata_distance_float(self):
        md = pd.Series([1.5, 2.0, 3.0], name='number',
                       index=['sample1', 'sample2', 'sample3'])
        exp = skbio.DistanceMatrix([[0.0, 0.5, 1.5],
                                    [0.5, 0.0, 1.0],
                                    [1.5, 1.0, 0.0]],
                                   ids=['sample1', 'sample2', 'sample3'])
        obs = _metadata_distance(md)
        self.assertEqual(exp, obs)

    def test_metadata_distance_one_sample(self):
        md = pd.Series([1.5], name='number',
                       index=['sample1'])
        exp = skbio.DistanceMatrix([[0.0]],
                                   ids=['sample1'])
        obs = _metadata_distance(md)
        self.assertEqual(exp, obs)

    def test_distance_matrix(self):
        md = qiime2.MetadataCategory(
            pd.Series(['1', '2', '3', '4'], name='number',
                      index=['sample1', 'sample2', 'sample3', 'sample4']))
        dm = distance_matrix(md)
        exp_data = np.array([[0.0, 1.0, 2.0, 3.0],
                             [1.0, 0.0, 1.0, 2.0],
                             [2.0, 1.0, 0.0, 1.0],
                             [3.0, 2.0, 1.0, 0.0]])
        exp_ids = ('sample1', 'sample2', 'sample3', 'sample4')
        np.testing.assert_array_equal(exp_data, dm.data)
        self.assertEqual(exp_ids, dm.ids)

    def test_distance_matrix_non_numeric(self):
        md = qiime2.MetadataCategory(
            pd.Series(['x1', 'x2', '3', '4'], name='number',
                      index=['sample1', 'sample2', 'sample3', 'sample4']))
        with self.assertRaises(ValueError):
            distance_matrix(md)


if __name__ == "__main__":
    main()
