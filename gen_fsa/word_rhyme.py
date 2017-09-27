# -*- coding: utf-8 -*-
import word2pinyin as pinyin

word_lib = './vocabulary_library/test.txt'
def rhyme_parse(py):
  if (py[0] in 'aoeiuv'):
    rhyme      = py[:-1] 
  else:
    rhyme      = py[2:-1] if py[:2] in 'zh,ch,sh' else py[1:-1]
  return rhyme

def line_parse(line):
  word            = line.split('\t')[0].strip()
  py              = pinyin.word2pinyin(word)
  word_cnt        = len(py.split())
  last_py         = py.split()[-1].strip()
  last_rhyme      = rhyme_parse(last_py)
  if (word_cnt > 1):
    second_last_py    = py.split()[-2].strip()
    second_last_rhyme = rhyme_parse(second_last_py)
  else:
    second_last_rhyme = ''
  #print word
  return word,last_rhyme,second_last_rhyme,word_cnt
def word_rhyme(word_list=[],strict_rhyme_en=0,debug_on=0):
  word_rhyme_dict = {}
  word_double_rhyme_dict = {}
  if len(word_list) == 0:
    with open(word_lib) as wl:
      lines = [x for x in wl.readlines()]
  else:
    lines = word_list
  for line in lines:
    word, last_rhyme, second_last_rhyme, word_cnt = line_parse(line)
    if (strict_rhyme_en == 0):
      key = str(last_rhyme) 
    else:
      key = str(last_rhyme) + str(word_cnt) 
    if (debug_on == 1):
      print 'word:%s, word_rhyme:%s, word_cnt:%d ' %(str(word),str(last_rhyme),word_cnt)
    if word_rhyme_dict.has_key(key):
      word_rhyme_dict[key].append(word) 
    else:
      word_rhyme_dict[key] = []
      word_rhyme_dict[key].append(word) 
    if (last_rhyme == second_last_rhyme):
      if word_double_rhyme_dict.has_key(key):
        word_double_rhyme_dict[key].append(word) 
      else:
        word_double_rhyme_dict[key] = []
        word_double_rhyme_dict[key].append(word) 
  #for rhyme,list_word in word_rhyme_dict.items():
  #  print '%s\t'%rhyme,
  #  for word in list_word:
  #    print word,
  #  print '\n'
  return word_rhyme_dict, word_double_rhyme_dict

if __name__=='__main__':
  l = ['你','我','他','喜','哈','摸'] 
  word_rhyme(l,0)
