# ----------------------------------------------------------------------------
# Copyright (c) 2016-2017, QIIME 2 development team.
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
        index = ['sample1', 'sample2', 'sample3']
        values = ['1.0', '2.0', '3.0']
        md = qiime2.Metadata(pd.DataFrame({'value': values}, index=index))

        with tempfile.TemporaryDirectory() as output_dir:
            tabulate(output_dir, md)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))

            viz = open(index_fp).read()

            self.assertTrue('pageLength: 100' in viz)
            for i in index:
                self.assertTrue(i in viz)
            for v in values:
                self.assertTrue(v in viz)

    def test_pagination(self):
        index = ['sample1', 'sample2', 'sample3']
        values = ['1.0', '2.0', '3.0']
        md = qiime2.Metadata(pd.DataFrame({'value': values}, index=index))

        with tempfile.TemporaryDirectory() as output_dir:
            tabulate(output_dir, md, page_size=2)
            index_fp = os.path.join(output_dir, 'index.html')
            self.assertTrue(os.path.exists(index_fp))

            viz = open(index_fp).read()

            self.assertTrue('pageLength: 2' in viz)

    def test_invalid_pagination(self):
        index = ['sample1', 'sample2', 'sample3']
        values = ['1.0', '2.0', '3.0']
        md = qiime2.Metadata(pd.DataFrame({'value': values}, index=index))

        with tempfile.TemporaryDirectory() as output_dir:
            with self.assertRaisesRegex(ValueError, 'less than one'):
                tabulate(output_dir, md, -1)


if __name__ == "__main__":
    main()
