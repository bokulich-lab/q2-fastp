# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import shutil
import unittest
from unittest.mock import patch, call, MagicMock, ANY

from q2_types.per_sample_sequences import CasavaOneEightSingleLanePerSampleDirFmt
from qiime2.plugin.testing import TestPluginBase

from q2_fastp.fastp import (
    _find_empty_samples,
    _remove_samples,
    _run_fastp,
    process_seqs,
)
from q2_fastp.types import FastpJsonDirectoryFormat


class TestFastp(TestPluginBase):
    package = "q2_fastp.tests"

    def setUp(self):
        super().setUp()

        self.reads_dir = os.path.join(self.temp_dir.name, "reads")
        shutil.copytree(self.get_data_path("reads"), self.reads_dir)
        self.reads = CasavaOneEightSingleLanePerSampleDirFmt(self.reads_dir, mode="r")
        self.reads_paired = CasavaOneEightSingleLanePerSampleDirFmt(
            self.get_data_path("reads-paired"), mode="r"
        )

    def test_find_empty_samples(self):
        # make sample1 empty
        os.truncate(os.path.join(self.reads_dir, "sample1_00_L001_R1_001.fastq.gz"), 0)

        empty_samples = _find_empty_samples(
            self.reads, ["sample1", "sample2", "sample3", "sample4"]
        )
        self.assertEqual(empty_samples, ["sample1"])

    def test_find_empty_samples_all(self):
        # make all samples empty
        ids = ["sample1", "sample2", "sample3", "sample4"]
        for sample in ids:
            os.truncate(
                os.path.join(self.reads_dir, f"{sample}_00_L001_R1_001.fastq.gz"), 0
            )

        with self.assertRaisesRegex(
            ValueError, "All samples are empty after processing with fastp"
        ):
            _find_empty_samples(self.reads, ids)

    def test_remove_samples(self):
        empty_samples = ["sample1"]
        _remove_samples(self.reads, empty_samples)

        # check that sample1 files are removed
        self.assertFalse(
            os.path.exists(
                os.path.join(self.reads_dir, "sample1_00_L001_R1_001.fastq.gz")
            )
        )

        # check that sample2 files still exist
        self.assertTrue(
            os.path.exists(
                os.path.join(self.reads_dir, "sample2_00_L001_R1_001.fastq.gz")
            )
        )

    @patch("q2_fastp.fastp.run_command")
    def test_run_fastp(self, mock_run_command):

        params = {
            "trim_front1": 2,
            "trim_tail1": 2,
            "trim_front2": 3,
            "trim_tail2": 3,
            "max_len2": 0,
            "adapter_sequence_r2": "",
            "cut_window_size": 4,
            "cut_mean_quality": 20,
            "n_base_limit": 5,
            "length_required": 15,
            "qualified_quality_phred": 15,
            "unqualified_percent_limit": 40,
            "thread": 1,
        }

        obs_seqs, obs_reports = _run_fastp(self.reads_paired, params)

        self.assertIsInstance(obs_seqs, CasavaOneEightSingleLanePerSampleDirFmt)
        self.assertIsInstance(obs_reports, FastpJsonDirectoryFormat)

        calls = [
            call(
                [
                    "fastp",
                    "--in1",
                    os.path.join(
                        self.reads_paired.path, f"{s}_00_L001_R1_001.fastq.gz"
                    ),
                    "--out1",
                    os.path.join(obs_seqs.path, f"{s}_00_L001_R1_001.fastq.gz"),
                    "--json",
                    os.path.join(obs_reports.path, f"{s}.json"),
                    "--html",
                    os.path.join(obs_reports.path, f"{s}.html"),
                    "--trim_front1",
                    "2",
                    "--trim_tail1",
                    "2",
                    "--cut_window_size",
                    "4",
                    "--cut_mean_quality",
                    "20",
                    "--n_base_limit",
                    "5",
                    "--length_required",
                    "15",
                    "--qualified_quality_phred",
                    "15",
                    "--unqualified_percent_limit",
                    "40",
                    "--thread",
                    "1",
                    "--in2",
                    os.path.join(
                        self.reads_paired.path, f"{s}_00_L001_R2_001.fastq.gz"
                    ),
                    "--out2",
                    os.path.join(obs_seqs.path, f"{s}_00_L001_R2_001.fastq.gz"),
                    "--trim_front2",
                    "3",
                    "--trim_tail2",
                    "3",
                    "--max_len2",
                    "0",
                ]
            )
            for s in ["sample1", "sample2"]
        ]
        mock_run_command.assert_has_calls(calls)

    @patch("q2_fastp.fastp._run_fastp")
    @patch("q2_fastp.fastp._find_empty_samples")
    @patch("q2_fastp.fastp._remove_samples")
    def test_process_seqs(self, mock_remove, mock_find_empty, mock_run):
        mock_output_seqs = MagicMock()
        mock_json_reports = MagicMock()

        mock_run.return_value = (mock_output_seqs, mock_json_reports)
        mock_find_empty.return_value = []
        mock_remove.return_value = mock_output_seqs

        output_sequences, json_reports = process_seqs(self.reads_paired)

        mock_run.assert_called_once_with(self.reads_paired, ANY)
        mock_find_empty.assert_called_once_with(
            mock_output_seqs, ["sample1", "sample2"]
        )
        mock_remove.assert_called_once_with(mock_output_seqs, [])

        self.assertIs(output_sequences, mock_output_seqs)
        self.assertIs(json_reports, mock_json_reports)


if __name__ == "__main__":
    unittest.main()
