# Experimental Nanopore FASTQ generator (NanoEx-Gen)

The purpose of this code is to generate a simulated FASTQ file by utilizing the read lengths extracted from an experimental FASTQ file and randomly selecting sequences from a provided reference genome. The generated reads carry equivalent lengths to the experimental reads, though originating from random positions within the reference genome. Additionally, it incorporates the error profile from real Oxford Nanopore Technology (ONT) DNA sequencing reads to to render the simulation more suitable for simulating a close to real simulation.

## Dependencies

To run `nanoexgen.py`, you will need the following dependencies:

- Python 3
- pysam

To install these dependencies, you can use pip:

```bash
pip install pysam
```

## Input Preparation
1. Experimental FASTQ File:
- A FASTQ file with ONT DNA sequencing reads from an experiment.
2. Reference Genome:
- A FASTA file of the reference genome from which you wish to simulate reads.
3. Aligned BAM File:
- A BAM file containing the alignment of the experimental FASTQ reads against the reference genome. 
- This file helps in deriving the error profile for the simulation.
- Obtain this by aligning the experimental FASTQ to the reference genome using tools like minimap2.
4. BAM Index File:
- The BAM file's corresponding index file (typically with a .bai extension). **It should be in the same directory as the BAM file**.


## Usage

Run the script using the following command:

```bash
./nanoexgen.py /path/to/infile path/to/ref_g path/to/aligned/bam path/to/output/simulated/fastq --seed [seed_value]

```

Specify the paths to the input FASTQ file (infile), reference genome (ref_g), the aligned BAM file (bam_file), and the desired location for the simulated FASTQ file (output_simulated_fastq). Optionally, provide a seed value (can be any integer) using --seed.


Example:

```bash
./nanoexgen.py /path/to/experimental_data.fq /path/to/reference_genome.fasta /path/to/aligned_data.bam /path/to/output/simulated_fastq.fq --seed 12345

```

To run the script, you would use a command like:

If you're using a UNIX-based system, execute permissions with:

```bash
chmod +x nanoexgen.py
```
## Functions

- **readfq(fp)**: Generator function to read sequences from FASTQ files.
- **extract_error_profile(bam_file)**: Extracts the error profile from the aligned BAM file.
- **introduce_errors(sequence, error_profile)**: Applies the error profile to a sequence.
- **generate_simulated_fastq(infile, ref_g, output_file, bam_file, seed=519)**: Generates the simulated FASTQ file using the experimental data, reference genome, and error profile. The reference genome is loaded into memory, and subsequently, for each read in the experimental data, a position in the reference genome is randomly chosen. From this position, a sequence of equal length is extracted. The newly generated sequence, along with the original header and quality scores, is recorded and saved in the newly created FASTQ file.

## Acknowledgments

Sections of this code were adopted from:
- [readfq](https://github.com/lh3/readfq)
- [NanoSim](https://github.com/bcgsc/NanoSim/)

It's always good practice to acknowledge and attribute the original sources when utilizing or modifying code.

## Citation

If you use this code in your research, please cite:

```less
[Byeongyeon Cho], Experimental Nanopore FASTQ generator (NanoEx-Gen), GitHub repository, [2023].
URL: [https://github.com/tedblry/NanoEx-Gen]
```

```arduino
This README now provides complete information about setting up, preparing inputs, and using the `nanoexgen.py` script.
```


