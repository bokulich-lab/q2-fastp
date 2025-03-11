# q2-fastp
![CI](https://github.com/bokulich-lab/q2-fastp/actions/workflows/ci.yaml/badge.svg)
![QIIME CI](https://github.com/bokulich-lab/q2-fastp/actions/workflows/ci-dev.yaml/badge.svg)
[![codecov](https://codecov.io/gh/bokulich-lab/q2-fastp/graph/badge.svg?token=PSCAYJUP01)](https://codecov.io/gh/bokulich-lab/q2-fastp)

# Installation
To install q2-fastp you will need an existing QIIME 2 conda environment. You can follow the steps described in the QIIME 2 installation instructions for the amplicon or moshpit distribution to create one. Once done, you can install q2-fastp as follows (we will use the moshpit distribution in this example):

```shell
conda activate moshpit-dev
```

Install the required dependencies:
```shell
mamba install -c bioconda -c conda-forge -c default fastp multiqc
```

Install q2-fastp:
```shell
pip install git+https://github.com/bokulich-lab/q2-fastp
```

Refresh cache and check if the plugin is available:
```shell
qiime dev refresh-cache
qiime fastp --help
```
