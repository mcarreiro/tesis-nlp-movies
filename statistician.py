import sys
sys.path.append('..')
import os
from repo.subtitle import Subtitle
import repo.config as CONFIG
import pandas as pd
import math
import pickle
from gensim.models.word2vec import Word2Vec
from sklearn.preprocessing import normalize
import numpy as np
import scipy.stats as ss


class Statistician(object):

  def __init__(self, window_size = 5):
    self.index = {}
    self.top_words = {}
    self.full_index = {}
    self.w2v_model = None
    self.window_size = window_size

    with open(CONFIG.datasets_path + "word_count.p", 'rb') as f:
      self.count_per_year = pickle.load(f)
    with open(CONFIG.datasets_path + "cooccurrence_matrices_" + str(self.window_size) + "/words_per_year.p", 'rb') as f:
      self.words_per_year = pickle.load(f)


  def word_frequency_for(self, words, chart_format=False, no_errors=False):
    """ Result is array of tuples from first year where #{word} was mentioned to last.
        Includes every year in between and the count is total mentions.
        [(1950, 78),(1951, 30),...]
    """
    if not self.index:
      with open(CONFIG.datasets_path + "frequency_index_2017.p", 'rb') as f:
        self.index = pickle.load(f)
    if isinstance(words, str):
      concept = [words]
    else:
      concept = words
    not_found = []
    found = []
    if no_errors:
      for word in concept:
        if word not in self.index:
          not_found.append(word)
        else:
          found.append(word)
      print("NOT FOUND: ", not_found)
    else:
      Statistician.error_if_not(words, self.index)
    # [{1983: 3, 1990: 62, ...},{},..]
    if no_errors:
      # this was just for testing purposes, the result if charted isn't ignoring the labels for not found keywords
      mentions_of_each = [self.index[word] for word in found]
    else:
      mentions_of_each = [self.index[word] for word in concept]
    totals = {}
    for mentions in mentions_of_each:
      for year, count in mentions.items():
        # Hack
        if int(year) == 2016:
          continue
        # Mentions / word total
        if year not in totals:
          totals[year] = count / self.count_per_year[int(year)]
        else:
          totals[year] += count / self.count_per_year[int(year)]
    if chart_format:
      totals = self.format_for_chart(totals)
    return totals


  def chart_frequency_for(self, words, smoothing=0, title="Título", save_to=None, no_errors=False, extra_colors=False):
    """ Charts frequency for list of words chosen. Each word separately.
        Smoothing (= n) parameter means result for 1 year (Y) equals (Y-N + .. + Y-1 + Y + Y+1 + .. + Y+N)/2N+1
    """
    import matplotlib.pyplot as plt
    frequencies = [self.word_frequency_for(word, chart_format=True, no_errors=no_errors) for word in words]
    if smoothing > 0:
      frequencies = [self.smoothed(arr,smoothing) for arr in frequencies]

    self.chart(frequencies, words, title=title, save_to=save_to, extra_colors=extra_colors)
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


  # Positive Pointwise Mutual Information
  def pmi_for(self, words1, words2, chart_format=False):
    result = {}
    for year in range(1930,2016):
      calc = self.yearly_pmi_for(words1, words2, year)
      result[year] = calc

    if chart_format:
      result_chart = {}
      for k,v in result.items():
        result_chart[k] = v["pmi"]
      result = self.format_for_chart(result_chart)
    return result


  # st.chart_pmi_for(["campaign","forces"],[["america","american","americans"],["iraq","iraqi","iraqis"],["muslim","muslims","islam"]],smoothing=3)
  def chart_pmi_for(self, target_words, comparison_words, smoothing=0, title="Título",save_to=None, highlights=[]):
    if not isinstance(target_words, list):
      target_words = [target_words]
    if not isinstance(comparison_words, list):
      comparison_words = [comparison_words]
    pmis = [self.pmi_for(target_words, ws, chart_format=True) for ws in comparison_words]
    if smoothing > 0:
      pmis = [self.smoothed(arr,smoothing) for arr in pmis]

    self.chart(pmis, comparison_words, title=title, save_to=save_to, vertical_markers=highlights)
    return None

  # Word to vec: distance of average of all context vectors to target vector
  # OR distance of all contexts of a single concept to all target vectors
  def w2v_average_for(self, target_words, context_words, chart_format=False, threshold=None):
    if (not isinstance(target_words,str) and len(target_words) > 1) and (len(context_words) > 1 and isinstance(context_words[0],list)):
      print("You can have multiple target words OR multiple context words. Not both")
      return
    if not self.w2v_model:
      w2v_model_path = CONFIG.datasets_path + "GoogleNews-vectors-negative300.bin"
      self.w2v_model = Word2Vec.load_word2vec_format(w2v_model_path, binary=True)
    if isinstance(target_words,list) and any([(target_word not in self.w2v_model) for target_word in target_words]):
      for target_word in target_words:
        if target_word not in self.w2v_model:
          print(target_word, "is not in the w2v model")
      return
    multiples = target_words if not isinstance(target_words,str) and len(target_words)>1 else context_words
    result = [{} for i in range(0,len(multiples))]

    for year in range(1930,2016):
      calc = self.yearly_w2v_for(target_words, context_words, year, threshold)
      for i in range(0,len(multiples)):
        result[i][year] = calc[i]
    if chart_format:
      result = [self.format_for_chart(word) for word in result]
    return result


  def chart_w2v_average_for(self, target_words, context_words, smoothing=0, title="Título", save_to=None, highlights=[]):
    w2v = self.w2v_average_for(target_words, context_words, chart_format=True)

    if smoothing > 0:
      w2v = [self.smoothed(arr,smoothing) for arr in w2v]

    multiples = target_words if not isinstance(target_words,str) and len(target_words)>1 else context_words
    self.chart(w2v, multiples, title=title, save_to=save_to, vertical_markers=highlights)
    return None


  # Word to vec: ratio of words in all contexts closer to target vector according to threshold.
  def w2v_threshold_for(self, target_word, context_words, threshold, chart_format=False):
    return self.w2v_average_for(target_word, context_words, chart_format=chart_format, threshold=threshold)


  def chart_w2v_threshold_for(self, target_words, context_words, threshold=0.193171, smoothing=0, title="Título", save_to=None, highlights=[]):
    w2v = self.w2v_threshold_for(target_words, context_words, chart_format=True, threshold=threshold)

    if smoothing > 0:
      w2v = [self.smoothed(arr,smoothing) for arr in w2v]

    multiples = target_words if not isinstance(target_words,str) and len(target_words)>1 else context_words
    self.chart(w2v, multiples, title=title, save_to=save_to, vertical_markers=highlights)
    return None


  def hypergeo_for(self, target_words, context_words, chart_format=False):
    result = {}
    for year in range(1930,2016):
      calc = self.yearly_hypergeo_for(target_words, context_words, year)
      result[year] = calc

    if chart_format:
      result = self.format_for_chart(result)
    return result


  def chart_hypergeo_for(self, target_words, comparison_words, smoothing=0, title="Titulo", save_to=None, highlights=[]):
    if not isinstance(target_words, list):
      target_words = [target_words]
    if not isinstance(comparison_words, list):
      comparison_words = [comparison_words]
    res = [self.hypergeo_for(target_words, ws, chart_format=True) for ws in comparison_words]

    if smoothing > 0:
      res = [self.smoothed(arr,smoothing) for arr in res]

    if not highlights:
      markers = [0.95]
    else:
      markers = highlights
    self.chart(res, comparison_words, title=title, save_to=save_to, horizontal_markers=markers)
    return None


  def find_high_pmi_movies(self, year, target_words, context_words):
    with open(CONFIG.datasets_path + "cooccurrence_matrices_" + str(self.window_size) + "/" + str(year) + "_reference.p", 'rb') as f:
      reference = pickle.load(f)
    general = self.yearly_pmi_for(target_words, context_words, year)
    print(general)
    indeces1, indeces2 = self.indeces(target_words, context_words, reference)
    all = []
    for movie in os.listdir(CONFIG.datasets_path + "partials/" + str(year) + "/"):
      with open(CONFIG.datasets_path + "partials/" + str(year) + "/" + movie, 'rb') as f:
        matrix = pickle.load(f)
      n = matrix.sum()
      joint_appearences = 0
      for row in indeces1:
        for col in indeces2:
          try:
            joint_appearences += matrix[row,col]
            if matrix[col,row] > 0:
              print("Found: " + movie)
          except:
            pass
      if joint_appearences == 0:
        pmi = 0
      else:
        calc = math.log((joint_appearences / n) / ((general['first'] / general['n']) * (general['second'] / general['n'])),2)
        if calc < 0:
          pmi = 0
        else:
          pmi = calc
      all.append([movie, pmi])
      all.sort(key=lambda a: -a[1])
    return [[movie, pmi] for movie,pmi in all if pmi > 0]


  def read_lines_with(self, target_words, context_words, year):
    movies = self.find_high_pmi_movies(year, target_words, context_words)
    for movie, pmi in movies:
      print(movie)
      id = movie[0:(movie.find('-'))]
      sub = Subtitle(id)
      subs = sub.subs_with(context_words,target_words)
      return [[sub.text for sub in movie] for movie in subs]



  # Auxiliaries

  def yearly_w2v_for(self, target_words, context_words, year, threshold=None):
    """ Returns an array of {1930: N, ..., 2015: M} for each pair of words. Each N is:
      - if multiple context_words it's distance of the resulting vector of all contexts
        of a context_word to the target vector (for that year)
      - if multiple target_words it's distance of a target word to all
        contexts of the single context_word (for that year)
    This should NOT be used with both multiple target words and multiple context words.
    Result will fail if you do.
    """
    if not self.w2v_model:
      w2v_model_path = CONFIG.datasets_path + "GoogleNews-vectors-negative300.bin"
      self.w2v_model = Word2Vec.load_word2vec_format(w2v_model_path, binary=True)
    # Matrices are in CSR format
    matrix, reference = self.load_matrix_for(year)
    target_words, context_words = self.listize(target_words, context_words)
    inv_reference = {v: k for k, v in reference.items()}
    target_vectors = normalize(np.array([self.w2v_model[target_word] for target_word in target_words]))

    if isinstance(context_words[0],str):
      context_word_indeces = [[Statistician.res_or_none(reference,word) for word in context_words]]
    else:
      context_word_indeces = [[Statistician.res_or_none(reference,word) for word in concept] for concept in context_words]
    rows = [[matrix.getrow(index) if index is not None else None for index in concept_indeces] for concept_indeces in context_word_indeces]
    rows = [[v for v in concept if v is not None] for concept in rows]
    rows = [l if len(l) > 0 else None for l in rows]
    vectors = []
    for row in rows:
      if row is None:
        vectors.append(None)
        continue
      row_vectors = []
      for word_row in row:
        for index in word_row.indices:
          word = inv_reference[index]
          if word in self.w2v_model:
            row_vectors.append(self.w2v_model[word])
      vectors.append(row_vectors)

    context_vectors = [normalize(row_vectors,axis=1) if row_vectors is not None else None for row_vectors in vectors]
    distances_per_target = {}
    distances = []
    for target_word,target_vector in zip(target_words, target_vectors):
      d = [np.matmul(vector,np.transpose(target_vector)) if vector is not None else None for vector in context_vectors]
      distances_per_target[target_word] = d
      distances.append(d)
    res = []
    for row in distances:
      for target in row:
        if target is None:
          res.append(None)
          continue
        if threshold:
            total = len(target)
            res.append(len([dist for dist in target if dist >= threshold]) / total)
        else:
          res.append(np.mean(target))
    return res


  def yearly_pmi_for(self, target_words, context_words, year):
    matrix, reference = self.load_matrix_for(year)
    indeces1, indeces2 = self.indeces(target_words, context_words, reference)

    n = matrix.sum()
    joint_appearences = 0
    for row in indeces1:
      for col in indeces2:
        joint_appearences += matrix[row,col]
    first_row = sum(map(lambda index: matrix.getrow(index).sum(), indeces1))
    second_row = sum(map(lambda index: matrix.getrow(index).sum(), indeces2))
    if not first_row or not second_row:
      pmi = None
    elif joint_appearences == 0:
      pmi = 0
    else:
      calc = math.log((joint_appearences / n) / ((first_row / n) * (second_row / n)),2)
      if calc < 0:
        pmi = 0
      else:
        pmi = calc
    return {"pmi": pmi, "joint": joint_appearences, "first": first_row, "second": second_row, "n": n}


  def yearly_hypergeo_for(self, target_words, context_words, year):
    matrix, reference = self.load_matrix_for(year)
    indeces1, indeces2 = self.indeces(target_words, context_words, reference)

    all_contexts = self.words_per_year[year]
    context_intersection = 0
    for row in indeces1:
      for col in indeces2:
        context_intersection += matrix[row,col]
    sum_for_target_words = sum(map(lambda index: matrix.getrow(index).sum(), indeces1))
    sum_for_context_words = sum(map(lambda index: matrix.getrow(index).sum(), indeces2))
    if not sum_for_target_words or not sum_for_context_words:
      res = None
    else:
      res = ss.hypergeom.cdf(context_intersection, all_contexts, sum_for_target_words, sum_for_context_words)
    return res


  def format_for_chart(self, hsh):
    """
    Receives a hash with years as keys.
    Returns an array of tuples [(1930, N),(1931, M)...] for all years between 1930 and 2015.
    Returns None for those without data in original hash.
    """
    sorted_tuples = [(k, hsh[k]) for k in sorted(hsh)]
    sorted_tuples = [(k, Statistician.res_or_none(hsh, k)) for k in range(1930, 2016)]
    return sorted_tuples

  def load_matrix_for(self, year):
    with open(CONFIG.datasets_path + "cooccurrence_matrices_" + str(self.window_size) + "/" + str(year) + ".p", 'rb') as f:
      matrix = pickle.load(f)
    with open(CONFIG.datasets_path + "cooccurrence_matrices_" + str(self.window_size) + "/" + str(year) + "_reference.p", 'rb') as f:
      reference = pickle.load(f)
    return [matrix, reference]

  def indeces(self, words1, words2, reference):
    words1, words2 = self.listize(words1,words2)

    indeces1 = map(lambda concept: Statistician.res_or_none(reference,concept), words1)
    indeces1 = [i for i in indeces1 if i is not None]
    indeces2 = map(lambda concept: Statistician.res_or_none(reference,concept), words2)
    indeces2 = [i for i in indeces2 if i is not None]
    return [indeces1, indeces2]


  def listize(self, words1, words2):
    if not isinstance(words1, list):
      words1 = [words1]
    if not isinstance(words2, list):
      words2 = [words2]
    return [words1, words2]


  def smoothed(self, tuples, level):
    """
    Receives an array in format_for_chart format.
    Returns the same format but it averages between the level years forward and back
    (if those years around have data)
    """
    result = []
    counter = 0
    for year,count in tuples:
      if count is not None:
        full_sum = count
        divisor = 1
        start = max(counter - level,0)
        for i in range(start,counter):
          if tuples[i][1] is not None:
            full_sum += tuples[i][1]
            divisor += 1
        finish = min(counter + level,len(tuples) - 1)
        for i in range(counter + 1,finish+1):
          if tuples[i][1] is not None:
            full_sum += tuples[i][1]
            divisor += 1
        res = full_sum / divisor
      else:
        res = None
      result.append((year, res))
      counter += 1
    return result


  def chart(self, data, labels, title="TÍTULO", save_to=None, horizontal_markers=[], vertical_markers=[], extra_colors=False):
    import matplotlib.pyplot as plt
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(14,7))
    ax = fig.add_subplot(111)

    if extra_colors:
      colormap = plt.cm.spectral
      total = len(data)
      i = 1
      for series,words in zip(data,labels):
        c = colormap(i/12.,1)
        i += 1
        ax.plot(range(len(series)), [v for k,v in series], label=words, color=c, marker='.')
    else:
      for series,words in zip(data,labels):
        ax.plot([k for k,v in series], [v for k,v in series], label=words, marker='.')

    for marker in horizontal_markers:
      ax.axhline(y=marker,color='black',ls='--')
    for marker in vertical_markers:
      ax.axvline(x=marker,color='black',ls='--')
    plt.locator_params(axis='x', nbins=85)
    plt.legend(loc='best')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.title(title)
    plt.ylim(ymin=0)
    if save_to is None:
      plt.show()
    else:
      plt.savefig(save_to, dpi=199)
    plt.close()


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
