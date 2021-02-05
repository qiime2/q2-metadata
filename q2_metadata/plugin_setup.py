# ----------------------------------------------------------------------------
# Copyright (c) 2017-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2.plugin
from qiime2.plugin import MetadataColumn, Numeric

import q2_metadata

from q2_metadata import tabulate, distance_matrix
from q2_types.distance_matrix import DistanceMatrix


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
