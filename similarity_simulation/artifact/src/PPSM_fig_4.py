import gensim
from gensim.models import FastText
from word2keypress import Keyboard
import numpy as np
from numpy import dot
from gensim.models.utils_any2vec import _save_word2vec_format, _load_word2vec_format, _compute_ngrams, _ft_hash
from gensim import utils, matutils

THRESHOLD_LIST = [0.83,0.75,0.5]
FILE_LIST = ['../test_files/rnn_attack.txt','../test_files/su_attack.txt']
KB = Keyboard()
model = gensim.models.Word2Vec.load('../models/fastText2_keyseq_mincount:10_ngram:1-4_negsamp:5_subsamp:0.001_d:200')
model.init_sims()
def get_vector_ngram(word):
    word_vec = np.zeros(model.wv.vectors_ngrams.shape[1], dtype=np.float32)
  
    ngrams = _compute_ngrams(word, model.wv.min_n, model.wv.max_n)
    ngrams_found = 0
    
    for ngram in ngrams:
        ngram_hash = _ft_hash(ngram) % model.wv.bucket
        if ngram_hash in model.wv.hash2index:
            word_vec += model.wv.vectors_ngrams_norm[model.wv.hash2index[ngram_hash]]
        
            ngrams_found += 1
    if word_vec.any():
        return word_vec / max(1, ngrams_found)
def similarity(word1,word2):
    return dot(matutils.unitvec(get_vector_ngram(word1)), matutils.unitvec(get_vector_ngram(word2)))
print("------PPSM-------")
for th in THRESHOLD_LIST:
    
    print("Threshold:"+str(th))
    print("-------------------")
    for i in range(2):
        file_name = FILE_LIST[i]
        file_r = open(file_name,'r')
        count = 0
        ts = 0
        t = 0
        for line in file_r:
            words = line.strip().split('\t')
            word1_k = KB.word_to_keyseq(words[0])
            word2_k = KB.word_to_keyseq(words[1])
            dis =  similarity(word1_k,word2_k)
            t=t+1 
            if dis>th:
                count = count + 1
        file_r.close()
        if i == 0:
            print("True Positives-"+ str(count/t))
        else:
            print("False Positives-"+ str(count/t))