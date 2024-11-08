# ----------------------------------------------------------------------------
# Copyright (c) 2024, Bokulich Lab.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from q2_types.per_sample_sequences import (
    PairedEndSequencesWithQuality,
    SequencesWithQuality,
)
from q2_types.sample_data import SampleData
from qiime2.core.type import Bool, Int, Range, Str, TypeMap
from qiime2.plugin import Citations, Plugin

from q2_fastp import __version__
from q2_fastp.fastp import process_seqs
from q2_fastp.types import FastpJsonDirectoryFormat, FastpJsonFormat, FastpJSONReports

citations = Citations.load("citations.bib", package="q2_fastp")

plugin = Plugin(
    name="fastp",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-fastp",
    package="q2_fastp",
    description="QIIME 2 plugin for sequence processing with fastp.",
    short_description="",
)

(
    I_fastp_in,
    I_fastp_out,
) = TypeMap(
    {
        SampleData[SequencesWithQuality]: SampleData[SequencesWithQuality],
        SampleData[PairedEndSequencesWithQuality]: SampleData[
            PairedEndSequencesWithQuality
        ],
    }
)

plugin.methods.register_function(
    function=process_seqs,
    inputs={"sequences": I_fastp_in},
    parameters={
        "trim_front1": Int % Range(0, None),
        "trim_tail1": Int % Range(0, None),
        "trim_front2": Int % Range(0, None),
        "trim_tail2": Int % Range(0, None),
        "max_len1": Int % Range(0, None),
        "max_len2": Int % Range(0, None),
        "disable_quality_filtering": Bool,
        "n_base_limit": Int % Range(0, None),
        "qualified_quality_phred": Int % Range(0, None),
        "unqualified_percent_limit": Int % Range(0, 100),
        "length_required": Int % Range(0, None),
        "compression": Int % Range(1, 12),
        "thread": Int % Range(1, None),
        "dedup": Bool,
        "dup_calc_accuracy": Int % Range(0, 6, inclusive_end=True),
        "dont_eval_duplication": Bool,
        "disable_adapter_trimming": Bool,
        "adapter_sequence": Str,
        "adapter_sequence_r2": Str,
        "poly_g_min_len": Int % Range(0, None),
        "poly_x_min_len": Int % Range(0, None),
        "correction": Bool,
        "overlap_len_require": Int % Range(0, None),
        "overlap_diff_limit": Int % Range(0, None),
        "overlap_diff_percent_limit": Int % Range(0, 100),
        "cut_front": Bool,
        "cut_tail": Bool,
        "cut_right": Bool,
        "cut_window_size": Int % Range(1, None),
        "cut_mean_quality": Int % Range(0, None),
        "overrepresentation_analysis": Bool,
        "overrepresentation_sampling": Int % Range(0, 10000),
    },
    outputs=[
        ("processed_sequences", I_fastp_out),
        ("reports", FastpJSONReports),
    ],
    input_descriptions={"sequences": "Input sequences."},
    parameter_descriptions={
        "trim_front1": "Number of bases to trim from the front of forward read.",
        "trim_tail1": "Number of bases to trim from the tail of forward read.",
        "max_len1": (
            "If forward read is longer than max_len1, then trim it at its "
            "tail to make it as long as max_len1"
        ),
        "trim_front2": "Number of bases to trim from the front of reverse read.",
        "trim_tail2": "Number of bases to trim from the tail of reverse read.",
        "max_len2": (
            "If reverse read is longer than max_len2, then trim it at its "
            "tail to make it as long as max_len2"
        ),
        "disable_quality_filtering": "Disable quality filtering.",
        "n_base_limit": "The maximum number of N bases allowed in a read.",
        "qualified_quality_phred": "The quality value that a base is qualified.",
        "unqualified_percent_limit": (
            "The maximum percentage of unqualified bases " "allowed in a read."
        ),
        "length_required": "The minimum length required for a read to be kept.",
        "compression": "The compression level for the output files.",
        "thread": "The number of threads to use.",
        "dedup": "Enable duplication removal.",
        "dup_calc_accuracy": "The accuracy for duplication calculation.",
        "dont_eval_duplication": "Disable duplication evaluation.",
        "disable_adapter_trimming": "Disable adapter trimming.",
        "adapter_sequence": "The adapter sequence for read 1.",
        "adapter_sequence_r2": "The adapter sequence for read 2.",
        "poly_g_min_len": "The minimum length of polyG tail to be detected.",
        "poly_x_min_len": "The minimum length of polyX tail to be detected.",
        "correction": "Enable base correction in overlapped regions.",
        "overlap_len_require": (
            "The minimum length to detect overlapped region " "of PE reads."
        ),
        "overlap_diff_limit": (
            "The maximum number of mismatched bases to detect "
            "overlapped region of PE reads."
        ),
        "overlap_diff_percent_limit": (
            "The maximum percentage of mismatched bases "
            "to detect overlapped region of PE reads."
        ),
        "cut_window_size": (
            "The window size option shared by cut_front, cut_tail " "or cut_sliding."
        ),
        "cut_mean_quality": (
            "The mean quality requirement option shared by cut_front, "
            "cut_tail or cut_sliding."
        ),
        "cut_front": "Move a sliding window from front (5') to tail.",
        "cut_tail": "Move a sliding window from tail (3') to front.",
        "cut_right": "Move a sliding window from front to tail.",
        "overrepresentation_analysis": "Enable overrepresentation analysis.",
        "overrepresentation_sampling": (
            "The sampling number for overrepresentation analysis. Smaller is slower."
        ),
    },
    output_descriptions={
        "processed_sequences": "Sequences processed by fastp.",
        "reports": "Fastp JSON reports.",
    },
    name="Process sequences with fastp.",
    description="This method uses fastp to process input sequences with various "
    "quality control options.",
    citations=[],
)

plugin.register_formats(
    FastpJsonFormat,
    FastpJsonDirectoryFormat,
)
plugin.register_semantic_types(FastpJSONReports)
plugin.register_semantic_type_to_format(
    FastpJSONReports, artifact_format=FastpJsonDirectoryFormat
)
