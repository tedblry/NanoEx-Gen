#!/usr/bin/env python3

import argparse
import random
import os

def readfq(fp):
    """
    Read sequences from FASTQ files.
    Adopted from: https://github.com/lh3/readfq

    Parameters:
    - fp: file pointer to the FASTQ file

    Yields:
    - name: sequence name/header
    - seq: sequence
    - qual: quality score (or None if absent)
    """
    last = None  
    while True:  
        if not last:
            for line in fp:
                if line[0] in '>@':
                    last = line.strip()
                    break

        if not last:
            break

        name, seqs, last = last[1:], [], None
        for line in fp:
            if line[0] in '@+>':
                last = line.strip()
                break
            seqs.append(line.strip())

        if not last or last[0] != '+':
            yield name, ''.join(seqs), None
        else:
            seq, leng, seqs = ''.join(seqs), 0, []
            for line in fp:
                seqs.append(line.strip())
                leng += len(line.strip())
                if leng >= len(seq):
                    yield name, seq, ''.join(seqs)
                    break


def generate_simulated_fastq(infile, ref_g, output_file, seed=519):
    """
    Generate simulated FASTQ file using lengths of reads from an experimental FASTQ file and sequences 
    randomly selected from a reference genome.
    Adopted from: https://github.com/bcgsc/NanoSim/

    Parameters:
    - infile: Path to the input FASTQ file
    - ref_g: Path to the reference genome file
    - output_file: Path to the output simulated FASTQ file
    - seed: Random seed for reproducibility (default: 519)
    """
    with open(ref_g, 'r') as f:
        ref_sequence = ''.join([line.strip() for line in f.readlines()[1:]])

    random.seed(seed)

    # Create the directory if it doesn't exist
    output_directory = os.path.dirname(output_file)
    if output_directory and not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(output_file, 'w') as out_f, open(infile, 'r') as in_f:
        for seq_name, seq, qual in readfq(in_f):
            start = random.randint(0, len(ref_sequence) - len(seq))
            new_seq = ref_sequence[start:start + len(seq)]

            # If the sequence length is 0, skip writing this entry
            if len(new_seq) == 0:
                continue

            # Adjust the length of the quality string to match the length of the simulated sequence
            if len(new_seq) > len(qual):
                # Extend the quality string by repeating the last character
                qual += qual[-1] * (len(new_seq) - len(qual))
            else:
                # Truncate the quality string
                qual = qual[:len(new_seq)]

            out_f.write(f"@{seq_name}\n{new_seq}\n+\n{qual}\n")

def main():
    parser = argparse.ArgumentParser(description="Generate a simulated FASTQ file from experimental reads.")
    parser.add_argument("infile", help="Input FASTQ file path.")
    parser.add_argument("ref_g", help="Reference genome file path.")
    parser.add_argument("output_simulated_fastq", help="Output simulated FASTQ file path.")
    args = parser.parse_args()

    generate_simulated_fastq(args.infile, args.ref_g, args.output_simulated_fastq)


if __name__ == "__main__":
    main()
