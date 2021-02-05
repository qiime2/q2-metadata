# ----------------------------------------------------------------------------
# Copyright (c) 2017-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
from unittest import TestCase, main
import tempfile

import pandas as pd
import qiime2

from q2_metadata import tabulate


class TabulateTests(TestCase):
    def test_valid_metadata(self):
        index = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data = ['1.0', '2.0', '3.0']
        md = qiime2.Metadata(pd.DataFrame({'foo': data}, index=index,
                                          dtype=object))

        with tempfile.TemporaryDirectory() as output_dir:
            tabulate(output_dir, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))

            viz = open(index_fp).read()

            self.assertTrue('pageLength: 100' in viz)
            self.assertTrue('"columns":[["id",""],["foo","categorical"]]'
                            in viz)
            self.assertTrue(all(i in viz for i in index))
            self.assertTrue(all(val in viz for val in data))

    def test_valid_metadata_many_columns(self):
        index = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data = [['1.0', 'lorem', 'peanut'],
                ['2.0', 'ipsum', 'the'],
                ['3.0', 'emrakul', 'dog']]
        md = qiime2.Metadata(pd.DataFrame(data, index=index, dtype=object,
                                          columns=['foo', 'bar', 'baz']))

        with tempfile.TemporaryDirectory() as output_dir:
            tabulate(output_dir, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))

            viz = open(index_fp).read()

            self.assertTrue('pageLength: 100' in viz)
            self.assertTrue('"columns":[["id",""],["foo","categorical"],'
                            '["bar","categorical"],["baz","categorical"]]'
                            in viz)
            self.assertTrue(all(i in viz for i in index))
            self.assertTrue(all(v in viz for row in data for v in row))

    def test_multiple_dtypes(self):
        index = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        data = [[1.0, 'lorem'], [2.0, 'ipsum'], [3.0, 'emrakul']]
        md = qiime2.Metadata(pd.DataFrame(data, index=index,
                                          columns=['foo', 'bar']))

        with tempfile.TemporaryDirectory() as output_dir:
            tabulate(output_dir, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))

            viz = open(index_fp).read()
            self.assertTrue('pageLength: 100' in viz)
            self.assertTrue('"columns":[["id",""],["foo","numeric"],'
                            '["bar","categorical"]]' in viz)
            self.assertTrue(all(i in viz for i in index))
            self.assertTrue(all(str(v) in viz for row in data for v in row))

    def test_pagination(self):
        index = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        values = ['1.0', '2.0', '3.0']
        md = qiime2.Metadata(pd.DataFrame({'value': values}, index=index))

        with tempfile.TemporaryDirectory() as output_dir:
            tabulate(output_dir, md, page_size=2)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))

            viz = open(index_fp).read()

            self.assertTrue('pageLength: 2' in viz)

    def test_invalid_pagination(self):
        index = pd.Index(['sample1', 'sample2', 'sample3'], name='id')
        values = ['1.0', '2.0', '3.0']
        md = qiime2.Metadata(pd.DataFrame({'value': values}, index=index))

        with tempfile.TemporaryDirectory() as output_dir:
            with self.assertRaisesRegex(ValueError, 'less than one'):
                tabulate(output_dir, md, -1)


if __name__ == "__main__":
    main()
