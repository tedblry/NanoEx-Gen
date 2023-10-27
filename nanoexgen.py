#!/usr/bin/env python3

import argparse
import random
import os
import pysam

def readfq(fp):
    """
    Read sequences from FASTQ files.
    Adopted from: https://github.com/lh3/readfq
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

def extract_error_profile(bam_file):
    print("Extracting error profile from the BAM file...")
    samfile = pysam.AlignmentFile(bam_file, "rb")
    
    total_bases = 0
    mismatches = 0
    insertions = 0
    deletions = 0
    
    for read in samfile.fetch():
        if hasattr(read, 'seq') and read.seq:
            total_bases += len(read.seq)
            for (op, length) in read.cigar:
                if op == 1:  # insertion
                    insertions += length
                elif op == 2:  # deletion
                    deletions += length
                elif op == 4:  # soft clipping, consider these as mismatches
                    mismatches += length
                
    samfile.close()
    
    error_profile = {
        "mismatch_rate": mismatches / total_bases,
        "insertion_rate": insertions / total_bases,
        "deletion_rate": deletions / total_bases
    }
    
    return error_profile

def introduce_errors(sequence, error_profile):
    new_sequence = []
    for base in sequence:
        rand = random.random()
        if rand < error_profile['mismatch_rate']:
            new_sequence.append(random.choice('ACGT'.replace(base, '')))  # introduce a mismatch
        elif rand < error_profile['mismatch_rate'] + error_profile['insertion_rate']:
            new_sequence.append(base)
            new_sequence.append(random.choice('ACGT'))  # introduce an insertion
        elif rand < error_profile['mismatch_rate'] + error_profile['insertion_rate'] + error_profile['deletion_rate']:
            continue  # introduce a deletion
        else:
            new_sequence.append(base)
    return ''.join(new_sequence)

def generate_simulated_fastq(infile, ref_g, bam_file, output_file, seed=519):
    print("Loading the reference genome...")
    with open(ref_g, 'r') as f:
        ref_sequence = ''.join([line.strip() for line in f.readlines()[1:]])

    print("Setting the random seed...")
    random.seed(seed)

    print("Creating the output directory if it doesn't exist...")
    output_directory = os.path.dirname(output_file)
    if output_directory and not os.path.exists(output_directory):
        os.makedirs(output_directory)

    error_profile = extract_error_profile(bam_file)

    with open(output_file, 'w') as out_f, open(infile, 'r') as in_f:
        print("Generating simulated FASTQ entries...")
        
        print("Introducing errors to the sequence based on the error profile...")
        
        for seq_name, seq, qual in readfq(in_f):
            start = random.randint(0, len(ref_sequence))
            
            seq_len_over_end =  start + len(seq) - len(ref_sequence)
            #print(f"sequence length over endpoint: {seq_len_over_end}")

            if seq_len_over_end > 0:
                new_seq = ref_sequence[start:(len(ref_sequence)+1)] + ref_sequence[0:seq_len_over_end]
            else:
                new_seq = ref_sequence[start:start+len(seq)]

            if len(new_seq) == 0:
                continue

            new_seq = introduce_errors(new_seq, error_profile)
            #print(qual)

            if len(new_seq) > len(qual):
                qual += qual[-1] * (len(new_seq) - len(qual))
            else:
                qual = qual[:len(new_seq)]

            out_f.write(f"@{seq_name}\n{new_seq}\n+\n{qual}\n")

    print("Simulated FASTQ generation completed!")

def main():
    parser = argparse.ArgumentParser(description="Generate a simulated FASTQ file from experimental reads.")
    parser.add_argument("infile", help="Input FASTQ file path.")
    parser.add_argument("ref_g", help="Reference genome file path.")
    parser.add_argument("bam_file", help="Path to the BAM file with alignments of the reads to the reference genome.")
    parser.add_argument("output_simulated_fastq", help="Output simulated FASTQ file path.")
    parser.add_argument("--seed", type=int, default=519, help="Random seed for reproducibility. Default is 519.")
    args = parser.parse_args()

    print("Starting the generation process...")
    generate_simulated_fastq(args.infile, args.ref_g, args.bam_file, args.output_simulated_fastq, args.seed)
    print("Generation process completed!")

if __name__ == "__main__":
    main()
