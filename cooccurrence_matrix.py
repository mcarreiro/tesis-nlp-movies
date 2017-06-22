import sys
sys.path.append('..')
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse import csr_matrix
from repo.subtitle import Subtitle
import repo.config as CONFIG
import pandas as pd
import pickle
import os
import math


class CooccurrenceMatrix(object):

  def __init__(self, window_size):
    with open(CONFIG.datasets_path + "filtered_index_2017.p", 'rb') as f:
      self.subs = pickle.load(f, encoding='latin-1')
    self.window_size = window_size


  def build(self, year):
    print("START BUILD OF YEAR ", year)
    word_to_index = {}
    next_index = 0
    year_subs = self.subs[self.subs.MovieYear == year][["IDSubtitleFile", "MovieYear"]]
    temp_matrix = None
    for entry in year_subs.itertuples():
      row, col, count = [],[],[]
      subId = str(int(entry.IDSubtitleFile))
      print(subId)
      # try:
      sub = Subtitle(int(subId))
      print("Getting contexts")
      contexts = sub.context_for_every_sub(self.window_size)
      if len(contexts) == 0:
        # Bizarre movie with 10 subs which are mostly empty/description in between brackets
        continue
      print("Contexts done")
      # sub = [word1, word2], context = [word3, word4]
      print("ADDING TO ARRAYS")
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
      print("Making single matrix")
      single_film_matrix = coo_matrix((count, (row, col)))
      # Testing out if converting to csr minimizes memory usage
      single_film_matrix = single_film_matrix.tocsr()
      if temp_matrix is not None:
        print("Adding up to previous matrix")
        # temp_matrix = temp_matrix + single_film_matrix
        temp_matrix = CooccurrenceMatrix.sum_through_coo(temp_matrix,single_film_matrix)
      else:
        temp_matrix = single_film_matrix
      # print("DONE")
      # except:
      #   print("ERROR")

    print("Converting to final matrix")
    matrix = temp_matrix.tocsr()
    # print("TRANSFORMING TO CSR")
    # m = matrix.tocsr()
    print("SAVING TO FILE")
    CooccurrenceMatrix.save_to_file(matrix, word_to_index, year, self.window_size)
    [word_to_index, matrix]


  @staticmethod
  def sum_through_coo(matrix1, matrix2):
    m = matrix1.tocoo()
    n = matrix2.tocoo()
    d = np.concatenate((m.data, n.data))
    r = np.concatenate((m.row, n.row))
    c = np.concatenate((m.col, n.col))
    result = coo_matrix((d,(r,c)))
    result = result.tocsr()
    return result

  @staticmethod
  def save_to_file(matrix, word_to_index, year, window_size):
    folder_path = CONFIG.datasets_path + "cooccurrence_matrices_" + str(window_size) + "/"
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
    pickle_dump(matrix, folder_path + str(year) + ".p")
    with open(folder_path + str(year) + "_reference.p", 'wb') as file2:
      pickle.dump(word_to_index, file2, protocol=pickle.HIGHEST_PROTOCOL)

  @staticmethod
  def build_all(window_size = 5):
    gen = CooccurrenceMatrix(window_size)
    folder_path = CONFIG.datasets_path + "cooccurrence_matrices_" + window_size + "/"
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


class MacOSFile(object):

  def __init__(self, f):
    self.f = f

  def __getattr__(self, item):
    return getattr(self.f, item)

  # def read(self, n):
  #     # print("reading total_bytes=%s" % n, flush=True)
  #     if n >= (1 << 31):
  #         buffer = bytearray(n)
  #         idx = 0
  #         while idx < n:
  #             batch_size = min(n - idx, 1 << 31 - 1)
  #             # print("reading bytes [%s,%s)..." % (idx, idx + batch_size), end="", flush=True)
  #             buffer[idx:idx + batch_size] = self.f.read(batch_size)
  #             # print("done.", flush=True)
  #             idx += batch_size
  #         return buffer
  #     return self.f.read(n)

  def write(self, buffer):
    n = len(buffer)
    print("writing total_bytes=%s..." % n, flush=True)
    idx = 0
    while idx < n:
      batch_size = min(n - idx, 1 << 31 - 1)
      print("writing bytes [%s, %s)... " % (idx, idx + batch_size), end="", flush=True)
      self.f.write(buffer[idx:idx + batch_size])
      print("done.", flush=True)
      idx += batch_size

def pickle_dump(obj, file_path):
  with open(file_path, "wb") as f:
    return pickle.dump(obj, MacOSFile(f), protocol=pickle.HIGHEST_PROTOCOL)

# def pickle_load(file_path):
#     with open(file_path, "rb") as f:
#         return pickle.load(MacOSFile(f))
