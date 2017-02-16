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

    start_year = min([ tup[0][0] for tup in frequencies ])
    max_year = max([ tup[len(frequencies) - 1][0] for tup in frequencies ])
    year_range = range(start_year,max_year)

    for series,word in zip(frequencies,words):
      plt.plot(range(len(series)), [v for k,v in series], label=word)

    # plt.xticks(range(len(year_range)), year_range)
    plt.xticks(range(len(frequencies[0])), [k for k,v in frequencies[0]])
    plt.legend(loc='best')
    locs, labels = plt.xticks()
    plt.setp(labels, rotation=90)
    plt.title("Word frequency for " + ",".join(words))
    plt.ylim(ymin=0)
    plt.show()
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


  # Levantar el índice: ~45s ? ~5.4GB
  # Pointwise Mutual Information
  def pmi_for(self, word1, word2, range_in_seconds, custom_index=None):
    first_word_freq = self.word_frequency_for(word1)
    second_word_freq = self.word_frequency_for(word2)

    if custom_index:
      self.full_index = custom_index
    if not self.full_index:
      with open(CONFIG.datasets_path + "index_all_2017.p", 'rb') as f:
        self.full_index = pickle.load(f)
    joined_frequency = self.joined_counts_for(word1,word2,range_in_seconds)

    result = {}
    for year in range(1930,2015):
      if year in joined_frequency:
        result[year] = {'pmi': math.log((joined_frequency[year] / (self.index[word1][year] * self.index[word2][year]))*self.count_per_year[year], 2), 'first': Statistician.res_or_zero(self.index[word1], year), 'second': Statistician.res_or_zero(self.index[word2], year), 'n': self.count_per_year[year], 'joined': Statistician.res_or_zero(joined_frequency,year)
        , 'first_freq': Statistician.res_or_zero(first_word_freq,year), 'second_freq': Statistician.res_or_zero(second_word_freq,year), "fraccion": (joined_frequency[year] / (self.index[word1][year] * self.index[word2][year]))}
      else:
        result[year] = {'pmi': 0, 'first': Statistician.res_or_zero(self.index[word1],year), 'second': Statistician.res_or_zero(self.index[word2],year), 'n': self.count_per_year[year], 'joined': Statistician.res_or_zero(joined_frequency,year)}
    return result

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


  def joined_frequency_for(self, word1, word2, range_in_seconds):
    Statistician.error_if_not([word1, word2], self.full_index)
    if self.sub_files(word1) > self.sub_files(word2):
      word_mentions = self.full_index[word2]
      index_word = word2
      search_word = word1
    else:
      word_mentions = self.full_index[word1]
      index_word = word1
      search_word = word2
    counts = {}
    for year, mentions in word_mentions.items():
      for sub_id, times in mentions.items():
        sub = Subtitle(sub_id)
        for time in times:
          context = sub.context_of(index_word, time, range_in_seconds)
          if search_word in context:
            # Hash.new 0 (mirar para python)
            if not year in counts:
              counts[year] = 0
            counts[year] += context.count(search_word)
    result = {}
    for year, count in counts.items():
      if year in self.count_per_year:
        result[year] = count / self.count_per_year[year]
    return result


  def joined_counts_for(self, word1, word2, range_in_seconds):
    Statistician.error_if_not([word1, word2], self.full_index)
    if self.sub_files(word1) > self.sub_files(word2):
      word_mentions = self.full_index[word2]
      index_word = word2
      search_word = word1
    else:
      word_mentions = self.full_index[word1]
      index_word = word1
      search_word = word2
    counts = {}
    for year, mentions in word_mentions.items():
      for sub_id, times in mentions.items():
        sub = Subtitle(sub_id)
        for time in times:
          context = sub.context_of(index_word, time, range_in_seconds)
          if search_word in context:
            # Hash.new 0 (mirar para python)
            if not year in counts:
              counts[year] = 0
            counts[year] += context.count(search_word)
    return counts


  def squash_years_into(self, result, years=5):
    new = True
    squashed = {}
    for year,data in result.items():
      if new:
        year_count = 1
        first = 0
        second = 0
        joined = 0
        n = 0
        new = False
      first += data["first"]
      second += data["second"]
      joined += data["joined"]
      n += data["n"]
      year_count += 1
      if year_count == years:
        new = True
        squashed[year] = {"first": first, "second": second, "n": n, "joined": joined, "pmi": math.log((joined / (first * second))*n,2)}
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
  def error_if_not(words,index):
    for word in words:
      if word not in index:
        raise KeyError(word + " is not in index")
