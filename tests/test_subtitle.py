import sys
sys.path.append('..')
from repo.subtitle import Subtitle

sub = Subtitle(1953230595)
time8 = '00:02:55,641' # sub.raw_sub[8].start.__str__()
time49 = '00:07:34,515'

def test_open_sub():
  assert sub.raw_sub[0].text == "WOMAN:\nI killed Sirius Black!"

def test_full_text_is_string():
  assert isinstance(sub.full_text(), str)

def test_context_if_word_list():
  assert isinstance(sub.context_of('police', time8, 3), list)

def test_context_is_accurate_for_3_secs():
  # (0, 2, 58, 348) + 3s = (0, 3, 01, 348)
  # line 8: 'The police are continuing with the investigation...'
  # line 9: '...into the cause of the Millennium Bridge disaster.'
  # line 10: 'Traffic has been halted as police search for survivors.' - start(0, 3, 0, 730)
  assert set(sub.context_of('police', time8, 3)) == set(['the', 'police', 'are', 'continuing', 'with', 'the',
    'investigation', 'into', 'the', 'cause', 'of', 'the', 'millennium', 'bridge', 'disaster', 'traffic', 'has',
    'been', 'halted', 'as', 'police', 'search', 'for', 'survivors'])

def test_context_is_accurate_for_10_secs():
  # (0, 2, 58, 348) + 10s = (0, 3, 08, 348)
  # line 8: 'The police are continuing with the investigation...'
  # line 9: '...into the cause of the Millennium Bridge disaster.'
  # line 10: 'Traffic has been halted as police search for survivors.'
  # line 11: 'The surrounding area remains closed.'
  # line 12: 'The mayor has urged Londoners to remain calm....' - start(0, 3, 6, 444)
  assert set(sub.context_of('police', time8, 10)) == set(['the', 'police', 'are', 'continuing', 'with', 'the',
    'investigation', 'into', 'the', 'cause', 'of', 'the', 'millennium', 'bridge', 'disaster', 'traffic', 'has',
    'been', 'halted', 'as', 'police', 'search', 'for', 'survivors', 'the', 'surrounding', 'area', 'remains', 'closed',
    'the', 'mayor', 'has', 'urged', 'londoners', 'to', 'remain', 'calm'])

def test_context_window_includes_prev_sub():
  # line 47: "Harry, I'd like you to meet an old friend and colleague of mine..." -> (0, 7, 28, 717) - (0, 7, 32, 710)
  # line 48: '...Horace Slughorn.'
  # line 49: 'Horace...' -> (0, 7, 34, 515)
  # Time(49) - 3s = (0, 7, 31, 515)
  assert sub.context_of('horace', time49, 3).count("friend") > 0
  assert sub.context_of('horace', time49, 3).count("like") > 0

def test_context_window_includes_following_sub():
  # line 49: 'Horace...' -> (0, 7, 34, 515)
  # line 50: '...well, you know who this is.'
  # line 51: 'Harry Potter.'
  # line 53: "What's with all the theatrics, Horace?" -> (0, 7, 44, 692) - (0, 7, 46, 432)
  # Time(49)-end : (0, 7, 36, 5) + 9s = (0, 7, 45, 5)
  assert sub.context_of('horace', time49, 9).count("know") > 0
  assert sub.context_of('horace', time49, 9).count("potter") > 0
  assert sub.context_of('horace', time49, 9).count("theatrics") > 0

def test_context_window_counts_after_end():
  # line 49: 'Horace...' -> (0, 7, 34, 515)
  # line 50: '...well, you know who this is.'
  # Time(49)-end : (0, 7, 36, 5) + 1s = (0, 7, 37, 5)
  assert sub.context_of('horace', time49, 11).count("who") > 0
