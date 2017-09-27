# -*- coding: utf-8 -*-
import sys

# Mandarin.dat: reference word to pinyin dictionary file
# ------------  with data format as:
# ------------                        3454      XU3
# ------------                        3458      JIE4
pinyindic = './Mandarin.dat'
dic = {}

with open(pinyindic) as f:
  for line in f:
    key, value = line.strip().split('\t')
    dic[key]   = value.lower().split(' ')[0]


def word2pinyin(targetstr, encoding = 'utf-8'):
  result = ''
  for i in targetstr.decode(encoding):
    unicodekey = '%X' % ord(i)
    if dic.has_key(str(unicodekey)):
      result += '%s '% dic[str(unicodekey)]
    else:
      result += i
  return result

if __name__=='__main__':
  for i in sys.argv[1:]:
    print(word2pinyin(i))

