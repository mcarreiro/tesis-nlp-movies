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
    self.window_size = int(window_size)


  def build(self, year, save_each_movie=False):
    print("START BUILD OF YEAR ", year)
    word_to_index = {}
    next_index = 0
    year_subs = self.subs[self.subs.MovieYear == year][["IDSubtitleFile", "MovieYear","MovieName"]]
    temp_matrix = None
    for entry in year_subs.itertuples():
      try:
        row, col, count = [],[],[]
        subId = str(int(entry.IDSubtitleFile))
        print(subId)
        sub = Subtitle(int(subId))
        contexts = sub.context_for_every_sub(self.window_size)
        if len(contexts) == 0:
          # Bizarre movie with 10 subs which are mostly empty/description in between brackets
          continue
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
        # print("Making single matrix")
        if len(row) == 0 or len(col) == 0:
          continue
        single_film_matrix = coo_matrix((count, (row, col)))
        single_film_matrix = single_film_matrix.tocsr()
        if save_each_movie:
          print("Saving " + entry.MovieName)
          CooccurrenceMatrix.save_partial(single_film_matrix, entry.MovieName, entry.IDSubtitleFile, year)
        else:
          if temp_matrix is not None:
            print("Adding up to previous matrix")
            temp_matrix = CooccurrenceMatrix.sum_through_coo(temp_matrix,single_film_matrix)
          else:
            temp_matrix = single_film_matrix
      except FileNotFoundError:
        print("ERROR")
    if not save_each_movie:
      print("Saving full year matrix")
      matrix = temp_matrix.tocsr()
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
  def save_partial(matrix, movie_name, movie_id, year):
    folder_path = CONFIG.datasets_path + "partials/" + str(year) + "/"
    if not os.path.exists(folder_path):
      os.makedirs(folder_path)
    pickle_dump(matrix, folder_path + str(int(movie_id)) + "-" + str(movie_name) + ".p")

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
    print("Window size: ", window_size)
    gen = CooccurrenceMatrix(window_size)
    folder_path = CONFIG.datasets_path + "cooccurrence_matrices_" + str(window_size) + "/"
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
    gen.build_year_sums()


  def build_year_sums(self):
    result = {}
    for year in range(1930,2016):
      with open(CONFIG.datasets_path + "cooccurrence_matrices_" + str(self.window_size) + "/" + str(year) + ".p", 'rb') as f:
        matrix = pickle.load(f)
      result[year] = matrix.sum()
    with open(CONFIG.datasets_path + "cooccurrence_matrices_" + str(self.window_size) + "/words_per_year.p", 'wb') as file:
      pickle.dump(result, file, protocol=pickle.HIGHEST_PROTOCOL)



class MacOSFile(object):

  def __init__(self, f):
    self.f = f

  def __getattr__(self, item):
    return getattr(self.f, item)

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
