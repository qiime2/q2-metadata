# ----------------------------------------------------------------------------
# Copyright (c) 2017-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

import numpy as np
import pandas as pd
import qiime2

from q2_metadata import merge


class MergeTests(unittest.TestCase):

    def test_merge_overlapping_samples_and_columns_errors(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data2 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                          columns=['col4', 'col2', 'col1']))

        self.assertRaisesRegex(ValueError,
                               "3 overl.*sam.*sample1,.*2 overl.*col.*col1,",
                               merge,
                               [md1, md2])


        index3 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data3 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md3 = qiime2.Metadata(pd.DataFrame(data3, index=index3, dtype=object,
                                          columns=['col4', 'col5', 'col6']))

        index4 = pd.Index(['sample7', 'sample8', 'sample5'], name='id')
        data4 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md4 = qiime2.Metadata(pd.DataFrame(data4, index=index4, dtype=object,
                                          columns=['col7', 'col8', 'col1']))

        self.assertRaisesRegex(ValueError,
                               "1 overl.*sam.*sample5,.*1 overl.*col.*col1,",
                               merge,
                               [md1, md3, md4])

        index5 = pd.Index(['sample4', 'sample5', 'sample1'], name='id')
        data5 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md5 = qiime2.Metadata(pd.DataFrame(data5, index=index5, dtype=object,
                                          columns=['col4', 'col5', 'col6']))

        index6 = pd.Index(['sample7', 'sample8', 'sample9'], name='id')
        data6 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md6 = qiime2.Metadata(pd.DataFrame(data4, index=index4, dtype=object,
                                          columns=['col7', 'col8', 'col1']))

        self.assertRaisesRegex(ValueError,
                               "1 overl.*sam.*sample1,.*1 overl.*col.*col1,",
                               merge,
                               [md1, md3, md4])

    def test_merge_all_samples_overlapping(self):
        # merge 2 metadata
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data2 = [['k', 'l', 'm'],
                 ['n', 'o', 'p'],
                 ['q', 'r', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col4', 'col5', 'col6']))

        obs1 = merge([md1, md2])

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data_exp1 = [['a', 'b', 'c'],
                     ['d', 'e', 'f'],
                     ['h', 'i', 'j'],
                     ['k', 'l', 'm'],
                     ['n', 'o', 'p'],
                     ['q', 'r', 's']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3',
                                  'col4', 'col5', 'col6']))

        self.assertEqual(obs1, exp1)

        # merge 3 metadata
        index3 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data3 = [['t', 'u', 'v']]
        md3 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col7']))

        obs2 = merge([md1, md2, md3])

        index_exp2 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data_exp2 = [['a', 'b', 'c'],
                     ['d', 'e', 'f'],
                     ['h', 'i', 'j'],
                     ['k', 'l', 'm'],
                     ['n', 'o', 'p'],
                     ['q', 'r', 's'],
                     ['t', 'u', 'v']]
        exp2 = qiime2.Metadata(
            pd.DataFrame(data_exp2, index=index_exp2, dtype=object,
                         columns=['col1', 'col2', 'col3',
                                  'col4', 'col5', 'col6', 'col7']))

        self.assertEqual(obs2, exp2)

    def test_merge_some_samples_overlapping(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample1', 'sample2', 'sample4'], name='id')
        data2 = [['k', 'l', 'm'],
                 ['n', 'o', 'p'],
                 ['q', 'r', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col4', 'col5', 'col6']))

        index3 = pd.Index(['sample1'], name='id')
        data3 = [['t']]
        md3 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col7']))

        obs1 = merge([md1, md2, md3])

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3', 'sample4'],
                              name='id')
        data_exp1 = [['a', 'b', 'c', np.nan],
                     ['d', 'e', 'f', np.nan],
                     ['h', 'i', 'j', np.nan],
                     ['k', 'l', np.nan, 'm'],
                     ['n', 'o', np.nan, 'p'],
                     ['q', 'r', np.nan, 's'],
                     ['t', np.nan, np.nan, np.nan]]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3',
                                  'col4', 'col5', 'col6', 'col7']))

        self.assertEqual(obs1, exp1)

    def test_merge_all_columns_overlapping(self):
        # merge 2 metadata
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data2 = [['k', 'l', 'm'],
                 ['n', 'o', 'p'],
                 ['q', 'r', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        obs1 = merge([md1, md2])

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3',
                               'sample4', 'sample5', 'sample6'], name='id')
        data_exp1 = [['a', 'b', 'c', 'k', 'l', 'm'],
                     ['d', 'e', 'f', 'n', 'o', 'p'],
                     ['h', 'i', 'j', 'q', 'r', 's']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3']))

        self.assertEqual(obs1, exp1)

        # merge 3 metadata
        index3 = pd.Index(['sample7'], name='id')
        data3 = [['t'],
                 ['u'],
                 ['v']]
        md3 = qiime2.Metadata(pd.DataFrame(data3, index=index3, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        obs2 = merge([md1, md2, md3])

        index_exp2 = pd.Index(['sample1', 'sample2', 'sample3',
                               'sample4', 'sample5', 'sample6',
                               'sample7'], name='id')
        data_exp2 = [['a', 'b', 'c', 'k', 'l', 'm', 't'],
                     ['d', 'e', 'f', 'n', 'o', 'p', 'u'],
                     ['h', 'i', 'j', 'q', 'r', 's', 'v']]
        exp2 = qiime2.Metadata(
            pd.DataFrame(data_exp2, index=index_exp2, dtype=object,
                         columns=['col1', 'col2', 'col3']))

        self.assertEqual(obs2, exp2)

    def test_merge_some_columns_overlapping(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data2 = [['k', 'l', 'm'],
                 ['n', 'o', 'p'],
                 ['q', 'r', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col4']))

        index3 = pd.Index(['sample7'], name='id')
        data3 = [['t'],
                 ['u'],
                 ['w']]
        md3 = qiime2.Metadata(pd.DataFrame(data3, index=index3, dtype=object,
                                          columns=['col1', 'col2', 'col5']))

        obs1 = merge([md1, md2, md3])

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3',
                               'sample4', 'sample5', 'sample6',
                               'sample7'], name='id')
        data_exp1 = [['a', 'b', 'c', 'k', 'l', 'm', 't'],
                     ['d', 'e', 'f', 'n', 'o', 'p', 'u'],
                     ['h', 'i', 'j', np.nan, np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, 'q', 'r', 's', np.nan],
                     [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 'w']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3', 'col4', 'col5']))

        self.assertEqual(obs1, exp1)

    def test_merge_no_samples_or_columns_overlapping(self):
        # merge 2 metadata
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'b', 'c'],
                 ['d', 'e', 'f'],
                 ['h', 'i', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data2 = [['k', 'l', 'm'],
                 ['n', 'o', 'p'],
                 ['q', 'r', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                          columns=['col4', 'col5', 'col6']))

        obs1 = merge([md1, md2])

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3',
                               'sample4', 'sample5', 'sample6'], name='id')
        data_exp1 = [['a', 'b', 'c', np.nan, np.nan, np.nan],
                     ['d', 'e', 'f', np.nan, np.nan, np.nan],
                     ['h', 'i', 'j', np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, 'k', 'l', 'm'],
                     [np.nan, np.nan, np.nan, 'n', 'o', 'p'],
                     [np.nan, np.nan, np.nan, 'q', 'r', 's']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3',
                                  'col4', 'col5', 'col6']))

        self.assertEqual(obs1, exp1)