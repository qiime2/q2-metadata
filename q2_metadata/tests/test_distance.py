# ----------------------------------------------------------------------------
# Copyright (c) 2017-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

import pandas as pd
import numpy as np
import skbio
import qiime2

from q2_metadata import distance_matrix


class DistanceMatrixTests(unittest.TestCase):
    def test_int_column(self):
        md = qiime2.NumericMetadataColumn(
            pd.Series([1, 2, 3], name='number',
                      index=pd.Index(['sample1', 'sample2', 'sample3'],
                                     name='id'))
        )
        exp = skbio.DistanceMatrix([[0, 1, 2],
                                    [1, 0, 1],
                                    [2, 1, 0]],
                                   ids=['sample1', 'sample2', 'sample3'])

        obs = distance_matrix(md)

        self.assertEqual(exp, obs)

    def test_float_column(self):
        md = qiime2.NumericMetadataColumn(
            pd.Series([1.5, 2.0, 3.0], name='number',
                      index=pd.Index(['sample1', 'sample2', 'sample3'],
                                     name='id'))
        )
        exp = skbio.DistanceMatrix([[0.0, 0.5, 1.5],
                                    [0.5, 0.0, 1.0],
                                    [1.5, 1.0, 0.0]],
                                   ids=['sample1', 'sample2', 'sample3'])
        obs = distance_matrix(md)

        self.assertEqual(exp, obs)

    def test_one_sample(self):
        md = qiime2.NumericMetadataColumn(
            pd.Series([1.5], name='number',
                      index=pd.Index(['sample1'],
                                     name='id'))
        )
        exp = skbio.DistanceMatrix([[0.0]],
                                   ids=['sample1'])

        obs = distance_matrix(md)

        self.assertEqual(exp, obs)

    def test_missing_values(self):
        md = qiime2.NumericMetadataColumn(
            pd.Series([1.0, 2.0, np.nan, 4.0], name='number',
                      index=pd.Index(['sample1', 'sample2', 'sample3',
                                      'sample4'],
                                     name='id'))
        )

        with self.assertRaisesRegex(ValueError, 'missing values'):
            distance_matrix(md)


if __name__ == "__main__":
    unittest.main()
