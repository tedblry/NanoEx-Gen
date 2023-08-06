# Experimental Nanopore FASTQ generator (NanoEx-Gen)

The purpose of this code is to generate a simulated FASTQ file by utilizing the read lengths extracted from an experimental FASTQ file and randomly selecting sequences from a provided reference genome. The generated reads carry equivalent lengths to the experimental reads, though originating from random positions within the reference genome.

## Usage

Run the script using the following command:

```bash
./Rand.py path_to_infile path_to_ref_g path_to_output_simulated_fastq
```

Please specify the paths to the input FASTQ file (`infile`), reference genome (`ref_g`), and the desired output location for the simulated FASTQ file (`output_simulated_fastq`).

Example:

```bash
./nanoexgen.py /path/to/experimental_data.fq /path/to/reference_genome.fasta /path/to/output/sim06_simulated_fastq.fq
```

## Functions

- **readfq(fp)**: Generator function to read sequences from FASTQ files.
- **generate_simulated_fastq(infile, ref_g, output_file, seed=519)**: The reference genome is loaded into memory, and subsequently, for each read in the experimental data, a position in the reference genome is randomly chosen. From this position, a sequence of equal length is extracted. The newly generated sequence, along with the original header and quality scores, is recorded and saved in the newly created FASTQ file.

## Acknowledgments

Sections of this code were adopted from:
- [readfq](https://github.com/lh3/readfq)
- [NanoSim](https://github.com/bcgsc/NanoSim/)

It's always good practice to acknowledge and attribute the original sources when utilizing or modifying code.

## Citation

If you use this code in your research, please cite:

```
[Byeongyeon Cho], Experimental Nanopore FASTQ generator (NanoEx-Gen), GitHub repository, [2023].
URL: [https://github.com/tedblry/NanoEx-Gen]
```
