# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
import tempfile

from q2_types.per_sample_sequences import CasavaOneEightSingleLanePerSampleDirFmt

from .types import FastpJsonDirectoryFormat
from .utils import add_param, run_command


def process_seqs(
    sequences: CasavaOneEightSingleLanePerSampleDirFmt,
    trim_front1: int = 0,
    trim_tail1: int = 0,
    max_len1: int = 0,
    trim_front2: int = 0,
    trim_tail2: int = 0,
    max_len2: int = 0,
    disable_quality_filtering: bool = False,
    n_base_limit: int = 5,
    qualified_quality_phred: int = 15,
    unqualified_percent_limit: int = 40,
    length_required: int = 15,
    compression: int = 2,
    thread: int = 1,
    dedup: bool = False,
    dup_calc_accuracy: int = 3,
    dont_eval_duplication: bool = False,
    disable_adapter_trimming: bool = False,
    adapter_sequence: str = "",
    adapter_sequence_r2: str = "",
    poly_g_min_len: int = 10,
    poly_x_min_len: int = 10,
    overlap_len_require: int = 30,
    overlap_diff_limit: int = 5,
    overlap_diff_percent_limit: int = 20,
    correction: bool = False,
    cut_window_size: int = 4,
    cut_mean_quality: int = 20,
    cut_front: bool = False,
    cut_tail: bool = False,
    cut_right: bool = False,
    overrepresentation_analysis: bool = False,
    overrepresentation_sampling: int = 20,
) -> (CasavaOneEightSingleLanePerSampleDirFmt, FastpJsonDirectoryFormat):
    kwargs = {
        k: v
        for k, v in locals().items()
        if k
        not in [
            "sequences",
            "trim_front2",
            "trim_tail2",
            "max_len2",
            "adapter_sequence_r2",
        ]
    }
    output_sequences = CasavaOneEightSingleLanePerSampleDirFmt()
    json_reports = FastpJsonDirectoryFormat()

    with tempfile.TemporaryDirectory() as tmp:
        report_dir = os.path.join(tmp, "html_reports")
        os.makedirs(report_dir, exist_ok=True)
        for sample_id, row in sequences.manifest.iterrows():
            input_fp = row["forward"]
            output_fp = os.path.join(
                output_sequences.path, os.path.basename(row["forward"])
            )
            report_fp = os.path.join(report_dir, f"{sample_id}.html")
            json_fp = os.path.join(str(json_reports), f"{sample_id}.json")
            cmd = [
                "fastp",
                "--in1",
                input_fp,
                "--out1",
                output_fp,
                "--json",
                json_fp,
                "--html",
                report_fp,
            ]

            # add common params
            for param, value in kwargs.items():
                add_param(cmd, param, value)

            if "reverse" in row and row["reverse"] is not None:
                input_fp2 = row["reverse"]
                output_fp2 = os.path.join(
                    output_sequences.path, os.path.basename(row["reverse"])
                )
                add_param(cmd, "in2", input_fp2, "--in2")
                add_param(cmd, "out2", output_fp2, "--out2")
                add_param(cmd, "trim_front2", trim_front2)
                add_param(cmd, "trim_tail2", trim_tail2)
                add_param(cmd, "max_len2", max_len2)
                add_param(cmd, "adapter_sequence_r2", adapter_sequence_r2)

            run_command(cmd)

    return output_sequences, json_reports
