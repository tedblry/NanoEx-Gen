# NanoEx-Gen: A Comprehensive Nanopore Sequencing Data Simulator for Bacterial Genome

NanoEx-Gen is a sophisticated Python-based pipeline designed to generate simulated FASTQ files from experimental reads. The pipeline introduces errors into the simulated reads based on the error profile extracted from the alignments of the experimental reads to a reference genome. This approach ensures that the simulated reads closely mimic the error profile of experimental Oxford Nanopore Technology (ONT) sequencing data, providing a robust tool for benchmarking and evaluating bioinformatics algorithms.

## Prerequisites

To run NanoEx-Gen, you need to have the following dependencies installed:

- Python 3
- pysam

You can install these dependencies using pip:

```
pip install pysam

```

## Input Preparation

NanoEx-Gen requires the following inputs:

1. **Experimental FASTQ File**: A FASTQ file with ONT DNA sequencing reads from an experiment.
2. **Reference Genome**: A FASTA file of the reference genome from which you wish to simulate reads.
3. **Aligned BAM File**: A BAM file containing the alignment of the experimental FASTQ reads against the reference genome. This file is used to derive the error profile for the simulation.
4. **BAM Index File**: The corresponding index file (.bai) for the BAM file. This file should be located in the same directory as the BAM file.

## Usage

You can run NanoEx-Gen using the following command:

```
./nanoexgen.py /path/to/infile /path/to/ref_g /path/to/aligned/bam /path/to/output/simulated/fastq --seed [seed_value]

```

In this command:

- Replace `/path/to/infile` with the path to your input FASTQ file.
- Replace `/path/to/ref_g` with the path to your reference genome.
- Replace `/path/to/aligned/bam` with the path to your aligned BAM file.
- Replace `/path/to/output/simulated/fastq` with the path where you want to save the simulated FASTQ file.
- Replace `[seed_value]` with an integer to set the random seed for reproducibility.

Here's an example:

```
./nanoexgen.py /path/to/experimental_data.fq /path/to/reference_genome.fasta /path/to/aligned_data.bam /path/to/output/simulated_fastq.fq --seed 12345

```

Before running the script, make sure it has execute permissions:

```
chmod +x nanoexgen.py

```

## Pipeline Workflow

NanoEx-Gen executes the following steps:

1. **Read sequences from the input FASTQ file**: For each sequence, a random start position is selected within the reference genome. If the selected start position and read length exceed the end of the reference genome, the sequence wraps around to the beginning of the genome.
2. **Extract the error profile from the BAM file**: The error profile includes the rates of mismatches, insertions, and deletions observed in the alignments.
3. **Introduce errors into the simulated reads**: For each base in the sequence, a random number is generated. If the random number is less than the mismatch rate, a mismatch is introduced. If it's less than the sum of the mismatch rate and the insertion rate, an insertion is introduced. If it's less than the sum of the mismatch rate, the insertion rate, and the deletion rate, a deletion is introduced.
4. **Write the simulated reads to the output FASTQ file**: The simulated reads with introduced errors and their corresponding quality scores are written to the output FASTQ file.

## Acknowledgments

This pipeline incorporates code from **[readfq](https://github.com/lh3/readfq)** and **[NanoSim](https://github.com/bcgsc/NanoSim/)**. We would like to acknowledge their contributions to the bioinformatics community.

## Citation

If you use NanoEx-Gen in your research, please cite:

```
[Byeongyeon Cho], Experimental Nanopore FASTQ generator (NanoEx-Gen), GitHub repository, [2023].
URL: [https://github.com/tedblry/NanoEx-Gen]

```

## Contact

For any queries or issues, please raise an issue on the GitHub repository or contact the author at [**[byeongyeon_cho@hms.harvard.edu](mailto:email_address@domain.com)**].
