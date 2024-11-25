# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import glob
import os
from typing import List
from warnings import warn

from q2_types.per_sample_sequences import CasavaOneEightSingleLanePerSampleDirFmt

from .types import FastpJsonDirectoryFormat
from .utils import add_param, run_command


def _find_empty_samples(
    sequences: CasavaOneEightSingleLanePerSampleDirFmt, original_ids: List[str]
) -> List[str]:
    """Find empty samples.

    Parameters:
    sequences (CasavaOneEightSingleLanePerSampleDirFmt):
        The sequences to find empty samples within.
    original_ids (List[str]): Sample IDs for the sequences.

    Returns:
    List[str]: A list of empty samples.
    """

    empty_samples = []
    all_reads = sorted(glob.glob(os.path.join(sequences.path, "*.fastq.gz")))
    for sample_id in original_ids:
        current_sample = [x for x in all_reads if sample_id in x]
        if any(os.path.getsize(f) == 0 for f in current_sample):
            empty_samples.append(sample_id)

    if len(empty_samples) == len(original_ids):
        raise ValueError(
            "All samples are empty after processing with fastp - please check "
            "your run parameters and try again."
        )
    elif len(empty_samples) > 0:
        warn(
            "The following samples are empty after processing with fastp and will be "
            "removed from the output: %s" % ", ".join(empty_samples)
        )

    return empty_samples


def _remove_samples(
    sequences: CasavaOneEightSingleLanePerSampleDirFmt, samples: List[str]
) -> CasavaOneEightSingleLanePerSampleDirFmt:
    """Remove samples from the sequence set.

    Parameters:
    sequences (CasavaOneEightSingleLanePerSampleDirFmt):
        The sequences to remove samples from.

    Returns:
    CasavaOneEightSingleLanePerSampleDirFmt: The sequences without the empty samples.
    """
    for sample_id in samples:
        for f in glob.glob(os.path.join(sequences.path, f"{sample_id}*.fastq.gz")):
            os.remove(f)
    return sequences


def _run_fastp(sequences: CasavaOneEightSingleLanePerSampleDirFmt, params: dict):
    """Run fastp on the sequences.

    Parameters:
    sequences (CasavaOneEightSingleLanePerSampleDirFmt):
        The sequences to process.
    params (dict): The parameters to pass to fastp.
    """
    kwargs = {
        k: v
        for k, v in params.items()
        if k
        not in [
            "trim_front2",
            "trim_tail2",
            "max_len2",
            "adapter_sequence_r2",
        ]
    }

    output_sequences = CasavaOneEightSingleLanePerSampleDirFmt()
    json_reports = FastpJsonDirectoryFormat()
    for sample_id, row in sequences.manifest.iterrows():
        input_fp = row["forward"]
        output_fp = os.path.join(
            output_sequences.path, os.path.basename(row["forward"])
        )
        report_fp = os.path.join(str(json_reports), f"{sample_id}.html")
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
            add_param(cmd, "trim_front2", params["trim_front2"])
            add_param(cmd, "trim_tail2", params["trim_tail2"])
            add_param(cmd, "max_len2", params["max_len2"])
            add_param(cmd, "adapter_sequence_r2", params["adapter_sequence_r2"])

        run_command(cmd)
    return output_sequences, json_reports


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
        ]
    }

    output_sequences, json_reports = _run_fastp(sequences, kwargs)

    # remove the HTML reports
    for f in glob.glob(os.path.join(str(json_reports), "*.html")):
        os.remove(f)

    # remove the empty samples
    empty_samples = _find_empty_samples(
        output_sequences, sequences.manifest.index.tolist()
    )
    output_sequences = _remove_samples(output_sequences, empty_samples)

    return output_sequences, json_reports
