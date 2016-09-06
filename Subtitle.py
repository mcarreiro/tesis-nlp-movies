# -*- coding: utf-8 -*-
import pysrt
import gzip
from datetime import datetime, date, timedelta
import config as CONFIG


# che, tire esto aca, no se como ponerlo de manera prolija. despues lo reubicamos donde les parezca
def time_to_seconds(time):
    return time.minute*60+time.second

class Dialog(list):
  """ Estructura que representa un diálogo, que a su vez está compuesto
    por frames, just in case... """
  def set_start(self, start_time):
    self.start = start_time

  def set_end(self, end_time):
    self.end_time = end_time

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
        self.pysrt = pysrt.from_string(file_content.decode("utf-8"))
      except:
        self.pysrt = pysrt.from_string(file_content.decode("latin-1"))

    self.dialogs_list = []

  def set_dialog_length_to(self, dialog_length):
    self.dialog_list = self.dialogs(self.pysrt, dialog_length)

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

  def word_count(self):
    return sum([len(x.split(' ')) for x in self.pysrt.text.split('\n')])

  def full_text(self):
    return self.pysrt.text





  def dialogs(self, srt_list, new_dialog_secs):
    """ Se le le pasa una lista de frames de srt y lo convierte en una
      lista de de lista de diccionarios. La listas internas van a
      representar 'diálogos' """

    # Para después buscar rápido la ubicación del frame en diálogos
    self.location_frame = {}

    # Identifico los diálogos
    n_diag = -1
    dialogs_list = []
    new_dialog = True
    for i, (s, s_sig) in enumerate(zip(srt_list, srt_list[1:] + ["end"])):
      if new_dialog == True: # Si es un nuevo diálogo, lo inicializo
        dialog = Dialog()
        dialog.set_start(s.start)
        n_diag += 1
        n_inside_diag = 0

      dialog.append(s)
      self.location_frame[i] = (n_diag, n_inside_diag)
      n_inside_diag += 1

      if s_sig !="end": # Si no le sigue el final
        # Me fijo si comienza un nuevo diálogo
        time_between = (s_sig.start - s.end)
        new_dialog = time_between > pysrt.SubRipTime(seconds=new_dialog_secs)
        if new_dialog: # Si comienzo un nuevo diálgo, termino el actual y lo adjunto
          dialog.set_end(s.end) # Fijo el final del diálogo
          dialogs_list.append(dialog)
      else: # Si llego al final de la película termina el diálogo
        dialogs_list.append(dialog)

    return dialogs_list

  def window(self, frame_number, window_time_min = 1, window_time_sec = 0):
    """ Devuelve los subtitulos en una ventana de tiempo desde el tiempo de comienzo y fin
      del frame que se pide. """

    # Veo en qué dialog y posición está y lo devuelvo
    n_diag, i = self.location_frame[frame_number]
    frame = self.dialogs_list[n_diag][i]
    sub_slice_from = frame.start
    sub_slice_to = frame.end

    # Usa la representación de tiempo interna de pysrt
    slice_from = sub_slice_from - pysrt.SubRipTime(minutes = window_time_min, seconds = window_time_sec)
    slice_to = sub_slice_to + pysrt.SubRipTime(minutes = window_time_min, seconds = window_time_sec)

    sub_slice = [e for e in self.dialogs_list[n_diag] if (e.start > slice_from) and (e.end < slice_to)]

    return sub_slice

  def to_text(self, subs_slice):
    """ Pasa un slice de subtitulos a texto """

    texto = []
    for s in subs_slice:
      s = s.text.replace(u"\n", u" ")
      texto.append(s)

    # Limpio los tags
    texto = " ".join(texto)
    tags = ["<b>", "</b>", "{b}", "{/b}", "<i>", "</i>",
        "{i}", "{/i}", "<u>", "</u>", "{u}", "{/u}"]

    for t in tags:
      texto = texto.replace(t, "")

    return texto

  def sub_len(self):
    return len(self.pysrt)

  def delta_frames(self):
    """ Devuelve una lista con el tiempo que hay entre cada frame, en segundos"""

    return [time_to_seconds((self.pysrt[i+1].start-self.pysrt[i].end).to_time()) for i in range(len(self.pysrt)-1)]

  """def slice_sub_by_delta_time(self):
    # Devuelve una lista con el tiempo que hay entre cada frame, en segundos

    return [self.pysrt[i+1].start for i in range(len(self.pysrt)-1) if time_to_seconds((self.pysrt[i+1].start-self.pysrt[i].end).to_time())>10] """
