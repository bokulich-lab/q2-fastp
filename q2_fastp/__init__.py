# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from . import _version
from .fastp import process_seqs
from .utils import collate_fastp_reports
from .visualization import visualize

__version__ = _version.get_versions()["version"]
__all__ = ["collate_fastp_reports", "process_seqs", "visualize"]
