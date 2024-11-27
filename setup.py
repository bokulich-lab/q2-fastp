# ----------------------------------------------------------------------------
# Copyright (c) 2022, <developer name>.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

import versioneer

setup(
    name="q2-fastp",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license="BSD-3-Clause",
    packages=find_packages(),
    author="Michal Ziemski",
    author_email="ziemski.michal@gmail.com",
    description="QIIME 2 plugin for fastp.",
    url="https://github.com/bokulich-lab/q2-fastp",
    entry_points={"qiime2.plugins": ["q2-fastp=q2_fastp.plugin_setup:plugin"]},
    package_data={
        "q2_fastp": ["citations.bib", "assets/*"],
    },
    zip_safe=False,
)
