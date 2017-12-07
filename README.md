## Análisis cuantitativo de sesgos culturales en películas de Hollywood

Repositorio de código que genera las estructuras auxiliares utilizadas en la tesis "Análisis cuantitativo de sesgos culturales en películas de Hollywood" a partir del corpus de subtítulos de [Open Subtitles](https://www.opensubtitles.org)

Las dos estructuras que se utilizan en la tesis son índice de frecuencias y matrices palabra-contexto. Para ambas es necesario configurar la ubicación del corpus en el archivo `config.py`:

```
subtitles_path = "../datasets/subtitulos/"
```

Reemplazar la variable `subtitles_path` por la ubicación del corpus.

# Directorio filtrado de películas

Para generar las estructuras utilizadas es necesario tener un directorio con todas las películas a analizar. El filtrado por país, duplicados, idioma, series o películas se realiza con el siguiente script:

``` $ python scripts/original_list_filter.py
```

# Índice de frecuencias

Este script genera un único archivo en formato pickle que contiene un diccionario cuyas claves son todas las palabras del corpus y los valores son otro diccionario que unifica año con cantidad de apariciones. Éste se genera con:

``` $ python scripts/build_frequency_index.py
```

# Matrices palabra-contexto

El script para generar las matrices crea un directorio `cooccurrence_matrices_X` con `X` la cantidad de segundos que tiene la ventana elegida. Dentro de ese directorio se almacenan un archivo pickle por año que se corresponde con la matriz palabra-contexto de ese año y un archivo `words_per_year.py` que recolecta las sumas totales de todas las posiciones de la matriz por cada año.

``` $ python scripts/build_matrices.py y
```

`y` es el tamaño de ventana en segundos. De no pasar ningún parámetro utiliza el default que es 5. 

