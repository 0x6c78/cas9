# -*- coding: utf-8 -*-
#
# Copyright @ 0x6c78.
#
# 16-10-20 下午1:27 0x6c78@gmail.com
#
# Distributed under terms of the MIT License
from operator import mul
from itertools import combinations


class Score(object):
    def __init__(self):
        """
        张峰实验室通过实验获得的每个位置错配的特异性，具体参考网页:
        http://crispr.mit.edu/about
        """
        self.m = (0, 0, 0.014, 0, 0, 0.395, 0.317, 0, 0.389, 0.079, 0.445,
                  0.508, 0.613, 0.851, 0.732, 0.828, 0.615, 0.804, 0.685, 0.583)

    def _t1(self, locs):
        """
        :param locs: 失配的位置
        :return: 公式第一部分的值
        """
        return reduce(mul, [1-self.m[loc] for loc in locs])

    @staticmethod
    def _t2(locs):
        """
        :param locs: 失配的位置, 由于没有失配就没有mean pairwise distance，故locs的length至少为1
        :return: 公式第二部分的值
        """
        if len(locs) == 1:
            return 1.000
        else:
            locs = sorted(locs)
            length = len(locs)
            mpd = (locs[-1] - locs[0]) / (length - 1)  # mean pairwise distance
            return 1 / (((19 - mpd) / 19) * 4 + 1)

    @staticmethod
    def _t3(m):
        """
        :param m: 失配碱基的个数
        :return: 公式第三部分的值
        """
        return 1 / (m ** 2)

    def get(self, locs):
        if len(locs) == 0:
            return 100.000
        elif len(locs) == 1:
            return round(100 * self._t1(locs), 3)
        else:
            return round(100 * self._t1(locs) * self._t2(locs) * self._t3(len(locs)), 3)

    @classmethod
    def to_dict(cls):
        """
        将所有可能的错配结果对应的得分先计算好，放到一个字典里
        加速得分的计算
        :return: 一个字典，字典的键是错配的位置由下划线分割的字符串，值是得分
        """
        mm2score = {}
        pos_list = range(20)
        score = cls()

        for mm_cnt in xrange(5):
            for mm_pos_list in combinations(pos_list, mm_cnt):
                mm2score['_'.join(str(_) for _ in mm_pos_list)] = score.get(mm_pos_list)

        return mm2score
