# -*- coding: utf-8  -*-
#逐行读取文件数据进行jieba分词

import jieba
import codecs,sys


if __name__ == '__main__':
    f = codecs.open('wiki.zh.text.jian', 'r', encoding='utf8')
    target = codecs.open('wiki.zh.text.seg', 'w', encoding='utf8')
    print 'open files.'

    lineNum = 1
    line = f.readline()
    while line:
        if (lineNum % 10000) == 0:
          print '---processing ',lineNum,' article---'
        seg_list = jieba.cut(line,cut_all=False)
        line_seg = ' '.join(seg_list)
        target.writelines(line_seg)
        lineNum = lineNum + 1
        line = f.readline()

    print 'well done.'
    f.close()
    target.close()