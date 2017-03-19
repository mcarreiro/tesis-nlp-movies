import sys
sys.path.append('..')
from repo.statistician import Statistician
import fixture_statistician as Fixtures

# Run with: $ py.test test_statistician.py

st = Statistician()
pmi = st.yearly_pmi_for("granger","hermione",2009)

def test_entries_in_index_match_result():
  potter = st.word_frequency_for("potter")
  assert potter.keys() == st.index["potter"].keys()

def test_chart_format_has_every_year_in_between():
  potter = st.word_frequency_for("potter",chart_format=True)
  assert [tup[0] for tup in potter] == list(range(1930,2015))

def test_output_has_correct_frequencies():
  potter = st.word_frequency_for("potter")
  index_frequencies = st.index["potter"]
  val_2009 = index_frequencies[2014] / st.count_per_year[2014]
  assert potter[2014] == val_2009

# Need to be redone
# def test_pmi_is
# def test_joined_frequency_correct_window():
#   assert [k for k,v in pmi.items() if v["pmi"] != 0] == [2009, 2014]

def test_pmi_format_includes_counts():
  print(pmi)
  assert pmi["first"] == st.index["granger"]
  assert pmi["second"] == st.index["hermione"]
  assert pmi["n"] == st.count_per_year[2009]

def test_smoothed():
  data = {1990: 1, 1991: 1, 1992: 1, 1993: 1, 1994: 1}
  data = st.format_for_chart(data)
  res = st.smoothed(data, 2)
  assert res == data
