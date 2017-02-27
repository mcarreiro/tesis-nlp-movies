from subtitle import Subtitle
import pandas as pd
import config as CONFIG
import math
import pickle

class Statistician(object):

  def __init__(self):
    self.index = {}
    self.top_words = {}
    self.full_index = {}

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
      # Mentions / word total
      if int(year) in self.count_per_year:
        result[year] = count / self.count_per_year[int(year)]

    if chart_format:
      sorted_tuples = [(k, result[k]) for k in sorted(result)]
      sorted_tuples = [(k, Statistician.res_or_zero(result, k)) for k in range(int(sorted_tuples[0][0]), int(sorted_tuples[len(sorted_tuples)-1][0]))]
      result = sorted_tuples
    return result


  def chart_frequency_for(self, words, smoothing=0):
    """ Charts frequency for list of words chosen.
        Smoothing (= n) parameter means result for 1 year (Y) equals (Y-N + .. + Y-1 + Y + Y+1 + .. + Y+N)/2N+1
    """
    import matplotlib.pyplot as plt
    frequencies = [self.word_frequency_for(word, chart_format=True) for word in words]
    if smoothing > 0:
      frequencies = [self.smoothed(arr,smoothing) for arr in frequencies]

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
  def pmi_for(self, word1, word2, chart_format=False, squashed=False):
    result = {}
    for year in range(1930,2016):
      calc = self.yearly_pmi_for(word1, word2, year)
      result[year] = calc

    if chart_format:
      if squashed:
        result = self.squash_years_into(result)
      result_chart = {}
      for k,v in result.items():
        result_chart[k] = v["pmi"]
      sorted_tuples = [(k, result_chart[k]) for k in sorted(result_chart)]
      sorted_tuples = [(k, Statistician.res_or_zero(result_chart, k)) for k in range(int(sorted_tuples[0][0]), int(sorted_tuples[len(sorted_tuples)-1][0]))]
      result = sorted_tuples
    return result

  def chart_pmi_for(self, words1, words2, smoothing=0, squashed=False):
    if not isinstance(words1, list):
      words1 = [words1]
    if not isinstance(words2, list):
      words2 = [words2]
    pairs = zip(words1,words2)
    pmis = [self.pmi_for(w1, w2, chart_format=True, squashed=squashed) for w1,w2 in pairs]

    if smoothing > 0:
      pmis = [self.smoothed(arr,smoothing) for arr in pmis]

    self.chart(pmis, words2)
    return None

  def yearly_pmi_for(self, concept1, concept2, year):
    with open(CONFIG.datasets_path + "cooccurrence_matrices/" + str(year) + ".p", 'rb') as f:
      matrix = pickle.load(f)
    with open(CONFIG.datasets_path + "cooccurrence_matrices/" + str(year) + "_reference.p", 'rb') as f:
      reference = pickle.load(f)

    if not isinstance(concept1, list):
      concept1 = [concept1]
    if not isinstance(concept2, list):
      concept2 = [concept2]

    indeces1 = map(lambda concept: Statistician.res_or_none(reference,concept), concept1)
    indeces1 = [i for i in indeces1 if i is not None]
    indeces2 = map(lambda concept: Statistician.res_or_none(reference,concept), concept2)
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
      pmi = math.log((joint_appearences / (first_row * second_row)) * n,2)
    return {"pmi": pmi, "joint": joint_appearences, "first": first_row, "second": second_row, "n": n}


  # Auxiliaries

  def smoothed(self, tuples, level):
    result = []
    counter = 0
    for year,count in tuples:
      full_sum = count
      divisor = 1
      start = max(counter - level,0)
      for i in range(start,counter - 1):
        full_sum += tuples[i][1]
        divisor += 1
      finish = min(counter + level,len(tuples) - 1)
      for i in range(counter + 1,finish):
        full_sum += tuples[i][1]
        divisor += 1

      result.append((year, full_sum / divisor))
      counter += 1
    return result


  def chart(self, data, labels):
    import matplotlib.pyplot as plt
    start_year = min([ tup[0][0] for tup in data ])
    max_year = max([ tup[len(data) - 1][0] for tup in data ])
    year_range = range(start_year,max_year)

    for series,words in zip(data,labels):
      plt.plot(range(len(series)), [v for k,v in series], label=words)

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
