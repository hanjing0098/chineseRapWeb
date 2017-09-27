# -*- coding: utf-8 -*-
import codecs
import jieba
import sys
import gen_fsa as fsa

if __name__=='__main__':
  vocab_l = []
  f = codecs.open('test_fsa.txt', 'r', encoding='utf-8')
  line = f.readline()
  while line:
    seg_list = jieba.cut(line, cut_all=False)
    for x in seg_list:
      if (x.strip() != ''):
        vocab_l.append(x.strip().encode('utf-8'))
    line = f.readline()
  f.close()
  #print vocab_l
  fsa.gen_fsa(vocab_l,"fsa.loog",2,4,4,0,0)
