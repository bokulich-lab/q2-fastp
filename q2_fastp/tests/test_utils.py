# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
from unittest.mock import patch, call, MagicMock

from qiime2.plugin.testing import TestPluginBase

from q2_fastp import collate_fastp_reports
from q2_fastp.types import FastpJsonDirectoryFormat
from q2_fastp.utils import run_command


class TestUtils(TestPluginBase):
    package = "q2_fastp.tests"

    def setUp(self):
        super().setUp()
        self.reports1 = FastpJsonDirectoryFormat(
            self.get_data_path("reports/set1"), "r"
        )
        self.reports2 = FastpJsonDirectoryFormat(
            self.get_data_path("reports/set2"), "r"
        )

    @patch("subprocess.run")
    def test_run_command_without_pipe(self, mock_subprocess_run):
        cmd = ["echo", "hello"]
        run_command(cmd, verbose=False)

        mock_subprocess_run.assert_called_once_with(cmd, check=True)

    @patch("subprocess.run")
    def test_run_command_with_pipe(self, mock_subprocess_run):
        mock_result = MagicMock()
        mock_result.stdout = "mock output"
        mock_subprocess_run.return_value = mock_result

        cmd = ["echo", "hello"]
        result = run_command(cmd, pipe=True, verbose=False)

        mock_subprocess_run.assert_called_once_with(cmd, env=None, check=True, capture_output=True, text=True)
        self.assertEqual(result.stdout, "mock output")

    @patch("q2_fastp.utils.shutil.move")
    def test_collate(self, p):
        obs = collate_fastp_reports(reports=[self.reports1, self.reports2])
        self.assertIsInstance(obs, FastpJsonDirectoryFormat)
        p.assert_has_calls(
            [
                call(
                    os.path.join(str(self.reports1.path), "sample1.json"),
                    obs.path / "sample1.json",
                ),
                call(
                    os.path.join(str(self.reports1.path), "sample2.json"),
                    obs.path / "sample2.json",
                ),
                call(
                    os.path.join(str(self.reports2.path), "sample3.json"),
                    obs.path / "sample3.json",
                ),
                call(
                    os.path.join(str(self.reports2.path), "sample4.json"),
                    obs.path / "sample4.json",
                ),
            ],
            any_order=True,
        )
