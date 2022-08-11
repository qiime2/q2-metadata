# ----------------------------------------------------------------------------
# Copyright (c) 2017-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin
from qiime2.plugin import (MetadataColumn, Numeric, SemanticType, Categorical,
                           Int, Str)
import qiime2.plugin.model as model

import q2_metadata

from q2_metadata import tabulate, distance_matrix, random_groups
from q2_types.distance_matrix import DistanceMatrix
from q2_types.sample_data import SampleData

import pandas as pd


plugin = qiime2.plugin.Plugin(
    name='metadata',
    version=q2_metadata.__version__,
    website='https://github.com/qiime2/q2-metadata',
    package='q2_metadata',
    user_support_text=None,
    citation_text=None,
    description=('This QIIME 2 plugin provides functionality for working with '
                 'and visualizing Metadata.'),
    short_description='Plugin for working with Metadata.'
)

plugin.methods.register_function(
    function=distance_matrix,
    inputs={},
    parameters={'metadata': MetadataColumn[Numeric]},
    parameter_descriptions={'metadata': 'Numeric metadata column to compute '
                                        'pairwise Euclidean distances from'},
    outputs=[('distance_matrix', DistanceMatrix)],
    name='Create a distance matrix from a numeric Metadata column',
    description='Create a distance matrix from a numeric metadata column. '
                'The Euclidean distance is computed between each pair of '
                'samples or features in the column.\n\n'
                'Tip: the distance matrix produced by this method can be used '
                'as input to the Mantel test available in `q2-diversity`.'
)

plugin.visualizers.register_function(
    function=tabulate,
    inputs={},
    parameters={
        'input': qiime2.plugin.Metadata,
        'page_size': qiime2.plugin.Int,
    },
    parameter_descriptions={
        'input': 'The metadata to tabulate.',
        'page_size': 'The maximum number of Metadata records to display '
                     'per page',
    },
    name='Interactively explore Metadata in an HTML table',
    description='Generate a tabular view of Metadata. The output '
                'visualization supports interactive filtering, sorting, and '
                'exporting to common file formats.',
)

ArtificialGrouping = \
    SemanticType('ArtificialGrouping', variant_of=SampleData.field['type'])

plugin.register_semantic_types(ArtificialGrouping)

class ArtificialGroupingFormat(model.TextFileFormat):
    def _validate(self, n_records=None):
        with self.open() as fh:
            # validate header
            line = fh.readline()
            line.startswith('sample-id')

            # validate body
            n_header_fields = len(line.split('\t'))
            for line_number, line in enumerate(fh, start=2):
                n_fields = len(line.split('\t'))
                if n_fields != n_header_fields:
                    raise ValidationError(
                        'Inconsistent number of tab-separated text fields.')
                if n_records is not None and (line_number - 1) >= n_records:
                    break

    def _validate_(self, level):
        record_count_map = {'min': 5, 'max': None}
        self._validate(record_count_map[level])


ArtificialGroupingDirectoryFormat = model.SingleFileDirectoryFormat(
    'ArtificialGroupingDirectoryFormat', 'artificial-groupings.tsv',
    ArtificialGroupingFormat)

plugin.register_formats(ArtificialGroupingFormat,
                        ArtificialGroupingDirectoryFormat)

plugin.register_semantic_type_to_format(
    SampleData[ArtificialGrouping],
    artifact_format=ArtificialGroupingDirectoryFormat)

@plugin.register_transformer
def _1(df: pd.DataFrame) -> (ArtificialGroupingFormat):
    ff = ArtificialGroupingFormat()
    with ff.open() as fh:
        df.to_csv(fh, sep='\t', header=True)
    return ff

@plugin.register_transformer
def _2(ff: ArtificialGroupingFormat) -> (qiime2.Metadata):

    with ff.open() as fh:
        df = pd.read_csv(fh, sep='\t', header=0, dtype='str', index_col=0)
        df.index.name = 'sample-id'
        return qiime2.Metadata(df)

plugin.methods.register_function(
    function=random_groups,
    inputs={},
    parameters={'metadata': MetadataColumn[Categorical],
                'n_columns': Int,
                'column_name_prefix': Str,
                'column_value_prefix': Str},
    parameter_descriptions={
        'metadata': ('Categorical metadata column to model randomized '
                     'metadata on.'),
        'n_columns': 'The number of randomized metadata columns to create.',
        'column_name_prefix': ('Prefix to use in naming the randomized '
                               'metadata columns.'),
        'column_value_prefix': ('Prefix to use in name the values in the '
                                'randomized metadata columns.')},
    output_descriptions={
        'random_groupings': 'Randomized metadata columns'
    },
    outputs=[('random_groupings', SampleData[ArtificialGrouping])],
    name='Create randomized categorical sample metadata column(s).',
    description=('Create one or more randomized categorical sample metadata '
                 'columns, with the number of groups and the count of '
                 'samples assigned to each group matching that of the '
                 'input metadata column. These data will be written to '
                 'an artifact that can be used as sample metadata.')
)