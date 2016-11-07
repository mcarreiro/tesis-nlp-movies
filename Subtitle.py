# -*- coding: utf-8 -*-
import pysrt
import gzip
import config as CONFIG
from pysrt import SubRipTime
from tokenizer import Tokenizer


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
    t = SubRipTime.from_string(time)
    delta = SubRipTime.from_ordinal(length * 1000) # (ordinal is milliseconds)
    start = t - delta
    end = t + delta
    subs = self.raw_sub.slice(starts_after=start, starts_before=end)
    tokenizer = Tokenizer()
    context = []
    for line in subs:
      tokens = tokenizer.full_run(line.text)
      context = context + tokens
    return list(set(context))


  def word_count(self):
    return sum([len(x.split(' ')) for x in self.raw_sub.text.split('\n')])


  def full_text(self):
    return self.raw_sub.text
