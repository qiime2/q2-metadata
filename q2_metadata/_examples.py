# ----------------------------------------------------------------------------
# Copyright (c) 2016-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import qiime2

epoch = qiime2.__release__
m_p_base = f'https://docs.qiime2.org/{epoch}/data/tutorials/moving-pictures/'
stats_url = m_p_base + 'demux-filter-stats.qza'


def tabulate_example(use):
    stats = use.init_artifact_from_url('demux_stats', stats_url)
    stats_md = use.view_as_metadata('stats_as_md', stats)

    viz, = use.action(
        use.UsageAction('metadata', 'tabulate'),
        use.UsageInputs(
            input=stats_md,
        ),
        use.UsageOutputNames(
            visualization='demux_stats_viz',
        )
    )

    viz.assert_output_type('Visualization')
