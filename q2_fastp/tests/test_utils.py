# ----------------------------------------------------------------------------
# Copyright (c) 2023, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
from unittest.mock import patch, call

from qiime2.plugin.testing import TestPluginBase

from q2_fastp import collate_fastp_reports
from q2_fastp.types import FastpJsonDirectoryFormat


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
