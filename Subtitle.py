# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import pysrt
import gzip
import repo.config as CONFIG
from pysrt import SubRipTime
from repo.tokenizer import Tokenizer

flatten = lambda l: [item for sublist in l for item in sublist]

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

    active = None
    window = []
    for i, sub in enumerate(self.raw_sub):
      # Invariant: window contains current sub + subs within reach going backwards
      # I need to find if any subs forwards fit the window
      # And delete those which fall out when advancing current
      # `sub` is a SubRipItem
      if len(window) == 0:
        active_subs_tokens = tokenizer.full_run(sub.text)
        if len(active_subs_tokens) > 0:
          # Add current to window
          window.append({'sub': sub, 'tokens': active_subs_tokens, 'i': i})
          active = 0
        else:
          # Subs with symbols, like music, or CAPS DESCRIPTIONS OF ACTION
          continue
      else:
        if sub.text != window[active]["sub"].text:
          # This sub has been ommitted from the window because it tokenizes to []
          # So now the window and the iteration are not matching up, so we skip.
          continue
      # Find if any after last in window now fall in range
      end_of_window = sub.end + delta
      j = window[len(window)-1]["i"] + 1 # if len(window) > 1 else i+1
      while j < len(self.raw_sub):
        next_fwd = self.raw_sub[j]
        if next_fwd.start < end_of_window:
          tokens = tokenizer.full_run(next_fwd.text)
          if len(tokens) > 0:
            window.append({'sub': next_fwd, 'tokens': tokens, 'i': j})
          j = j+1
        else:
          break
      # Append tokens in window to result
      context = flatten([item['tokens'] for k,item in enumerate(window) if k != active])
      result.append([window[active]['tokens'],context])

      # Move active forward and remove previous subs falling out of range
      if len(window)-1 > active:
        current_sub = window[active]["sub"]
        active = active+1
        new_start = window[active]["sub"].start - delta
        while window[0]["sub"] != current_sub:
          if window[0]["sub"].end > new_start:
            break
          else:
            window = window[1:]
            active = active-1
      else:
        window = []
        active = None
    return result


  def context_for_every_sub_OLD(self, length=5):
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
