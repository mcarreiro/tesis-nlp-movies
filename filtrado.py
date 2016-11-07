#coding=utf-8

from subtitle import Subtitle
import pandas as pd
import numpy as np
import random

def best_subs(subs_df, seed = 1234):
	""" Función que elige los subtitulos por pelicula de usuario
	    de mayor ranking """

	random.seed(seed)

	elegidos = set()
	UserRank = ["super admin", "administrator", "subtranslator",
				 "platinum member", "vip plus member", "vip member",
				 "gold member", "trusted", "silver member",
				 "bronze member", "sub leecher", None] # Fuente: http://forum.opensubtitles.org/viewtopic.php?t=1991

	# Veo las peliculas y para cada una elijo al azar un subtitulos
	# de los usuarios con mayor ranking
	for m in subs_df.MovieID.unique():
		subs_df_tmp_1 = subs_df[subs_df.MovieID == m]
		assert subs_df_tmp_1.shape[0] > 0
		for st in UserRank:
			# Selecciono los subtitulos del ranking que busco
			if st == None:
				subs_df_tmp_2 = subs_df_tmp_1[subs_df_tmp_1.UserRank.isnull()]
			else:
				subs_df_tmp_2 = subs_df_tmp_1[subs_df_tmp_1.UserRank==st]
			# Si hay del ranking, elijo uno al azar
			if subs_df_tmp_2.shape[0] > 0:
				elegidos.add(int(random.choice(list(subs_df_tmp_2.IDSubtitleFile))))
				break

	# Armo los índices
	ix = [True if int(e) in elegidos else False for e in subs_df.IDSubtitleFile.tolist()]
	return subs_df[ix]
