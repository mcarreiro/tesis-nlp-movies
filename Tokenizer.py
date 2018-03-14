from textblob import TextBlob
from textblob import Word
from nltk.corpus import stopwords
from nltk.corpus import wordnet
import re

# Set which ones are the stopwords
words_for_removal = list(stopwords.words('english'))
words_for_removal.remove('he')
words_for_removal.remove('she')
words_for_removal.remove('her')
words_for_removal.remove('hers')
words_for_removal.remove('him')
words_for_removal.remove('his')
words_for_removal.remove('herself')
words_for_removal.remove('himself')
words_for_removal = set(words_for_removal)

page_names = set(['www.addic7ed.com',
                  'www.allsubs.org',
                  'www.ncicap.org',
                  'www.opensubtitles.org',
                  'www.titlovi.com',
                  'www.podnapisi.net'])

def wordnet_pos_code(tag):
    if tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    else:
        return None


class Tokenizer(object):

    def clean(self, text):
        # Removes tags, replaces & for 'and', removes anything between ( and ), or [ and ]
        # clean_text = re.sub('<[^>]*>', ' ', text)  # Now we use text_without_tags in pysrt
        clean_text = re.sub(r'\(.*? \)', ' ', text)
        clean_text = re.sub(r'\[.*?\]', ' ', clean_text)
        clean_text = re.sub(r'.*: (.*)', ' ', clean_text)  # Used to be re.sub(r'([A-Z]){2,}(\s:)?:?', '', clean_text)
        clean_text = re.sub("\s*?\-\s*?\:*?", ' ', clean_text)
        clean_text = re.sub("\s*\&s*", "and", clean_text)
        clean_text = ' '.join(clean_text.split())  # Removes trailing or extra whitespace

        return clean_text

    def tokenize(self, text):
        # Separates into list of words
        blob = TextBlob(text)
        tokens = [word.lower() for word in blob.words]
        tokens = filter(lambda x: re.compile("\w+").search(x), tokens)  # Keep words with at least one alphanumeric character
        tokens = filter(lambda x: x not in page_names, tokens)  # Keep words with at least one alphanumeric character
        return list(tokens)

    def filter_stopwords(self, list_of_tokens, words_for_removal=words_for_removal):
        # Remove stopwords according to NLTK's stopword list
        # I'm going to retain he, him, his and she, her, hers
        return [word for word in list_of_tokens if word not in words_for_removal]

    def lemmatize(self, list_of_tokens):
        # Given a tokenized text, lemmatizes all nouns (otherwise it requires POS analisys)
        # THIS TAKES A LONG TIME EVEN FOR A SHORT STRING
        pos_tags = [TextBlob(e).tags[0] for e in list_of_tokens]
        return [Word(word).lemmatize(wordnet_pos_code(tag)) for (word, tag) in pos_tags]

    def full_run(self, text):  # I will not remove stopwords, we'll do that later on
        result = self.clean(text)
        result = self.tokenize(result)
        # result = self.filter_stopwords(result)
        return result
