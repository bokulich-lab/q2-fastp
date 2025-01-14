# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import unittest

from q2_types.per_sample_sequences import CasavaOneEightSingleLanePerSampleDirFmt
from qiime2.plugin.testing import TestPluginBase

from q2_fastp import process_seqs


class TestFastp(TestPluginBase):
    package = "q2_fastp.tests"

    def setUp(self):
        self.input_sequences = CasavaOneEightSingleLanePerSampleDirFmt(
            self.get_data_path("reads_in"), "r"
        )
        # self.output_sequences = CasavaOneEightSingleLanePerSampleDirFmt()

    def test_run_fastp(self):
        output_sequences, reports = process_seqs(
            self.input_sequences,
            trim_front1=2,
            trim_tail1=2,
            cut_window_size=4,
            cut_mean_quality=20,
            n_base_limit=5,
            length_required=15,
            qualified_quality_phred=15,
            unqualified_percent_limit=40,
            thread=1,
        )

        # Check if output files are created
        for i in range(1, 4):
            output_fp = os.path.join(output_sequences.path, f"sample{i}.fastq.gz")
        #     self.assertTrue(os.path.exists(output_fp))
        #
        # # Check if the output files are not empty
        # for i in range(1, 4):
        #     output_fp = os.path.join(output_sequences.path, f"sample{i}.fastq.gz")
        #     self.assertGreater(os.path.getsize(output_fp), 0)


if __name__ == "__main__":
    unittest.main()
