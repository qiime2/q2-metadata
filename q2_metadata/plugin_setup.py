# ----------------------------------------------------------------------------
# Copyright (c) 2017-2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pandas as pd
from q2_types.distance_matrix import DistanceMatrix
from q2_types.sample_data import SampleData
from q2_types.metadata import ImmutableMetadata
import qiime2.plugin
from qiime2.plugin import (
    Int, Categorical, MetadataColumn, model, Numeric, Plugin, SemanticType,
    Str, Bool, Metadata, ValidationError,
)

from . import tabulate, distance_matrix, shuffle_groups, merge, __version__

plugin = Plugin(
    name='metadata',
    version=__version__,
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
    def validate(self, *args):
        try:
            md = qiime2.Metadata.load(str(self))
        except qiime2.metadata.MetadataFileError as md_exc:
            raise ValidationError(md_exc) from md_exc

        if md.column_count == 0:
            raise ValidationError('Format must contain at least 1 column')

        filtered_md = md.filter_columns(column_type='categorical')
        if filtered_md.column_count != md.column_count:
            raise ValidationError('Must only contain categorical values.')


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
    md = qiime2.Metadata(df)
    md.save(str(ff))
    return ff


@plugin.register_transformer
def _2(ff: ArtificialGroupingFormat) -> (qiime2.Metadata):
    return qiime2.Metadata.load(str(ff))


plugin.methods.register_function(
    function=shuffle_groups,
    inputs={},
    parameters={'metadata': MetadataColumn[Categorical],
                'n_columns': Int,
                'md_column_name_prefix': Str,
                'md_column_values_prefix': Str,
                'encode_sample_size': Bool
                },
    parameter_descriptions={
        'metadata': ('Categorical metadata column to shuffle.'),
        'n_columns': 'The number of shuffled metadata columns to create.',
        'md_column_name_prefix': ('Prefix to use in naming the shuffled '
                                  'metadata columns.'),
        'md_column_values_prefix': ('Prefix to use in naming the values in '
                                    'the shuffled metadata columns.'),
        'encode_sample_size': ('If true, the sample size of each metadata '
                               'group will be appended to the shuffled '
                               'metadata column values.'),
        },
    output_descriptions={
        'shuffled_groups': 'Randomized metadata columns'},
    outputs=[('shuffled_groups', SampleData[ArtificialGrouping])],
    name='Shuffle values in a categorical sample metadata column.',
    description=('Create one or more categorical sample metadata '
                 'columns by shuffling the values in an input metadata '
                 'column. To avoid confusion, the column name and values '
                 'will be derived from the provided prefixes. The number of '
                 'different values (or groups), and the counts of each value, '
                 'will match the input metadata column but the association of '
                 'values with sample ids will be random. These data will be '
                 'written to an artifact that can be used as sample metadata.')
)


plugin.methods.register_function(
    function=merge,
    inputs={},
    parameters={'metadata1': Metadata,
                'metadata2': Metadata},
    parameter_descriptions={
        'metadata1': 'First metadata file to merge.',
        'metadata2': 'Second metadata file to merge.'
    },
    outputs=[('merged_metadata', ImmutableMetadata)],
    output_descriptions={
        'merged_metadata': 'The merged metadata.'
    },
    name='Merge metadata',
    description=('Merge metadata that contains overlapping ids or overlapping '
                 'columns, but not both overlapping ids and overlapping '
                 'columns. The result will be the union (i.e., outer join) '
                 'of the ids and columns from the two metadata inputs.\n\n'
                 'Attemping to merge metadata with both overlapping ids and '
                 'overlapping columns will currently fail because we don\'t '
                 'resolve conflicting column values for a sample. '
                 'Merging metadata with neither overlapping ids or '
                 'overlapping columns is possible with this action.\n\n'
                 'To merge more than two metadata objects, run this command '
                 'multiple times, iteratively using the output of the '
                 'previous run as one of the metadata inputs.\n\n'
                 'The output, an ImmutableMetadata artifact, can be used '
                 'anywhere that a metadata file can be used, or can be '
                 'exported to a metadata tsv file in the typical format.')
)
