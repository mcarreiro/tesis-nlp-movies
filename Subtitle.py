# -*- coding: utf-8 -*-
import pysrt
import gzip
from repo import config as CONFIG
from pysrt import SubRipTime
from repo.tokenizer import Tokenizer


class Subtitle(object):
  """ Lee el archivo srt dado un número de pelicula y devuelve el texto y
    y los tiempos."""

  def __init__(self, movie_file_number):
    """ Inicia la clase, lee el archivo .srt y lo parsea """
    self.movie_file_number = str(movie_file_number)
    self.file_path = self.file_name(CONFIG.subtitles_path)

    # Lee el archivo srt
    with gzip.open(self.file_path) as f:
      file_content = f.read()
      try:
        self.raw_sub = pysrt.from_string(file_content.decode("utf-8"))
      except:
        self.raw_sub = pysrt.from_string(file_content.decode("latin-1"))


  def file_name(self, subtitles_path):
    """ Arma el nombre de archivo para abrir el srt """
    tmp_name = zip(self.movie_file_number, self.movie_file_number[::-1])
    file_path = [subtitles_path]
    file_name = []

    for i, (s1, s2) in enumerate(tmp_name):
      file_name.append(s1)
      if i < 4:
        file_path.insert(0, s2 + "/")

    return "".join(file_path[::-1]) + "".join(file_name) + ".gz"


  def context_of(self, word, time, length=10):
    t = SubRipTime.from_string(time) + 1
    sub = self.raw_sub.at(t)
    context = []
    if sub:
      sub = sub[0]
      delta = SubRipTime.from_ordinal(length * 1000) # (ordinal is milliseconds)
      start = sub.start - delta
      end = sub.end + delta
      subs = self.raw_sub.slice(ends_after=start, starts_before=end)
      tokenizer = Tokenizer()
      for line in subs:
        tokens = tokenizer.full_run(line.text)
        context = context + tokens
    return list(context)


  def word_count(self):
    return sum([len(x.split(' ')) for x in self.raw_sub.text.split('\n')])


  def full_text(self):
    return self.raw_sub.text


  def context_for_every_sub(self, length=5):
    """
    Returns an array containing dicts: {target_sub: ['a','b'], context: ['c','d']}
    This means every word in the target sub has as context all others in target and all in context.
    """
    tokenizer = Tokenizer()
    result = []
    delta = SubRipTime.from_ordinal(length * 1000) # (ordinal is milliseconds)
    for i, sub in enumerate(self.raw_sub):
      # `sub` is a SubRipItem
      context = []
      start = sub.start - delta
      end = sub.end + delta
      j = i-1
      while j >= 0:
        next_back = self.raw_sub[j]
        if next_back.end > start:
          context.append(next_back)
          j = j-1
        else:
          break
      j = i+1
      while j < len(self.raw_sub):
        next_fwd = self.raw_sub[j]
        if next_fwd.start < end:
          context.append(next_fwd)
          j = j+1
        else:
          break
      tokenized_context = []
      for line in context:
        tokens = tokenizer.full_run(line.text)
        tokenized_context = tokenized_context + tokens
      result.append([tokenizer.full_run(sub.text),tokenized_context])
    return result
