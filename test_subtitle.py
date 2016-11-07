from subtitle import Subtitle

sub = Subtitle(1953230595)
# Line: 'MAN [ON RADIO]: The police are continuing\nwith the investigation...'
time = '00:02:55,641' # sub.raw_sub[8].start.__str__()

def test_open_sub():
  assert sub.raw_sub[0].text == "WOMAN:\nI killed Sirius Black!"

def test_full_text_is_string():
  assert isinstance(sub.full_text(), str)

def test_context_if_word_list():
  assert isinstance(sub.context_of('police', time, 3), list)

def test_context_is_accurate_for_3_secs():
  assert set(sub.context_of('police', time, 3)) == set(['investigation',
    'disaster',
    'continuing',
    'police',
    'bridge',
    'millennium',
    'cause'])

def test_context_is_accurate_for_10_secs():
  assert set(sub.context_of('police', time, 10)) == set(['investigation',
    'disaster',
    'continuing',
    'police',
    'bridge',
    'millennium',
    'cause',
    'surrounding',
    'remains',
    'closed',
    'survivors',
    'halted',
    'search',
    'area',
    'traffic'])
