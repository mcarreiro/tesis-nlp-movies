from textblob import TextBlob
from textblob import Word
from nltk.corpus import stopwords
import re

class Tokenizer(object):

  def clean(self, text):
    # Removes tags, replaces & for 'and', removes anything between ( and ), or [ and ]

    clean_text = re.sub('<[^>]*>', '', text)
    clean_text = re.sub(r'\(.*\)', '', clean_text)
    clean_text = re.sub(r'\[.*\]', '', clean_text)
    clean_text = re.sub(r'([A-Z]){2,}(\s:)?:?', '', clean_text)
    clean_text = clean_text.replace('-', '')
    clean_text = clean_text.replace('&', 'and')
    clean_text = ' '.join(clean_text.split()) # Removes trailing or extra whitespace

    return clean_text

  def tokenize(self, text):
    # Separates into list of words

    blob = TextBlob(text)
    downcased = [word.lower() for word in blob.words]
    return downcased

  def filter_stopwords(self, list_of_tokens):
    # Remove stopwords according to NLTK's stopword list
    # I'm going to retain he, him, his and she, her, hers
    words_for_removal = list(stopwords.words('english'))
    words_for_removal.remove('he')
    words_for_removal.remove('she')
    words_for_removal.remove('her')
    words_for_removal.remove('hers')
    words_for_removal.remove('him')
    words_for_removal.remove('his')
    return [word for word in list_of_tokens if word not in words_for_removal]

  def lemmatize(self, list_of_tokens):
    # Given a tokenized text, lemmatizes all nouns (otherwise it requires POS analisys)
    # THIS TAKES A LONG TIME EVEN FOR A SHORT STRING
    return [Word(word).lemmatize() for word in list_of_tokens]

  def full_run(self, text):
    result = self.clean(text)
    result = self.tokenize(result)
    result = self.filter_stopwords(result)
    return result
