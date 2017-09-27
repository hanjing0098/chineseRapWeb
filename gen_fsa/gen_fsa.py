# -*- coding: utf-8 -*-
import sys
import random
import word_rhyme as rhyme
global out
def vocb2word(vocb_l):
  word_dict = {}
  v_cnt     = 0
  for v in vocb_l:
    key = 'W%0d'%v_cnt
    word_dict[key]=str(v)
    v_cnt = v_cnt + 1
  return word_dict

def find_rhyme(rhym_vocb, rhym_key_list, line_num):
  max_length = 0
  lkeys=[key for key in rhym_key_list if (rhym_vocb.has_key(key) and len(rhym_vocb[key])> line_num)] 
  #for key in lkeys:
  #    print "key is %s"%key
  if len(lkeys) == 0:
    for key in rhym_vocb.keys():
      if (len(rhym_vocb[key]) > max_length):
        max_key    = key
        max_length = len(rhym_vocb[key])
    key_select = max_key
  else:
    #key_select = random.choice(lkeys)  
    key_select = lkeys[0] 
  return key_select, rhym_vocb[key_select] 

def state_trans_print(src_state,tar_state,word):
  #print '(%s (%s %s))'%(src_state,tar_state,word)
  global out
  out.write('(%s (%s %s))'%(src_state,tar_state,word) + '\n')

def index2str(index):
  if (index > 9):
    index_str = '0' + str(index)
  else:
    index_str = '0' + str(index)
  
  return index_str
def word_len_cal(word):
  return len(word.decode('utf-8'))

def normal_state_trans(vocb_l,line_index_str,word_index):
  for trans_word in vocb_l:
    state_trans_print('L%sW%s'%(line_index_str,index2str(word_index-1)),'L%sW%s'%(line_index_str,index2str(word_index)),str(trans_word))

def state_trans_log(line_index, word_index, trans_word):
  word_len = word_len_cal(trans_word)
  #print 'word_len = %d'%word_len
  state_trans_print('L%sW%s'%(line_index,index2str(word_index)),'L%sW%s'%(line_index,index2str(word_index+word_len)),trans_word)

def one_word_sentence_handle(word_index, trans_word, alliter_en, rhym_key):
  py = rhyme.pinyin.word2pinyin(trans_word.strip())
  if (alliter_en == 1):
    first_rhyme = rhyme.rhyme_parse(py.split()[0].strip())
    if (first_rhyme == rhym_key):
      log_flag = 1
    else:
      log_flag = 0
  else:
    log_flag = 1
  
  return log_flag

def vari_word_len_handle(word_num_line, line_index_str, word_index, trans_word, alliter_en, rhym_key):
  if (word_len_cal(trans_word) < (word_num_line-word_index)):
    state_trans_log(line_index_str, word_index, trans_word)
  elif (word_len_cal(trans_word) == (word_num_line-word_index)):
    log_flag = one_word_sentence_handle(word_index, trans_word, alliter_en, rhym_key) 
    if (log_flag == 1):
      state_trans_log(line_index_str, word_index, trans_word)

def line_process(vocb_l, rhym_l, double_rhym_l, line_index_str, word_num_line, alliter_en, dbet_en, rhym_key):
  state_trans_print('L%sSTART'%line_index_str,'L%sW00'%line_index_str, '*e*')
  if (dbet_en == 1):
    rhym_tr = double_rhym_l
  else:
    rhym_tr = rhym_l
  #gen each word in line
  word_num_str = index2str(word_num_line)
  for word_index in range(word_num_line):
    word_index_str = index2str(word_index)
    if (word_index == 0):
      if (dbet_en == 1):
        for trans_word in rhym_l:
          if (word_len_cal(trans_word) == 1):
            state_trans_log(line_index_str, word_index, trans_word)
      for trans_word in rhym_tr:
        vari_word_len_handle(word_num_line, line_index_str, word_index, trans_word, alliter_en, rhym_key)
    elif (word_index == 1):
      if (dbet_en == 1):
        for trans_word in rhym_l: 
          vari_word_len_handle(word_num_line, line_index_str, word_index, trans_word, alliter_en, rhym_key)
      else:
        for trans_word in vocb_l:
          vari_word_len_handle(word_num_line, line_index_str, word_index, trans_word, alliter_en, rhym_key)
    elif (word_index == (word_num_line-1)):
      if (alliter_en == 1):
        for trans_word in rhym_l:
          if (word_len_cal(trans_word) == 1):
            state_trans_log(line_index_str, word_index, trans_word)
      else:
        for trans_word in vocb_l:
          if (word_len_cal(trans_word) == 1):
            state_trans_log(line_index_str, word_index, trans_word)
    else:
      for trans_word in vocb_l:
        vari_word_len_handle(word_num_line, line_index_str, word_index, trans_word, alliter_en, rhym_key)
  state_trans_print('L%sW%s'%(line_index_str, word_num_str),'L%sEND'%line_index_str, '*e*')

def vocab_sort(vocab, vocb_topic):
  vocab_list = []
  vocab = sorted(vocab.items(), key=lambda x: x[1], cmp=lambda x,y:cmp(max([vocb_topic[i] for i in x]),max([vocb_topic[j] for j in y])), reverse=True)
  for x,y in vocab:
    vocab_list.append(x)
  return vocab_list

def rhym_select(doublebet_en, rhym_vocb, rhym_key_list, double_rhym_vocb, double_rhym_key_list, line_num):      
  if (doublebet_en == 1):
    if (double_rhym_vocb is None):
      #double_rhym_l = [] 
      dbet_en = 0
      rhym_key_a, rhym_a  = find_rhyme(rhym_vocb, rhym_key_list, line_num) 
      double_rhym_a       = rhym_a
      rhym_vocb.pop(rhym_key_a,None)
      rhym_key_b, rhym_b  = find_rhyme(rhym_vocb, rhym_key_list, line_num) 
      double_rhym_b       = rhym_b
      print 'Warning: there is no double rhyme word related to topic word'
    else:
      dbet_en = 1
      rhym_key_a, double_rhym_a  = find_rhyme(double_rhym_vocb, double_rhym_key_list, line_num) 
      rhym_a                     = rhym_vocb[rhym_key_a]
      double_rhym_vocb.pop(rhym_key_a,None)
      if (double_rhym_vocb is None):
        print 'Warning: there is not enough double rhyme word related to topic word, let b=a'
        rhym_key_b    = rhym_key_a
        rhym_b        = rhym_a
        double_rhym_b = double_rhym_a
      else:
        rhym_key_b, double_rhym_b  = find_rhyme(double_rhym_vocb, double_rhym_key_list, line_num) 
        rhym_b                     = rhym_vocb[rhym_key_b]
  else: 
    dbet_en = 0
    double_rhym_a = [] 
    double_rhym_b = [] 
    rhym_key_a, rhym_a  = find_rhyme(rhym_vocb, rhym_key_list, line_num) 
    rhym_vocb.pop(rhym_key_a,None)
    rhym_key_b, rhym_b  = find_rhyme(rhym_vocb, rhym_key_list, line_num) 
  
  return dbet_en, rhym_key_a, rhym_a, double_rhym_a, rhym_key_b, rhym_b, double_rhym_b 

def gen_fsa(vocb_topic, vocb_all, output, source_file, mode=0, line_num=4, word_num=7, alliter_en=0, doublebet_en=0, fix_word_num=1, variance=2):
  """
  Args:
    vocb_l: related word vocabulary
    mode  : rap mode, 0->aaaa; 1->abab; 2->aabb
    line_num: expected line_num in each paragraph
    aliter_en: 0->disable; 1->enable
    doublebet_en: 0-> 单押; 1->双押
  """
  global out
  if (mode >= 3):
    print 'mode should less than 3: 0-> aaaa; 1-> abab; 2-> aabb'
    raise ValueError
  out = open(output, 'w')
  src = open(source_file, 'w')
  #get rhym list
  double_rhym_l     = [] 
  rhym_l            = [] 
  rhym_key_l        = []
  double_rhym_l     = [] 
  double_rhym_key_l = [] 
  rhym_vocb, double_rhym_vocb = rhyme.word_rhyme(vocb_topic.keys())
  rhym_key_l        = vocab_sort(rhym_vocb, vocb_topic)
  double_rhym_key_l = vocab_sort(double_rhym_vocb, vocb_topic)

  dbet_en, rhym_key_a, rhym_a, double_rhym_a, rhym_key_b, rhym_b, double_rhym_b = rhym_select(doublebet_en, rhym_vocb, rhym_key_l, double_rhym_vocb, double_rhym_key_l, line_num)
  
  #gen end state
  #print 'END'
  out.write('END \n')
  #START -> L00START
  state_trans_print('START','L00START','*e*')
  #gen each line
  rhym_cnt = 0
  for line_index in range(line_num):
    if (rhym_cnt == 3):
      rhym_cnt = 0
    else:
      rhym_cnt = rhym_cnt + 1
    line_index_str = index2str(line_index)
    if (fix_word_num == 1):
      word_num_line = word_num
    else:
      word_num_line = random.randint(word_num-variance,word_num+variance)
    if (mode == 0): ##aaaa
      doublt_rhym_l   = double_rhym_a
      rhym_l          = rhym_a
      rhym_key        = rhym_key_a 
    elif (mode == 1): ##abab
      if (line_index % 2 == 0):
        doublt_rhym_l   = double_rhym_a
        rhym_l          = rhym_a
        rhym_key        = rhym_key_a 
      else:
        doublt_rhym_l   = double_rhym_b
        rhym_l          = rhym_b
        rhym_key        = rhym_key_b 
    elif (mode == 2): ##aabb
      if (rhym_cnt < 2):
        doublt_rhym_l   = double_rhym_a
        rhym_l          = rhym_a
        rhym_key        = rhym_key_a 
      else:
        doublt_rhym_l   = double_rhym_b
        rhym_l          = rhym_b
        rhym_key        = rhym_key_b 
    #sorted rhym_l and doublt_rhym_l according to word2vec score
    rhym_l        = sorted(rhym_l, key=lambda x:vocb_topic[x], reverse=True)
    doublt_rhym_l = sorted(doublt_rhym_l, key=lambda x:vocb_topic[x], reverse=True)
    if (dbet_en == 1):
      #rhym_word = random.choice(doublt_rhym_l) 
      rhym_word = doublt_rhym_l[line_index]
      #src.write(random.choice(doublt_rhym_l) + ' ')
    else:
      rhym_word = rhym_l[line_index]
      #rhym_word = random.choice(rhym_l) 
    src.write(rhym_word + ' ')
    ##check me TODO
    #rhym_l        = [rhym_word]
    #double_rhym_l = [rhym_word]
    line_process(vocb_all, rhym_l, double_rhym_l, line_index_str, word_num_line, alliter_en, dbet_en,rhym_key)
    #line->line
    if (line_index == (line_num - 1)):
      state_trans_print('L%sEND'%line_index_str,'PREEND','.')
      state_trans_print('PREEND','END','<EOF>')
    else:
      state_trans_print('L%sEND'%line_index_str,'L%sSTART'%index2str(line_index+1),',')
  out.close()
  src.close()
      
if __name__=='__main__':
  vocb_topic = ['你好','嘻嘻','哈哈','笑笑','下雨','米采奕奕'] 
  vocb_all   = ['你好','嘻嘻','哈哈','笑笑','下雨','米采奕奕'] 
  gen_fsa(vocb_topic,vocb_all,'fsa.txt','source.txt',2,4,4,0)
         
        
        
   
  

