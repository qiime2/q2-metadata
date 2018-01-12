# ----------------------------------------------------------------------------
# Copyright (c) 2017-2018, QIIME 2 development team.
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
    def test_int_category(self):
        md = qiime2.MetadataCategory(
            pd.Series([1, 2, 3], name='number',
                      index=['sample1', 'sample2', 'sample3']))
        exp = skbio.DistanceMatrix([[0, 1, 2],
                                    [1, 0, 1],
                                    [2, 1, 0]],
                                   ids=['sample1', 'sample2', 'sample3'])

        obs = distance_matrix(md)

        self.assertEqual(exp, obs)

    def test_float_category(self):
        md = qiime2.MetadataCategory(
            pd.Series([1.5, 2.0, 3.0], name='number',
                      index=['sample1', 'sample2', 'sample3']))
        exp = skbio.DistanceMatrix([[0.0, 0.5, 1.5],
                                    [0.5, 0.0, 1.0],
                                    [1.5, 1.0, 0.0]],
                                   ids=['sample1', 'sample2', 'sample3'])
        obs = distance_matrix(md)

        self.assertEqual(exp, obs)

    def test_one_sample(self):
        md = qiime2.MetadataCategory(
            pd.Series([1.5], name='number', index=['sample1']))
        exp = skbio.DistanceMatrix([[0.0]],
                                   ids=['sample1'])

        obs = distance_matrix(md)

        self.assertEqual(exp, obs)

    def test_str_casting(self):
        md = qiime2.MetadataCategory(
            pd.Series(['1', '2', '3', '4'], name='number',
                      index=['sample1', 'sample2', 'sample3', 'sample4']))
        exp = skbio.DistanceMatrix([[0.0, 1.0, 2.0, 3.0],
                                    [1.0, 0.0, 1.0, 2.0],
                                    [2.0, 1.0, 0.0, 1.0],
                                    [3.0, 2.0, 1.0, 0.0]],
                                   ids=['sample1', 'sample2', 'sample3',
                                        'sample4'])

        obs = distance_matrix(md)

        self.assertEqual(exp, obs)

    def test_non_numeric_category(self):
        md = qiime2.MetadataCategory(
            pd.Series(['x1', 'x2', '3', '4'], name='number',
                      index=['sample1', 'sample2', 'sample3', 'sample4']))

        with self.assertRaisesRegex(ValueError,
                                    'non-numeric values.*\n\n.*x1'):
            distance_matrix(md)

    def test_missing_values(self):
        md = qiime2.MetadataCategory(
            pd.Series([1.0, 2.0, np.nan, 4.0], name='number',
                      index=['sample1', 'sample2', 'sample3', 'sample4']))

        with self.assertRaisesRegex(ValueError, 'missing values'):
            distance_matrix(md)

    def test_empty_metadata_category(self):
        md = qiime2.MetadataCategory(pd.Series([], name='number', index=[]))

        with self.assertRaisesRegex(ValueError, 'metadata category.*empty'):
            distance_matrix(md)


if __name__ == "__main__":
    unittest.main()
