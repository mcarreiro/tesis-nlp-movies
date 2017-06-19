import sys
sys.path.append('..')
from repo.subtitle import Subtitle
import repo.config as CONFIG
import pandas as pd
import math
import pickle
from gensim.models.word2vec import Word2Vec
from sklearn.preprocessing import normalize
import numpy as np


class Statistician(object):

  def __init__(self):
    self.index = {}
    self.top_words = {}
    self.full_index = {}
    self.w2v_model = None

    with open(CONFIG.datasets_path + "word_count.p", 'rb') as f:
      self.count_per_year = pickle.load(f)
    with open(CONFIG.datasets_path + "/cooccurrence_matrices/words_per_year.p", 'rb') as f:
      self.words_per_year = pickle.load(f)


  def word_frequency_for(self, word, chart_format=False):
    """ Result is array of tuples from first year where #{word} was mentioned to last.
        Includes every year in between and the count is total mentions.
        [(1950, 78),(1951, 30),...]
    """
    if not self.index:
      with open(CONFIG.datasets_path + "frequency_index_2017.p", 'rb') as f:
        self.index = pickle.load(f)
    Statistician.error_if_not([word], self.index)
    mentions = self.index[word] # {1983: 3, 1990: 62, ...}
    result = {}
    for year, count in mentions.items():
      # Hack
      if int(year) == 2016:
        continue
      # Mentions / word total
      if int(year) in self.count_per_year:
        result[year] = count / self.count_per_year[int(year)]

    if chart_format:
      result = self.format_for_chart(result)
    return result


  def chart_frequency_for(self, words, smoothing=0):
    """ Charts frequency for list of words chosen.
        Smoothing (= n) parameter means result for 1 year (Y) equals (Y-N + .. + Y-1 + Y + Y+1 + .. + Y+N)/2N+1
    """
    import matplotlib.pyplot as plt
    frequencies = [self.word_frequency_for(word, chart_format=True) for word in words]
    if smoothing > 0:
      frequencies = [self.smoothed(arr,smoothing) for arr in frequencies]
    print(frequencies)

    self.chart(frequencies, words)
    return None


  def top_words_for(self, year, tolerance=0.7):
    if not self.top_words:
      with open(CONFIG.datasets_path + "deprecated/top_words.p", 'rb') as f:
        self.top_words = pickle.load(f)
    prevalence = {}

    for y,l in self.top_words.items():
      for word in l:
        if word in prevalence:
          prevalence[word] += 1
        else:
          prevalence[word] = 1

    return [ word for word in self.top_words[str(year)] if prevalence[word] < tolerance * (2014-1930) ]


  # Pointwise Mutual Information
  def pmi_for(self, words1, words2, alpha=1, chart_format=False):
    result = {}
    for year in range(1930,2016):
      calc = self.yearly_pmi_for(words1, words2, year, alpha)
      result[year] = calc

    if chart_format:
      result_chart = {}
      for k,v in result.items():
        result_chart[k] = v["pmi"]
      result = self.format_for_chart(result_chart)
    return result


  # st.chart_pmi_for(["campaign","forces"],[["america","american","americans"],["iraq","iraqi","iraqis"],["muslim","muslims","islam"]],smoothing=3)
  def chart_pmi_for(self, target_words, comparison_words, smoothing=0, alpha=1):
    if not isinstance(target_words, list):
      target_words = [target_words]
    if not isinstance(comparison_words, list):
      comparison_words = [comparison_words]
    pmis = [self.pmi_for(target_words, ws, chart_format=True) for ws in comparison_words]

    if smoothing > 0:
      pmis = [self.smoothed(arr,smoothing) for arr in pmis]

    self.chart(pmis, comparison_words)
    return None


  def w2v_average_for(self, target_word, context_words, chart_format=False, threshold=None):
    if not self.w2v_model:
      w2v_model_path = CONFIG.datasets_path + "GoogleNews-vectors-negative300.bin"
      self.w2v_model = Word2Vec.load_word2vec_format(w2v_model_path, binary=True)
    result = [{} for w in context_words]

    for year in range(1930,2016):
      calc = self.yearly_w2v_for(target_word, context_words, year, threshold)
      for i in range(0,len(context_words)):
        result[i][year] = calc[i]
    # print("W2V_AVG: ", result)
    if chart_format:
      result = [self.format_for_chart(word) for word in result]
    return result


  def chart_w2v_average_for(self, target_word, context_words, smoothing=0):
    w2v = self.w2v_average_for(target_word, context_words, chart_format=True)

    if smoothing > 0:
      w2v = [self.smoothed(arr,smoothing) for arr in w2v]

    self.chart(w2v, context_words)
    return None


  def w2v_threshold_for(self, target_word, context_words, threshold, chart_format=False):
    return self.w2v_average_for(target_word, context_words, chart_format=chart_format, threshold=threshold)


  def chart_w2v_threshold_for(self, target_word, context_words, threshold=0.193171, smoothing=0):
    w2v = self.w2v_threshold_for(target_word, context_words, chart_format=True, threshold=threshold)

    if smoothing > 0:
      w2v = [self.smoothed(arr,smoothing) for arr in w2v]

    self.chart(w2v, context_words)
    return None


  # Auxiliaries

  def yearly_w2v_for(self, target_words, context_words, year, threshold=None):
    if not self.w2v_model:
      w2v_model_path = CONFIG.datasets_path + "GoogleNews-vectors-negative300.bin"
      self.w2v_model = Word2Vec.load_word2vec_format(w2v_model_path, binary=True)
    # Matrices are in CSR format
    with open(CONFIG.datasets_path + "cooccurrence_matrices/" + str(year) + ".p", 'rb') as f:
      matrix = pickle.load(f)
    with open(CONFIG.datasets_path + "cooccurrence_matrices/" + str(year) + "_reference.p", 'rb') as f:
      reference = pickle.load(f)
    inv_reference = {v: k for k, v in reference.items()}
    target_vector = normalize(np.array([self.w2v_model[target_word]]),axis=1)[0]

    context_word_indeces = [Statistician.res_or_none(reference,word) for word in context_words]
    rows = [matrix.getrow(index) if index is not None else None for index in context_word_indeces]
    vectors = []
    for row in rows:
      if row is None:
        vectors.append(None)
        continue
      row_vectors = []
      for index in row.indices:
        word = inv_reference[index]
        if word in self.w2v_model:
          row_vectors.append(self.w2v_model[word])
      vectors.append(row_vectors)
    vectors = [normalize(row_vectors,axis=1) if row_vectors is not None else None for row_vectors in vectors]
    distances = [np.matmul(vector,np.transpose(target_vector)) if vector is not None else None for vector in vectors]
    res = []
    for row in distances:
      if row is None:
        res.append(None)
        continue
      if threshold:
          total = len(row)
          res.append(len([dist for dist in row if dist >= threshold]) / total)
      else:
        res.append(np.mean(row))
    return res


  def yearly_pmi_for(self, target_words, context_words, year, alpha=1):
    with open(CONFIG.datasets_path + "cooccurrence_matrices/" + str(year) + ".p", 'rb') as f:
      matrix = pickle.load(f)
    with open(CONFIG.datasets_path + "cooccurrence_matrices/" + str(year) + "_reference.p", 'rb') as f:
      reference = pickle.load(f)

    if not isinstance(target_words, list):
      target_words = [target_words]
    if not isinstance(context_words, list):
      context_words = [context_words]

    indeces1 = map(lambda concept: Statistician.res_or_none(reference,concept), target_words)
    indeces1 = [i for i in indeces1 if i is not None]
    indeces2 = map(lambda concept: Statistician.res_or_none(reference,concept), context_words)
    indeces2 = [i for i in indeces2 if i is not None]

    n = self.words_per_year[year]
    joint_appearences = 0
    for row in indeces1:
      for col in indeces2:
        joint_appearences += matrix[row,col]

    first_row = sum(map(lambda index: matrix.getrow(index).sum(), indeces1))
    second_row = sum(map(lambda index: matrix.getrow(index).sum(), indeces2))
    if joint_appearences == 0:
      pmi = 0
    else:
      calc = math.log((joint_appearences / n) / ((first_row / n) * (second_row**alpha / n**alpha)),2)
      if calc < 0:
        pmi = 0
      else:
        pmi = calc
    return {"pmi": pmi, "joint": joint_appearences, "first": first_row, "second": second_row, "n": n}


  def format_for_chart(self, hsh):
    sorted_tuples = [(k, hsh[k]) for k in sorted(hsh)]
    sorted_tuples = [(k, Statistician.res_or_none(hsh, k)) for k in range(1930, 2016)]
    return sorted_tuples

  def smoothed(self, tuples, level):
    result = []
    counter = 0
    for year,count in tuples:
      full_sum = count
      divisor = 1
      start = max(counter - level,0)
      for i in range(start,counter - 1):
        if tuples[i][1] is not None:
          full_sum += tuples[i][1]
          divisor += 1
      finish = min(counter + level,len(tuples) - 1)
      for i in range(counter + 1,finish):
        if tuples[i][1] is not None:
          full_sum += tuples[i][1]
          divisor += 1

      result.append((year, full_sum / divisor))
      counter += 1
    return result


  def chart(self, data, labels):
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')

    colormap = plt.cm.spectral
    total = len(data)
    i = 1
    for series,words in zip(data,labels):
      c = colormap(i/10.,1)
      i += 1
      plt.plot(range(len(series)), [v for k,v in series], label=words, color=c)

    plt.xticks(range(len(data[0])), [k for k,v in data[0]])
    plt.legend(loc='best')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    # plt.title("PMI for " + ",".join(labels))
    plt.ylim(ymin=0)
    plt.show()


  def squash_years_into(self, result, years=5):
    new = True
    squashed = {}
    for year,data in result.items():
      if new:
        year_count = 1
        first = 0
        second = 0
        joint = 0
        n = 0
        new = False
        year_mark = year
      first += data["first"]
      second += data["second"]
      joint += data["joint"]
      n += data["n"]
      year_count += 1
      if year_count == years:
        new = True
        if joint == 0 or first == 0 or second == 0:
          pmi = 0
        else:
          pmi = math.log((joint / (first * second))*n,2)
        squashed[year_mark] = {"first": first, "second": second, "n": n, "joint": joint, "pmi": pmi}
    return squashed


  def sub_files(self, word):
    count = 0
    for year,movies in self.full_index[word].items():
      count += len(movies)
    return count


  @staticmethod
  def one_year(index,year):
    res = {}
    for word,years in index.items():
        if year in years.keys():
            res[word] = {}
            res[word][year] = years[year]
    return res

  @staticmethod
  def res_or_zero(res, k):
    if k in res:
      return res[k]
    else:
      return 0

  @staticmethod
  def res_or_none(res, k):
    if k in res:
      return res[k]
    else:
      return None

  @staticmethod
  def error_if_not(words,index):
    for word in words:
      if word not in index:
        raise KeyError(word + " is not in index")
