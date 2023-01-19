# ----------------------------------------------------------------------------
# Copyright (c) 2016-2022, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


stats_url = ('https://data.qiime2.org/usage-examples/'
             'moving-pictures/demux-filter-stats.qza')
faith_pd_url = ('https://data.qiime2.org/usage-examples/moving-pictures/'
                'core-metrics-results/faith_pd_vector.qza')

metadata_url = ('https://data.qiime2.org/usage-examples/'
                'moving-pictures/sample-metadata.tsv')


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


def tabulate_multiple_files_example(use):
    md = use.init_metadata_from_url('sample-metadata', metadata_url)
    faith_pd = use.init_artifact_from_url('faith_pd_vector', faith_pd_url)
    faith_pd_as_md = use.view_as_metadata('faith_pd_as_metadata', faith_pd)

    merged = use.merge_metadata('merged', md, faith_pd_as_md)

    use.comment(
        "Multiple metadata files or artifacts viewed as metadata can be merged"
        " to make one tabular visualization. "
        "This one displays only 25 metadata rows per page."
    )
    viz, = use.action(
        use.UsageAction('metadata', 'tabulate'),
        use.UsageInputs(
            input=merged,
            page_size=25,
        ),
        use.UsageOutputNames(
            visualization='demux_stats_viz',
        )
    )

    viz.assert_output_type('Visualization')
