# -*- coding: utf-8 -*-
#
# Copyright @ 0x6c78
#
# 16-10-20 下午1:25 0x6c78@gmail.com
#
# Distributed under terms of the MIT License
from score import Score


def align(candidate, bd):
    """
    将candidate与background database的任意一条比对，返回错配的位置
    :param candidate: candidate的序列
    :param bd: background database其中一条的序列
    :return: 如果有大于4个错配返回None，否则返回错配的位置列表
    """
    mm_pos_list = []
    cnt = 0
    for i in range(20):
        if candidate[i] != bd[i]:
            cnt += 1
            if cnt > 4:
                return None
            else:
                mm_pos_list.append(i)
    return mm_pos_list


def batch_align(candidate_dict, bd_file, outfile):
    """
    批量的比对函数
    :param candidate_dict: candidate字典，键是candidate的id，值是candidate的序列
    :param bd_file: 包含所有background database文件
    :param outfile: 保存比对结果的文件
    :return: None
    """
    bd2cnt = {}
    mm2score = Score.to_dict()
    with open(bd_file) as bd_handle:
        for line in bd_handle:
            bd, attr = line.rstrip().split(',')
            bd2cnt[bd] = attr.count(';')

    candidate_id2score = {}
    for candidate_id, candidate_seq in candidate_dict.iteritems():
        score = 0
        for bd, cnt in bd2cnt.iteritems():
            res = align(candidate_seq, bd)
            if res is not None:
                score += (mm2score['_'.join(str(_) for _ in res)] * cnt)
        candidate_id2score[candidate_id] = score

    with open(outfile, 'w') as handle:
        for candidate_id, score in candidate_id2score.iteritems():
            handle.write('%s,%s,%s\n' % (candidate_id, candidate_dict[candidate_id], score))
