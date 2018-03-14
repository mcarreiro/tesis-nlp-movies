Steps to collect and generate the data:

1 - Download top movies by year from IMDB.

	python3 download_top_movies.py

2 - Download IMDB metadata from top movies and create datasets.

	python3 download_metadata_from_top.py

3 - Filter movies from collected metadata

	python3 original_list_filter.py

4 - Download de location of the best srt

	python3 download_best_srt.py

5 - Check which subtitles we have in the dump on move them to a folder

	python3 look_in_dump.py

6 - Download missing subtitles

	python3 download_subs_not_in_dump.py

Steps to create matrices

1 - Build a vocabulary index and contexts by movie

	python3 build_frequency_index.py

2 - Build co-occurrence matrices (and creates output tables)

	python3 cooccurrence_matrix.py
