# -*- coding: utf-8 -*-
import logging
import gensim
import os 
import sys
reload (sys)
sys.setdefaultencoding('utf8')
if __name__ == '__main__':
  #program = os.path.basename(sys.argv[0])
  #ogger = logging.getLogger(program)
  #logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
  model = gensim.models.Word2Vec.load('wiki.zh.text.model')
  print 'model load successfully! ...'
  print 'find the similar word...... ...'
  result = model.most_similar(u'足球',[],1000)
  for e in result:
    #logger.info("most similar word is %s, probability is %d"%(e[0],e[1]))
    print e[0], e[1]
