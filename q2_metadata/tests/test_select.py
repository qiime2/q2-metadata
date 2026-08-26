# ----------------------------------------------------------------------------
# Copyright (c) 2017-2026, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

import pandas as pd
from pandas.testing import assert_frame_equal

import qiime2


class SelectTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pm = qiime2.sdk.PluginManager()
        cls.select_action = pm.plugins['metadata'].actions['select']

    def setUp(self):
        df = pd.DataFrame({
            'id': ['1', '2', '3'],
            'col1': ['a', 'b', 'c'],
            'col2': [1.0, 2.0, 9.0],
            'col3': ['some', 'cool', 'stuff'],
            'missing': ['grape', pd.NA, 'banana'],
            'weird_N&m3!?': [0.9, 1_000_000, 12],
        })
        df.set_index('id', inplace=True)

        self.md = qiime2.Metadata(df)

    def test_select_keep_true(self):
        selected, = self.select_action(self.md, columns=['col1', 'col3'])
        selected = selected.view(qiime2.Metadata).to_dataframe()

        expected = pd.DataFrame({
            'id': ['1', '2', '3'],
            'col1': ['a', 'b', 'c'],
            'col3': ['some', 'cool', 'stuff'],
        }).set_index('id')

        assert_frame_equal(selected, expected)

    def test_select_keep_false(self):
        selected, = self.select_action(
            self.md, columns=['col1', 'weird_N&m3!?'], keep=False
        )
        selected = selected.view(qiime2.Metadata).to_dataframe()

        expected = pd.DataFrame({
            'id': ['1', '2', '3'],
            'col2': [1.0, 2.0, 9.0],
            'col3': ['some', 'cool', 'stuff'],
            'missing': ['grape', pd.NA, 'banana'],
        }).set_index('id')

        assert_frame_equal(selected, expected)

    def test_select_errors_nonpresent_column(self):
        with self.assertRaisesRegex(ValueError, r'.*waldo.*not found'):
            self.select_action(self.md, columns=['col1', 'waldo', 'col2'])

        with self.assertRaisesRegex(ValueError, r'.*waldo.*not found'):
            self.select_action(self.md, columns=['col1', 'waldo'], keep=False)
