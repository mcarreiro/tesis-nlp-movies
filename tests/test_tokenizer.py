import sys
sys.path.append('..')
from repo.subtitle import Subtitle
from repo.tokenizer import Tokenizer
import re

# 1953230595 = Harry Potter and the Half Blood Prince (hearing impaired)
tokenizer = Tokenizer()
sub = Subtitle(1953230595)
text = sub.full_text()[:479]
clean = tokenizer.clean(text)
"""
What text looks like:

WOMAN:\nI killed Sirius Black!\n[WOMAN CACKLES]\nMAN:\nHe\'s back.\n[MAN YELLS]\n[PEOPLE SCREAMING]\n[CHATTERING]\n
[METAL SQUEAKING]\n[PEOPLE SCREAMING]\nMAN [ON RADIO]: The police are continuing\nwith the investigation...\n
...into the cause\nof the Millennium Bridge disaster.\nTraffic has been halted\nas police search for survivors.\n
The surrounding area remains closed.\nThe mayor has urged Londoners\nto remain calm....\n"Harry Potter."\n
Who\'s Harry Potter?\nOh, no one.\nBit of a tosser, really.\n
"""

# 1952521673 = Harry Potter and the Half Blood Prince (with styling)
sub_styled = Subtitle(1952521673)
text_styled = sub_styled.full_text()[:470]
"""
What text_styled looks like:

<i>I killed Sirius Black!</i>\n<i>He\'s back.</i>\nHARRY POTTER AND THE HALF-BLOOD PRINCE\n<i>The police are</i>\n
<i>continuing with the investigation...</i>\n<i>...into the cause</i>\n<i>of the Millennium Bridge disaster.</i>\n
<i>Traffic has been halted</i>\n<i>as police search for survivors.</i>\n<i>The surrounding area remains closed.</i>\n
<i>The mayor has urged Londoners</i>\n<i>to remain calm...</i>\n"Harry Potter. "\nWho\'s Harry Potter?\nOh, no one.\n
Bit of a tosser, really.\n
"""


def test_html_removal():
  clean_styled = tokenizer.clean(text_styled)
  assert clean_styled == 'I killed Sirius Black! He\'s back. The police are continuing with the investigation... ...into the cause of the Millennium Bridge disaster. Traffic has been halted as police search for survivors. The surrounding area remains closed. The mayor has urged Londoners to remain calm... "Harry Potter. " Who\'s Harry Potter? Oh, no one. Bit of a tosser, really.'

def test_sound_description_removal():
  # Since it's a hearing impaired version, removal of character names is also necessary
  assert clean == 'I killed Sirius Black! He\'s back. The police are continuing with the investigation... ...into the cause of the Millennium Bridge disaster. Traffic has been halted as police search for survivors. The surrounding area remains closed. The mayor has urged Londoners to remain calm.... "Harry Potter." Who\'s Harry Potter? Oh, no one. Bit of a tosser, really.'

def test_equal_results_after_cleanup():
  # They are not exactly the same because of an extra trailing space and an extra dot. Testing only first few chars for completeness (no '-'s, no names, no caps)
  clean2 = tokenizer.clean(text_styled)
  assert clean[:100] == clean2[:100]

def test_tokenize():
  tokens = tokenizer.tokenize(clean)
  assert tokens == ['i', 'killed', 'sirius', 'black', 'he', "'s", 'back', 'the', 'police', 'are', 'continuing', 'with', 'the', 'investigation', 'into', 'the', 'cause', 'of', 'the', 'millennium', 'bridge', 'disaster', 'traffic', 'has', 'been', 'halted', 'as', 'police', 'search', 'for', 'survivors', 'the', 'surrounding', 'area', 'remains', 'closed', 'the', 'mayor', 'has', 'urged', 'londoners', 'to', 'remain', 'calm', 'harry', 'potter', 'who', "'s", 'harry', 'potter', 'oh', 'no', 'one', 'bit', 'of', 'a', 'tosser', 'really']

def test_tokenize_downcases():
  # Verifies that there are no caps in the tokenized text
  tokens = tokenizer.tokenize(clean)
  assert len([word for word in tokens if re.match(r'[A-Z]', word)]) == 0

def test_he_she_not_in_stopwords():
  # Not much of mine, but testing that 'he' is still in there
  tokens = tokenizer.tokenize(clean)
  filtered = tokenizer.filter_stopwords(tokens)
  assert 'he' in filtered

def test_lemmatization():
  tokens = tokenizer.tokenize(clean)
  filtered = tokenizer.filter_stopwords(tokens)
  lemmatized = tokenizer.lemmatize(filtered)
  assert 'londoners' not in lemmatized
  assert 'londoner' in lemmatized

def test_full_run_returns_filtered_tokens():
  tokens = tokenizer.full_run(text)
  assert tokens == ['killed', 'sirius', 'black', 'he', "'s", 'back', 'police', 'continuing', 'investigation', 'cause', 'millennium', 'bridge', 'disaster', 'traffic', 'halted', 'police', 'search', 'survivors', 'surrounding', 'area', 'remains', 'closed', 'mayor', 'urged', 'londoners', 'remain', 'calm', 'harry', 'potter', "'s", 'harry', 'potter', 'oh', 'one', 'bit', 'tosser', 'really']
