import sys
import os
sys.path.append('..')
from repo.statistician import Statistician

folder_path = "../generated_charts/"
if not os.path.exists(folder_path):
  os.makedirs(folder_path)

# freq_st = Statistician()
# freq_st.chart_frequency_for(
#   [["iraq", "iraqis", "iraqi"],["islam", "muslim", "muslims"],["terrorism","terrorist","terrorists"]],
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_iraq.png")
# )

# freq_st.chart_frequency_for(
#   [["russia", "russian", "russians"],["communist", "communism", "communists"]],
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_russia.png")
# )

# freq_st.chart_frequency_for(
#   [["she", "her", "hers"],["he", "him", "his"],["woman"],["man"]],
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_pronouns.png")
# )

# freq_st.chart_frequency_for(
#   [["homo", "homosexual","homosexuality"],["heterosexuality","hetero", "heterosexual"],["gay"],["lesbian"]],
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_homosexuality.png")
# )

for window_size in [3,5,20]:
  st = Statistician(window_size)

  st.chart_pmi_for(
    ["terrorism","terrorist","terrorists"],
    [["iraq", "iraqis", "iraqi"],["america","american","americans"],["italian","italy","italians"],["canada","canadian","canadians"]],
    title="PPMI de 'terrorist','terrorists' y 'terrorism'",
    save_to=(folder_path + str(window_size) + "_terrorism_nationality.png")
  )

  st.chart_pmi_for(
    ["terrorism","terrorist","terrorists"],
    [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
    title="PPMI de 'terrorist','terrorists' y 'terrorism'",
    save_to=(folder_path + str(window_size) + "_terorrism_religion.png")
  )

  st.chart_pmi_for(
    ["kitchen","cook","serve","dinner"],
    [["she","her","hers"],["him","his","he"]],
    title="PPMI de 'kitchen,'cook','serve','dinner'",
    save_to=(folder_path + str(window_size) + "_kitchen_cook_serve_dinner.png")
  )

  st.chart_pmi_for(
    ["sick","sickness"],
    [["woman"],["man"],["gay"]],
    title="PPMI de 'sick,'sickness'",
    save_to=(folder_path + str(window_size) + "_pmi_sick_sickness.png"),
    smoothing=3
  )

  st.chart_w2v_average_for(
    ["sick"],
    ["woman","man","gay"],
    title="W2V de 'sick'",
    save_to=(folder_path + str(window_size) + "_w2v_sick_sickness.png"),
    smoothing=3
  )
