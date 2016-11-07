from subtitle import Subtitle
import pandas as pd
import config as CONFIG
import pickle
import matplotlib.pyplot as plt

class Analyzer(object):

  def __init__(self):
    self.index = {}
    self.top_words = {}
    self.full_index = {}

    with open(CONFIG.datasets_path + "word_count.p", 'rb') as f:
      self.count_per_year = pickle.load(f)


  def word_frequency_for(self, word):
    """ Result is array of tuples from first year where #{word} was mentioned to last.
        Includes every year in between and the count is total mentions.
        [(1950, 78),(1951, 30),...]
    """
    if not self.index:
      with open(CONFIG.datasets_path + "frequency_index.p", 'rb') as f:
        self.index = pickle.load(f)
    if word not in self.index:
      print("This word is not in the index")
      return [];
    else:
      mentions = self.index[word] # {1983: 3, 1990: 62, ...}
      result = {}
      for key, value in mentions.items():
        # Mentions / word total
        if int(key) in self.count_per_year:
          result[key] = value / self.count_per_year[int(key)]

      sorted_tuples = [(k, result[k]) for k in sorted(result)]
      sorted_tuples = [(k, Analyzer.res_or_zero(result, str(k))) for k in range(int(sorted_tuples[0][0]), int(sorted_tuples[len(sorted_tuples)-1][0]))]
      return sorted_tuples


  def chart_frequency_for(self, words, smoothing=0):
    """ Charts frequency for list of words chosen.
        Smoothing (= n) parameter means result for 1 year (Y) equals (Y-N + .. + Y-1 + Y + Y+1 + .. + Y+N)/2N+1
    """
    frequencies = [self.word_frequency_for(word) for word in words]
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
    plt.show()
    return None


  def top_words_for(self, year, tolerance=0.7):
    if not self.top_words:
      with open(CONFIG.datasets_path + "top_words.p", 'rb') as f:
        self.top_words = pickle.load(f)
    prevalence = {}

    for y,l in self.top_words.items():
      for word in l:
        if word in prevalence:
          prevalence[word] += 1
        else:
          prevalence[word] = 1

    return [ word for word in self.top_words[str(year)] if prevalence[word] < tolerance * (2014-1930) ]


  # Levantar el índice: ~45s ~4.3GB
  # Pointwise Mutual Information
  def pmi_for(self, word1, word2, range_in_seconds):
    if not self.full_index:
      with open(CONFIG.datasets_path + "full_per_year/index_all.p", 'rb') as f:
        self.full_index = pickle.load(f)
    first_word_freq = word_frequency_for(word1)
    second_word_freq = word_frequency_for(word2)
    joined_frequency = Analyzer.joined_frequency_for(word1,word2,range_in_seconds)
    # math.log(joined_frequency, 2) - math.log(first_word_freq * second_word_freq) PER YEAR
    return 0

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
    word1_mentions = self.full_index[word1]
    counts = {}
    for year, mentions in word1_mentions.items():
      for sub_id, times in mentions.items():
        sub = Subtitle(sub_id)
        for time in times:
          context = sub.context_of(word1, time, range_in_seconds)
          if word2 in context:
            if year in counts:
              counts[year] = 0
            counts[year] += 1


  @staticmethod
  def res_or_zero(res, k):
    if k in res:
      return res[k]
    else:
      return 0
