from datasets import load_dataset
import re
import pandas as pd
import collections
from typing import List, Tuple, Dict
import os
import errno

def make_dir(path):
    try:
        os.makedirs(path, exist_ok=True)  # Python>3.2
    except TypeError:
        try:
            os.makedirs(path)
        except OSError as exc: # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else: raise

def getBigCorpus():
      file = open("big_corpus.txt", "r") 
      lines = file.readlines()
      return lines

def getMedCorpus():
      df = pd.read_csv("med_corpus.csv")
      return df["text"].to_list()

def getSmallCorpus():
      dst = load_dataset("wikitext", "wikitext-2-v1", split="test")
      corpus = []
      for i in dst["text"]:
            if(i != "" and not re.match(r" =+ .+ =+", i)):
                  if(not "=" in i):
                        corpus.append(i.strip().lower())
      return corpus

def count_ngrams(tokenized_corpus: List[List[str]], n: int, traslator = None) -> Dict[Tuple[str, ...], int]:
      ngram_counts = collections.Counter()
      for tokens in tokenized_corpus:
            for i in range(len(tokens) - n + 1):
                  if traslator == None:
                        ngram = tuple(tokens[i:i + n])
                  else:
                        ngram = tuple([traslator[token] for token in tokens[i:i + n]])
                  ngram_counts[ngram] += 1
      return ngram_counts 

def tokenize_corpus(corpus: List[str]) -> List[List[str]]: 
      return [ ['<s>'] + re.sub(r" +", " ", SimplificarSTR(sentence)).split() + ['</s>'] for sentence in corpus]

def compute_unique_context_counts(bigram_counts: Dict[Tuple[str, str], int]) -> Dict[str, int]:
      continuation_counts = collections.Counter()
      for (w_prev, w_next) in bigram_counts:
            continuation_counts[w_next] += 1
      return continuation_counts

def SimplificarSTR(input:str):
      return re.sub( r"[^a-z0-9 ]+","", input.lower(),)


def CorpusProcesador(raw : List[str], mdir: str, N = 5):
      tokenized_corpus = tokenize_corpus(raw)
      #print(tokenized_corpus)
      lstNGram = [count_ngrams(tokenized_corpus, i + 1) for i in range(1)]
      lstInfo = {SimplificarSTR(k[0]):0 for k in lstNGram[0].keys()}
      keys = list(lstInfo.keys()) + ["<s>","</s>"]
      dic_trans = {keys[i] : i for i in range(len(keys))}
      revdic_trans = {i : keys[i] for i in range(len(keys))}
      lstNGram = [count_ngrams(tokenized_corpus, i + 1, dic_trans) for i in range(N)]
      
      make_dir(mdir)
      lines = [f"{k}:{dic_trans[k]}\n" for k in dic_trans.keys()]
      f = open(mdir + "/dic.txt", "w")
      f.writelines(lines)
      f.close()
      
      for i in range(N):
            print(f"{i+1} esimo ngrama con {len(lstNGram[i])} tokens")
            lines = [f"{SimplificarSTR(str(k))}:{lstNGram[i][k]}\n" for k in lstNGram[i].keys()]
            f = open(mdir + f"/NG{i+1}.txt", "w")
            f.writelines(lines)
            f.close()

            
#CorpusProcesador(getSmallCorpus(), "data/corpus_1")      
#CorpusProcesador(getMedCorpus(), "data/corpus_2")
#CorpusProcesador(getBigCorpus(), "data/corpus_3") #CORPUS MUY PESADO