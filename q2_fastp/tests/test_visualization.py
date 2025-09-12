# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import unittest
from unittest.mock import patch, MagicMock, ANY

from qiime2.plugin.testing import TestPluginBase

from q2_fastp import visualize
from q2_fastp.types import FastpJsonDirectoryFormat
from q2_fastp.visualization import TEMPLATES


class TestVisualization(TestPluginBase):
    package = "q2_fastp.tests"

    def setUp(self):
        super().setUp()

        self.reports = FastpJsonDirectoryFormat(
            self.get_data_path("reports/set1"), mode="r"
        )

    @patch("tempfile.TemporaryDirectory")
    @patch("q2_fastp.visualization.run_command")
    @patch("q2templates.render")
    @patch("shutil.copy")
    def test_visualize(self, mock_copy, mock_render, mock_run_command, mock_tempdir):
        mock_temp_instance = MagicMock()
        mock_temp_instance.name = "mock_temp_dir"
        mock_tempdir.return_value.__enter__.return_value = mock_temp_instance

        visualize(self.temp_dir.name, self.reports)

        mock_run_command.assert_called_once_with(
            [
                "multiqc",
                str(self.reports),
                "--outdir",
                ANY,
                "--filename",
                "report.html",
            ],
            verbose=True,
        )

        self.assertEqual(mock_copy.call_count, 2)

        mock_render.assert_called_once_with(
            [os.path.join(TEMPLATES, "index.html")], self.temp_dir.name, context={}
        )


if __name__ == "__main__":
    unittest.main()
