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
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data2 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]

        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        self.assertRaisesRegex(ValueError,
                               "3 overl.*ids.*sample1.*3 overl.*col.*col1",
                               merge, md1, md2)

        index3 = pd.Index(['sample4', 'sample5', 'sample1'], name='id')
        data3 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md3 = qiime2.Metadata(pd.DataFrame(data3, index=index3, dtype=object,
                                           columns=['col4', 'col5', 'col1']))

        self.assertRaisesRegex(ValueError,
                               "1 overl.*ids.*sample1.*1 overl.*col.*col1",
                               merge, md1, md3)

    def test_merge_all_samples_overlapping(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data2 = [['k', 'n', 'q'],
                 ['l', 'o', 'r'],
                 ['m', 'p', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                           columns=['col4', 'col5', 'col6']))

        obs1 = merge(md1, md2)

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data_exp1 = [['a', 'd', 'h', 'k', 'n', 'q'],
                     ['b', 'e', 'i', 'l', 'o', 'r'],
                     ['c', 'f', 'j', 'm', 'p', 's']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3',
                                  'col4', 'col5', 'col6']))

        self.assertEqual(obs1, exp1)

    def test_merge_some_samples_overlapping(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample1', 'sample2', 'sample4'], name='id')
        data2 = [['k', 'n'],
                 ['l', 'o'],
                 ['m', 'p']]
        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                           columns=['col4', 'col5']))

        obs1 = merge(md1, md2)

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3', 'sample4'],
                              name='id')
        data_exp1 = [['a', 'd', 'h', 'k', 'n'],
                     ['b', 'e', 'i', 'l', 'o'],
                     ['c', 'f', 'j', np.nan, np.nan],
                     [np.nan, np.nan, np.nan, 'm', 'p']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3',
                                  'col4', 'col5']))

        self.assertEqual(obs1, exp1)

    def test_merge_all_columns_overlapping(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data2 = [['k', 'n', 'q'],
                 ['l', 'o', 'r'],
                 ['m', 'p', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        obs1 = merge(md1, md2)
        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3',
                               'sample4', 'sample5', 'sample6'], name='id')
        data_exp1 = [['a', 'd', 'h'],
                     ['b', 'e', 'i'],
                     ['c', 'f', 'j'],
                     ['k', 'n', 'q'],
                     ['l', 'o', 'r'],
                     ['m', 'p', 's']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3']))
        self.assertEqual(obs1, exp1)

    def test_merge_some_columns_overlapping(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data2 = [['k', 'n', 'q'],
                 ['l', 'o', 'r'],
                 ['m', 'p', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                           columns=['col1', 'col2', 'col4']))

        obs1 = merge(md1, md2)

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3',
                               'sample4', 'sample5', 'sample6'], name='id')
        data_exp1 = [['a', 'd', 'h', np.nan],
                     ['b', 'e', 'i', np.nan],
                     ['c', 'f', 'j', np.nan],
                     ['k', 'n', np.nan, 'q'],
                     ['l', 'o', np.nan, 'r'],
                     ['m', 'p', np.nan, 's']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3', 'col4']))

        self.assertEqual(obs1, exp1)

    def test_merge_no_samples_or_columns_overlapping(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data2 = [['k', 'n', 'q'],
                 ['l', 'o', 'r'],
                 ['m', 'p', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                           columns=['col4', 'col5', 'col6']))

        obs1 = merge(md1, md2)

        index_exp1 = pd.Index(['sample1', 'sample2', 'sample3',
                               'sample4', 'sample5', 'sample6'], name='id')
        data_exp1 = [['a', 'd', 'h', np.nan, np.nan, np.nan],
                     ['b', 'e', 'i', np.nan, np.nan, np.nan],
                     ['c', 'f', 'j', np.nan, np.nan, np.nan],
                     [np.nan, np.nan, np.nan, 'k', 'n', 'q'],
                     [np.nan, np.nan, np.nan, 'l', 'o', 'r'],
                     [np.nan, np.nan, np.nan, 'm', 'p', 's']]
        exp1 = qiime2.Metadata(
            pd.DataFrame(data_exp1, index=index_exp1, dtype=object,
                         columns=['col1', 'col2', 'col3',
                                  'col4', 'col5', 'col6']))

        self.assertEqual(obs1, exp1)

    def test_merge_mismatched_columnID_names_in_error_message(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(pd.DataFrame(data1, index=index1, dtype=object,
                                           columns=['col1', 'col2', 'col3']))

        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='sample-id')
        data2 = [['k', 'n', 'q'],
                 ['l', 'o', 'r'],
                 ['m', 'p', 's']]
        md2 = qiime2.Metadata(pd.DataFrame(data2, index=index2, dtype=object,
                                           columns=['col4', 'col5', 'col6']))

        with self.assertRaisesRegex(
            ValueError,
            "Metadata files contain different ID column names.*id.*sample-id"
        ):
            merge(md1, md2)

    def test_merge_mismatched_md_column_type_designations(self):
        index1 = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data1 = [['a', 'd', 'h'],
                 ['b', 'e', 'i'],
                 ['c', 'f', 'j']]
        md1 = qiime2.Metadata(
            pd.DataFrame(
                data1,
                index=index1,
                dtype=object,
                columns=['col1', 'col2', 'col3']
            )
        )
        index2 = pd.Index(['sample4', 'sample5', 'sample6'], name='id')
        data2 = [['k', 'n', 40.0],
                 ['l', 'o', 41.0],
                 ['m', 'p', 42.0]]
        md2 = qiime2.Metadata(
            pd.DataFrame(
                data2,
                index=index2,
                columns=['col1', 'col2', 'col3']
            )
        )
        with self.assertRaisesRegex(
            ValueError,
            "Metadata files contain the shared column 'col3' with different "
            "type designations. In 'metadata1', the column 'col3' is of type "
            "\(CategoricalMetadataColumn\), and in 'metadata2', it is of type "
            "\(NumericMetadataColumn\). These type designations must match."
        ):
            merge(md1, md2)
