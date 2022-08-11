# ----------------------------------------------------------------------------
# Copyright (c) 2017-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

import pandas as pd
import numpy as np
import qiime2

from q2_metadata import random_groups


class RandomGroupsTests(unittest.TestCase):

    # number of iterations to run for tests of randomization
    n_iterations = 100

    def test_random_groups_shape_41(self):
        md = qiime2.CategoricalMetadataColumn(
            pd.Series(['a', 'b', 'a', 'b'], name='groups',
                      index=pd.Index(['sample1', 'sample2', 'sample3', 's4'],
                                     name='id'))
        )

        # expected number of rows and columns in result
        obs = random_groups(md, n_columns=1,
                            column_name_prefix='random-grouping-',
                            column_value_prefix='fake-group-')
        self.assertEqual(obs.shape, (4,1))

        # expected column names (the original should not be in the result)
        self.assertFalse('groups' in obs.columns)
        self.assertTrue('random-grouping-0' in obs.columns)

        # correct number of groups in the new column
        self.assertEqual(len(obs['random-grouping-0'].unique()), 2)

        # correct group names in new column
        self.assertEqual(set(obs['random-grouping-0'].unique()),
                         {'fake-group-1', 'fake-group-0'})

        # distributions of value counts are equal in input and output
        self.assertEqual(sorted(list(obs['random-grouping-0'].value_counts())),
                         sorted(list(md.to_series().value_counts())))

        # randomization of key/value associations is occurring
        random_check = []
        for i in range(self.n_iterations):
            obs2 = random_groups(md, n_columns=1,
                                 column_name_prefix='random-grouping-',
                                 column_value_prefix='fake-group-')
            random_check.append(
                list(obs['random-grouping-0']) ==
                list(obs2['random-grouping-0']))
        self.assertIn(False, random_check,
                      "All random groupings in %d iterations were "
                      "identicial, suggesting that values are not "
                      "randomly assigned." % self.n_iterations)

    def test_random_groups_shape_33(self):
        md = qiime2.CategoricalMetadataColumn(
            pd.Series(['a', 'b', 'c','a', 'b', 'c','a', 'b', 'c'],
                      name='groups',
                      index=pd.Index(['sample1', 'sample2', 'sample3',
                                      'samplea', 'sampleb', 'sc',
                                      'sample1_w', 'ctl1', 'ctl3'],
                                     name='id'))
        )

        # expected number of rows and columns
        obs = random_groups(md, n_columns=3,
                            column_name_prefix='random-grouping-',
                            column_value_prefix='fake-group-')
        self.assertEqual(obs.shape, (9,3))

        # original column name should not be in the result
        self.assertFalse('groups' in obs.columns)

        for i in range(3):
            column_id = 'random-grouping-%d' % i
            self.assertTrue(column_id in obs.columns)

            # correct number of groups in the new column
            self.assertEqual(len(obs[column_id].unique()), 3)

            self.assertEqual(set(obs[column_id].unique()),
                            {'fake-group-1', 'fake-group-0', 'fake-group-2'})

        # randomization of key/value associations is occurring
        random_check1 = []
        random_check2 = []
        random_check3 = []
        for i in range(self.n_iterations):
            random_check1.append(
                list(obs['random-grouping-0']) ==
                list(obs['random-grouping-1']))
            random_check2.append(
                list(obs['random-grouping-0']) ==
                list(obs['random-grouping-2']))
            random_check3.append(
                list(obs['random-grouping-1']) ==
                list(obs['random-grouping-2']))
        self.assertIn(False, random_check1,
                    "All random groupings in %d iterations were "
                    "identicial, suggesting that values are not "
                    "randomly assigned." % self.n_iterations)
        self.assertIn(False, random_check2,
                    "All random groupings in %d iterations were "
                    "identicial, suggesting that values are not "
                    "randomly assigned." % self.n_iterations)
        self.assertIn(False, random_check3,
                    "All random groupings in %d iterations were "
                    "identicial, suggesting that values are not "
                    "randomly assigned." % self.n_iterations)

    def test_random_groups_alt_input_column_name(self):
        md = qiime2.CategoricalMetadataColumn(
            pd.Series(['a', 'b', 'a', 'b'], name='xyz',
                      index=pd.Index(['sample1', 'sample2', 'sample3', 's4'],
                                     name='id'))
        )

        # expected number of rows and columns in result
        obs = random_groups(md, n_columns=1,
                            column_name_prefix='random-grouping-',
                            column_value_prefix='fake-group-')
        self.assertEqual(obs.shape, (4,1))

        # expected column names (the original should not be in the result)
        self.assertFalse('xyz' in obs.columns)
        self.assertTrue('random-grouping-0' in obs.columns)

        # correct number of groups in the new column
        self.assertEqual(len(obs['random-grouping-0'].unique()), 2)

        # correct group names in new column
        self.assertEqual(set(obs['random-grouping-0'].unique()),
                         {'fake-group-1', 'fake-group-0'})

    def test_random_groups_alt_column_name_prefix(self):
        md = qiime2.CategoricalMetadataColumn(
            pd.Series(['a', 'b', 'a', 'b'], name='groups',
                      index=pd.Index(['sample1', 'sample2', 'sample3', 's4'],
                                     name='id'))
        )

        # expected number of rows and columns in result
        obs = random_groups(md, n_columns=1,
                            column_name_prefix='1',
                            column_value_prefix='fake-group-')
        self.assertEqual(obs.shape, (4,1))

        # expected column names (the original should not be in the result)
        self.assertFalse('groups' in obs.columns)
        self.assertTrue('10' in obs.columns)

        # correct number of groups in the new column
        self.assertEqual(len(obs['10'].unique()), 2)

        # correct group names in new column
        self.assertEqual(set(obs['10'].unique()),
                         {'fake-group-1', 'fake-group-0'})

    def test_random_groups_alt_column_value_prefix(self):
        md = qiime2.CategoricalMetadataColumn(
            pd.Series(['a', 'b', 'a', 'b'], name='groups',
                      index=pd.Index(['sample1', 'sample2', 'sample3', 's4'],
                                     name='id'))
        )

        # expected number of rows and columns in result
        obs = random_groups(md, n_columns=1,
                            column_name_prefix='random-grouping-',
                            column_value_prefix='1')
        self.assertEqual(obs.shape, (4,1))

        # expected column names (the original should not be in the result)
        self.assertFalse('groups' in obs.columns)
        self.assertTrue('random-grouping-0' in obs.columns)

        # correct number of groups in the new column
        self.assertEqual(len(obs['random-grouping-0'].unique()), 2)

        # correct group names in new column
        self.assertEqual(set(obs['random-grouping-0'].unique()),
                         {'11', '10'})