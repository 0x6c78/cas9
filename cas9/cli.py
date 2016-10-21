# -*- coding: utf-8 -*-
#
# Copyright @ CangTu.
#
# 16-10-9 下午4:18 licangtu@gmail.com
#
# Distributed under terms of the MIT License
from finder import Cas9
from align import batch_align
from Bio import SeqIO
from progressbar import ProgressBar


def find(input_file, out_file, fmt='fasta'):
    with open(input_file) as f:
        sr_list = SeqIO.parse(f, fmt)  # SeqRecord list
        total_sr = sum(1 for sr in sr_list)

    with open(input_file) as in_f, ProgressBar(max_value=total_sr) as pb, open(out_file, 'w') as out_f:
        cnt = 0
        sr_list = SeqIO.parse(in_f, fmt)  # SeqRecord list
        for sr in sr_list:
            cas9_list = Cas9.from_gene(sr.id, str(sr.seq))
            for cas9 in cas9_list:
                out_f.write(cas9.serialize())
            cnt += 1
            pb.update(cnt)


def align(candidate_file, bd_file, outfile):
    candidate_dict = {}
    with open(candidate_file) as handle:
        for line in handle:
            candidate_id, candidate_seq = line.rstrip().split(',')
            candidate_dict[candidate_id] = candidate_seq

    batch_align(candidate_dict, bd_file, outfile)


def main():
    import argparse

    parser = argparse.ArgumentParser(prog='cas9', description='')
    sub_parser = parser.add_subparsers(title='sub commands', dest='command')

    find_parser = sub_parser.add_parser('find', help='find cas9 target site from fasta or genbank file')
    align_parser = sub_parser.add_parser('align', help='align cas9 target to background database file')

    find_parser.add_argument('-i', '--input', help='fasta or genbank file', required=True)
    find_parser.add_argument('-o', '--output', help='where to save the results', required=True)
    find_parser.add_argument('-f', '--format', help='file format', choices=['gb', 'fasta'],
                             default='fasta', required=False)

    align_parser.add_argument('-c', '--candidate', help='candidate file', required=True)
    align_parser.add_argument('-b', '--bd', help='background database file', required=True)
    align_parser.add_argument('-o', '--outfile', help='outfile', required=True)

    args = parser.parse_args()
    if args.command == 'find':
        find(args.input, args.output, args.format)
    elif args.command == 'align':
        align(args.candidate, args.bd, args.outfile)
