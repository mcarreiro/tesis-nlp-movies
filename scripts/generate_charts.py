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

  ## Terrorismo e Islam

  st.chart_pmi_for(
    ["terrorism","terrorist","terrorists"],
    [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestina","palestinian"]],
    title="PPMI de 'terrorist','terrorists' y 'terrorism' (Nacionalidad)",
    save_to=(folder_path + "terrorism_nationality_" + str(window_size) + ".png")
  )

  st.chart_pmi_for(
    ["terrorism","terrorist","terrorists"],
    [["lonewolf","gunman"],["band","gang"],["fanatic","fanatics","fanaticism"],["extremist","extremism","extremists"],["money","ransom"]],
    title="PPMI de'terrorist','terrorists' y 'terrorism' (Perfil)",
    save_to=(folder_path + "terrorism_profile_" + str(window_size) + ".png")
  ),

  st.chart_pmi_for(
    ["terrorism","terrorist","terrorists"],
    [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
    title="PPMI de 'terrorist','terrorists' y 'terrorism' (Religión)",
    save_to=(folder_path + "terorrism_religion_" + str(window_size) + ".png")
  )

  st.chart_pmi_for(
    ["muslim","islam","muslims"],
    [["rat","rats"],["scurry","swarm","slither","scurrying","slithering","swarming","swarmed","scurried","slithered"],["breed","breeding"],["hunt","hunted","hunting","trap","trapped","net","netting","snare","snaring","bait","baiting"],["entrapment","capture","capturing","cage","caged"],["nest","lair","nests","lairs"]],
    title="PPMI de 'terrorist','terrorists' y 'terrorism' (Deshumanización)",
    save_to=(folder_path + "terorrism_deshumanization_" + str(window_size) + ".png")
  )

  ## Rusia como enemigo

  st.chart_pmi_for(
    ["russia","russian","russians"],
    [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["ally","allies"],["worker","workers","job","work"],["bride","brides","mailorder"]],
    title="PPMI de 'russia','russian' y 'russians'",
    save_to=(folder_path + "russia_associations_" + str(window_size) + ".png"),
    smoothing=3
  )

  st.chart_pmi_for(
    ["russia","russian","russians"],
    [["rat","rats"],["scurry","swarm","slither","scurrying","slithering","swarming","swarmed","scurried","slithered"],["breed","breeding"],["hunt","hunted","hunting","trap","trapped","net","netting","snare","snaring","bait","baiting"],["entrapment","capture","capturing","cage","caged"],["nest","lair","nests","lairs"]],
    title="PPMI de 'russia','russian' y 'russians' (Deshumanización)",
    save_to=(folder_path + "russia_dehumanization_" + str(window_size) + ".png")
  )

  st.chart_pmi_for(
    ["russia","russian","russians"],
    [["violent","violence"],["execute","execution","executions"],["love","romance"],["friend","friends"],["he"],["she"]],
    title="PPMI de 'russia','russian' y 'russians' (Violencia)",
    save_to=(folder_path + "russia_violence_" + str(window_size) + ".png")
  )

  # st.chart_pmi_for(
  #   ["kitchen","cook","serve","dinner"],
  #   [["she","her","hers"],["him","his","he"]],
  #   title="PPMI de 'kitchen,'cook','serve','dinner'",
  #   save_to=(folder_path + str(window_size) + "_kitchen_cook_serve_dinner.png")
  # )

  # st.chart_pmi_for(
  #   ["sick","sickness"],
  #   [["woman"],["man"],["gay"]],
  #   title="PPMI de 'sick,'sickness'",
  #   save_to=(folder_path + str(window_size) + "_pmi_sick_sickness.png"),
  #   smoothing=3
  # )

  # st.chart_w2v_average_for(
  #   ["sick"],
  #   ["woman","man","gay"],
  #   title="W2V de 'sick'",
  #   save_to=(folder_path + str(window_size) + "_w2v_sick_sickness.png"),
  #   smoothing=3
  # )
