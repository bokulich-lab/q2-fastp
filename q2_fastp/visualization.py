# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import shutil
import tempfile

import pkg_resources
import q2templates

from q2_fastp.types import FastpJsonDirectoryFormat
from q2_fastp.utils import run_command

TEMPLATES = pkg_resources.resource_filename("q2_fastp", "assets")


def visualize(output_dir: str, reports: FastpJsonDirectoryFormat) -> None:
    """Visualize fastp reports."""

    with tempfile.TemporaryDirectory() as temp_dir:
        cmd = [
            "multiqc",
            str(reports.path),
            "--outdir",
            temp_dir,
            "--filename",
            "report.html",
        ]
        run_command(cmd, verbose=True)

        shutil.copy(os.path.join(TEMPLATES, "index.html"), output_dir)
        shutil.copy(os.path.join(temp_dir, "report.html"), output_dir)

    templates = [
        os.path.join(TEMPLATES, "index.html"),
    ]

    q2templates.render(templates, output_dir, context={})
