# -*- coding: utf-8 -*-
#
# Copyright @ CangTu.
#
# 16-10-9 下午3:23 licangtu@gmail.com
#
# Distributed under terms of the MIT License
import re
import uuid
from Bio.Seq import Seq


PATTERN = re.compile(r'[ATCG]{21}GG', re.IGNORECASE)


class Cas9(object):
    def __init__(self, cid, seq):
        """
        :param cid: the ID of this sequence
        :param seq: the sequence of this gRNA
        """
        self.cid = cid
        self.seq = seq

    def __repr__(self):
        return '<Cas9 %s>' % self.cid

    def __len__(self):
        return len(self.seq) if self.seq else 0

    @classmethod
    def from_seq(cls, seq, sid=None):
        rc_seq = str(Seq(seq).reverse_complement())  # reverse complement sequence
        sid = sid if sid else uuid.uuid4().hex  # sequence id
        cas9_list = []

        mo = PATTERN.search(seq)  # match object
        while mo:
            pos = mo.start() + 1
            cs = mo.group()  # cas9 sequence
            cas9_list.append(cls('%s__%s__1' % (sid, pos), cs))
            mo = PATTERN.search(seq, pos=pos)

        # reverse complement sequence
        rc_mo = PATTERN.search(rc_seq)
        while rc_mo:
            pos = rc_mo.start() + 1
            cs = rc_mo.group()
            cas9_list.append(cls('%s__%s__-1' % (sid, pos), cs))
            rc_mo = PATTERN.search(rc_seq, pos=pos)

        return cas9_list

    @classmethod
    def from_gene(cls, gene_id, seq):
        return cls.from_seq(seq, gene_id)

    def serialize(self):
        return '%s,%s\n' % (self.cid, self.seq)
