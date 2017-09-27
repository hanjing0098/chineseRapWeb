# -*- coding: utf-8 -*-
import codecs
import sys
import gensim
import gen_fsa as fsa
import argparse
import socket


host = "10.125.13.2"
port = 10000
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
parser = argparse.ArgumentParser()
parser.add_argument("-m","--mode", type = int, default=0, help="rhym mode selection -m/--mode=0(1,2)")
parser.add_argument("-ln","--linenum", type = int, default=4,  help="line number selection -ln/--linenum")
parser.add_argument("-wn","--wordnum", type = int, default=7, help="word number in one line selection -wn/--wordnum")
parser.add_argument("-al","--alli", type = int, default=0, help="enable lliteration or not -al/--alli 0(1)")
parser.add_argument("-d","--doublerhyme", type = int, default=0, help="enable double rhyme or not -d/--doublerhyme 0(1)")
parser.add_argument("-t","--topic", default='默认', help="specify the topic word -t/--topic")
parser.add_argument("-o","--fsafile", default='rap.fsa',  help="specify the fsa output file -o/-filename filename")
parser.add_argument("-s","--sourcefile", default='source.txt',  help="specify the source.txt file -o/-filename filename")

vocab_dict   = {}
vocab_all    = []

def is_chinese(word):
  for _word in word:
    if _word >= u'\u4e00' and _word <= u'\u9f5a':
      return True
    else:
      return False

def load_vocb():
  vocab_f   = open('vocab.txt', 'r')
  vocab_all = []
  for line in vocab_f.readlines():
    word = line.strip().decode('utf-8')
    if (word != '') and is_chinese(word):
      vocab_all.append(word.encode('utf-8'))
  return  vocab_all
  vocab_f.close()

def gen_vocb(result):
  for x in result:
    if (x[0].strip() != '') and (is_chinese(x[0])):
      rhym_word = x[0].strip().encode('utf-8')
      if (rhym_word in vocab_all):
        #vocab_l.append(rhym_word)
        vocab_dict[rhym_word] = x[1]

def server():
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  print 'Socket created'
  try:
    s.bind((host, port))
  except socket.error as msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
  print 'Socket bind complete'
  s.listen(0)
  while True:
    conn, addr = s.accept()
    conn.sendall('Accept')
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    data = conn.recv(1024)
    #cmd = "python run_fsa.py {}".format(data)
    args = parser.parse_args(data.split())
    word = args.topic
    print 'topic: '+word
    print data
    result = model.most_similar(args.topic.decode('utf-8'),[],1000)
    gen_vocb(result)
    print 'start gen fsa ...'
    try:
      fsa.gen_fsa(vocab_dict, vocab_all, args.fsafile, args.sourcefile, args.mode, args.linenum, args.wordnum, args.alli, args.doublerhyme)
    except:
      print '**************FSA GEN ERROR***********'
      sys.exit()
    print 'fsa done ...'
    #sp.call(cmd.split())
    result = ""
    conn.sendall(result)
    conn.close()
  s.close()

if __name__=='__main__':
  #f = codecs.open('test_fsa.txt', 'r', encoding='utf-8')
  vocab_all = load_vocb() 
  model = gensim.models.Word2Vec.load('../models/wiki.zh.model')
  print 'model load successfully! ...'
  #print vocab_l
  #socket
  server()
