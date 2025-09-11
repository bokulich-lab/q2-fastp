# ----------------------------------------------------------------------------
# Copyright (c) 2025, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.core.exceptions import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_fastp.types import FastpJsonDirectoryFormat


class TestFormats(TestPluginBase):
    package = "q2_fastp.tests"

    def test_fastp_json_format(self):
        FastpJsonDirectoryFormat(self.get_data_path("reports/set1"), "r").validate()

    def test_fastp_json_format_corrupted(self):
        with self.assertRaisesRegex(
            ValidationError, "JSON file is not formatted correctly"
        ):
            FastpJsonDirectoryFormat(
                self.get_data_path("reports/set3-broken"), "r"
            ).validate()
