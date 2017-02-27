import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from subtitle import Subtitle
import pandas as pd
import config as CONFIG
import pickle
import os
import math

class CooccurrenceMatrix(object):

  def __init__(self):
    with open(CONFIG.datasets_path + "filtered_index_2017.p", 'rb') as f:
      self.subs = pickle.load(f, encoding='latin-1')


  def build(self, year):
    word_to_index = {}
    next_index = 0
    row, col, count = [],[],[]
    year_subs = self.subs[self.subs.MovieYear == year][["IDSubtitleFile", "MovieYear"]]
    for entry in year_subs.itertuples():
      subId = str(int(entry.IDSubtitleFile))
      print(subId)
      try:
        sub = Subtitle(int(subId))
        contexts = sub.context_for_every_sub()
        # sub = [word1, word2], context = [word3, word4]
        for sub,context in contexts:
          for word in sub:
            # Get an index for this word in the matrix
            if word in word_to_index:
              i = word_to_index[word]
            else:
              i = next_index
              word_to_index[word] = i
              next_index += 1

            # Add each context for this word.
            # There will be duplicates, but the matrix will handle them:
            # https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.coo_matrix.html
            for c in sub + context:
              if c == word:
                continue
              # Get an index for the c word
              if c in word_to_index:
                c_i = word_to_index[c]
              else:
                c_i = next_index
                word_to_index[c] = c_i
                next_index += 1
              row.append(i)
              col.append(c_i)
              count.append(1)
      except:
        print("ERROR")

    matrix = coo_matrix((count, (row, col)))
    m = matrix.tocsr()
    CooccurrenceMatrix.save_to_file(m, word_to_index, year)
    [word_to_index, matrix]


  @staticmethod
  def save_to_file(matrix, word_to_index, year):
    folder_path = CONFIG.datasets_path + "cooccurrence_matrices/"
    with open(folder_path + str(year) + ".p", 'wb') as file:
      pickle.dump(matrix, file, protocol=pickle.HIGHEST_PROTOCOL)
    with open(folder_path + str(year) + "_reference.p", 'wb') as file2:
      pickle.dump(word_to_index, file2, protocol=pickle.HIGHEST_PROTOCOL)

  @staticmethod
  def build_all():
    gen = CooccurrenceMatrix()
    folder_path = CONFIG.datasets_path + "cooccurrence_matrices/"
    if os.path.exists(folder_path):
      files = os.listdir(folder_path)
      start = 1930 + math.floor(len(files) / 2)
    else:
      os.makedirs(folder_path)
      start = 1930

    print("STARTS IN: ", start)
    for year in range(start,2016):
      print("HERE STARTS YEAR: ", year)
      gen.build(year)
