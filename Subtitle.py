# -*- coding: utf-8 -*-
import sys
sys.path.append('..')
import pysrt
import config as CONFIG
from pysrt import SubRipTime
from Tokenizer import Tokenizer


tokenizer = Tokenizer()


def flatten(l):
    return [item for sublist in l for item in sublist]


class Subtitle(object):
    """ Lee el archivo srt dado un número de pelicula y devuelve el texto y
      y los tiempos."""

    def __init__(self, movie_sub_number):
        """ Inicia la clase, lee el archivo .srt y lo parsea """
        self.movie_sub_number = str(movie_sub_number)
        self.filename = CONFIG.subtitles_path + self.movie_sub_number + ".srt"
        self.all_frames = None

        # Lee el archivo srt
        with open(self.filename, "rb") as f:
            file_content = f.read()
            try:
                self.raw_sub = pysrt.from_string(file_content.decode("utf-8"))
            except Exception:
                self.raw_sub = pysrt.from_string(file_content.decode("latin-1"))

    def full_tokens(self):
        full_tokens = []
        self.all_frames = []
        for f in self.raw_sub:
            tokens = tokenizer.full_run(f.text_without_tags)
            full_tokens.extend(tokens)
            self.all_frames.append({"start": f.start,
                                    "end": f.end,
                                    "tokens": tokens})
        return full_tokens

    def generate_word_contexts(self, length):
        self.word_contexts = {}
        self.len_windows = []
        delta = SubRipTime.from_ordinal(int(length) * 1000)  # (ordinal is milliseconds)
        if not self.all_frames:
            self.full_tokens()

        for i, f in enumerate(self.all_frames):
            # Get data from frame
            f_start = f["start"]
            f_end = f["end"]
            f_tokens = f["tokens"]
            start_of_window = f_start - delta
            end_of_window = f_end + delta

            if not f_tokens:  # The frame has no tokens
                continue

            f_context = f["tokens"].copy()  # Initialization of the context

            # Add tokens of preceding frames
            j = -1
            while (i + j) >= 0 and self.all_frames[i + j]["end"] >= start_of_window:
                f_context.extend(self.all_frames[i + j]["tokens"])
                j -= 1

            # Add tokens of later frames
            j = 1
            while (i + j) <= (len(self.all_frames) - 1) and self.all_frames[i + j]["start"] <= end_of_window:
                f_context.extend(self.all_frames[i + j]["tokens"])
                j += 1

            # Add to context dictionary
            for t in f["tokens"]:
                self.len_windows.append(len(f_context) - 1)  # This is for the length of windows analysis
                if t not in self.word_contexts:
                    self.word_contexts[t] = {}
                for c in f_context:
                    self.word_contexts[t][c] = self.word_contexts[t].get(c, 0) + 1
                self.word_contexts[t][t] -= 1
                if self.word_contexts[t][t] == 0:
                    del self.word_contexts[t][t]

        if not self.check_correct_start_end():  # If end and star are not correct, the matrices are not symmmetric
            self.correct_symmetry()

        return(self.word_contexts)

    def correct_symmetry(self):
        for i, t1 in enumerate(self.word_contexts.copy()):
            for t2 in self.word_contexts[t1]:
                v = max(self.word_contexts[t1].get(t2, 0), self.word_contexts[t2].get(t1, 0))
                self.word_contexts[t1][t2] = v
                self.word_contexts[t2][t1] = v

    def check_correct_start_end(self):
        for i in range(1, len(self.all_frames)):
            if (self.all_frames[i - 1]["end"] > self.all_frames[i]["start"]):
                return False
        return True

    def bad_beginnings(self):
        return [e for e in self.all_frames if (e["start"] > e["end"])]
