from statistician import Statistician
import fixture_statistician as Fixtures

st = Statistician()

def test_entries_in_index_match_result():
  potter = st.word_frequency_for("potter")
  assert potter.keys() == st.index["potter"].keys()

def test_chart_format_has_every_year_in_between():
  potter = st.word_frequency_for("potter",chart_format=True)
  assert [tup[0] for tup in potter] == list(range(1930,2014))

def test_output_has_correct_frequencies():
  potter = st.word_frequency_for("potter")
  index_frequencies = st.index["potter"]
  val_2009 = index_frequencies['2014'] / st.count_per_year[2014]
  assert potter['2014'] == val_2009

def test_joined_frequency_counts_each_appearance():
  # Hermione: '00:22:03,213'(0, 22, 3, 783),*'00:22:03,783'(0, 22, 4, 443),*'00:22:04,443',*'00:22:04,443'
  # Granger: '00:22:06,853'
  st.full_index = Fixtures.miniature_index
  freq = st.joined_frequency_for("granger","hermione",3)
  assert freq[2009] == 3 / st.count_per_year[2009]

def test_joined_frequency_counts_each_appearance_backwards():
  # Hermione: '00:22:03,213'(0, 22, 3, 783),*'00:22:03,783'(0, 22, 4, 443),*'00:22:04,443',*'00:22:04,443'
  # Granger: '00:22:06,853'
  st.full_index = Fixtures.miniature_index2
  freq = st.joined_frequency_for("granger","hermione",3)
  assert freq[2009] == 3 / st.count_per_year[2009]

# def test_joined_frequency_correct_window():
#   assert [k for k,v in st.pmi_for("granger","hermione",10, Fixtures.test_index).items() if v != 0] == [2009, 2014]

