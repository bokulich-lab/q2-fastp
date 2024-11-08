# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import json

from qiime2.core.exceptions import ValidationError
from qiime2.plugin import model


class FastpJsonFormat(model.TextFileFormat):
    def _validate_(self, level):
        with open(self.path) as f:
            try:
                json.load(f)
            except json.decoder.JSONDecodeError:
                raise ValidationError(
                    f'"{self.path}" JSON file is not formatted correctly.'
                )


class FastpJsonDirectoryFormat(model.DirectoryFormat):
    reports = model.FileCollection(r".+\.json$", format=FastpJsonFormat)

    @reports.set_path_maker
    def reports_path_maker(self, sample_id):
        return f"{sample_id}.json"
