import sys
import os
sys.path.append('..')
from repo.statistician import Statistician

folder_path = "../generated_charts/"
if not os.path.exists(folder_path):
  os.makedirs(folder_path)

freq_st = Statistician()
# freq_st.chart_frequency_for(
#   [["iraq", "iraqis", "iraqi"],["afghan", "afghans","afghanistan"],["islam", "muslim", "muslims"],["terrorism","terrorist","terrorists"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_iraq.png")
# )

# freq_st.chart_frequency_for(
#   [["russia", "russian", "russians"],["communist", "communism", "communists"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_russia.png")
# )

# freq_st.chart_frequency_for(
#   [["she", "her", "hers"],["he", "him", "his"],["woman"],["man"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_pronouns.png")
# )

res = {}
fem = freq_st.word_frequency_for(["she","her","hers"])
masc = freq_st.word_frequency_for(["he","him","his"])
for y in range(1930,2016):
  res[y] = masc[y] / fem[y]
for_chart = freq_st.format_for_chart(res)
for_chart = freq_st.smoothed(for_chart,3)
freq_st.chart([for_chart],
  ["Frecuencia H / frecuencia M"],
  title="Comparación de frecuencias de pronombres femeninos y masculinos",
  save_to=folder_path + "freq_pronoun_comparison.png",
  vertical_markers=[1945,1968])


# freq_st.chart_frequency_for(
#   [["homo", "homosexual","homosexuality"],["heterosexuality","hetero", "heterosexual"],["gay"],["lesbian"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_homosexuality.png")
# )

# freq_st.chart_frequency_for(
#   [["educated","education","school","study","studies","educate"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_education.png")
# )


for window_size in [3,5,10,20]:
  st = Statistician(window_size)

  ## Terrorismo e Islam

  # st.chart_pmi_for(
  #   ["terrorism","terrorist","terrorists"],
  #   [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestina","palestinian","palestinians"],["afghan", "afghans", "afghanstan"],["pakistan","pakistani","pakistanis"]],
  #   smoothing=3,
  #   title="PPMI de 'terrorist','terrorists' y 'terrorism' (Nacionalidad)",
  #   save_to=(folder_path + "terrorism_nationality_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["terrorism","terrorist","terrorists"],
  #   [["lonewolf","gunman"],["band","gang"],["fanatic","fanatics","fanaticism"],["extremist","extremism","extremists"],["money","ransom"]],
  #   smoothing=3,
  #   title="PPMI de'terrorist','terrorists' y 'terrorism' (Perfil)",
  #   save_to=(folder_path + "terrorism_profile_" + str(window_size) + ".png")
  # ),

  # st.chart_pmi_for(
  #   ["terrorism","terrorist","terrorists"],
  #   [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
  #   smoothing=3,
  #   title="PPMI de 'terrorist','terrorists' y 'terrorism' (Religión)",
  #   save_to=(folder_path + "terorrism_religion_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["muslim","islam","muslims"],
  #   [["rat","rats"],["scurry","swarm","slither","scurrying","slithering","swarming","swarmed","scurried","slithered"],["breed","breeding"],["hunt","hunted","hunting","trap","trapped","net","netting","snare","snaring","bait","baiting"],["entrapment","capture","capturing","cage","caged"],["nest","lair","nests","lairs"]],
  #   smoothing=3,
  #   title="PPMI de 'terrorist','terrorists' y 'terrorism' (Deshumanización)",
  #   save_to=(folder_path + "terorrism_deshumanization_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["muslim","islam","muslims"],
  #   [["rat","rats"],["hunt","hunted","hunting"],["cage","caged","cages"],["nest","nesting"],["arrest","arrested","arrests"],["prison","prisons","prisoner","prisoners"],["hideout","refuge","shelter"]],
  #   smoothing=3,
  #   title="PPMI de 'terrorist','terrorists' y 'terrorism' (Deshumanización)",
  #   save_to=(folder_path + "terorrism_deshumanization2_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["terrorism","terrorist","terrorists"],
  #   [["rat","rats"],["hunt","hunted","hunting"],["cage","caged","cages"],["nest","nesting"],["arrest","arrested","arrests"],["prison","prisons","prisoner","prisoners"],["hideout","refuge","shelter"]],
  #   smoothing=3,
  #   title="PPMI de 'muslim', 'muslims' e 'islam' (Deshumanización)",
  #   save_to=(folder_path + "terorrism_muslim_deshumanization2_" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   ["terrorism","terrorist","terrorists"],
  #   [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestina","palestinian","palestinians"],["afghan", "afghans", "afghanstan"],["pakistan","pakistani","pakistanis"]],
  #   title="Test hipergeométrico de 'terrorist','terrorists' y 'terrorism' (Nacionalidad)",
  #   save_to=(folder_path + "hg_terrorism_nationality_" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   ["terrorism","terrorist","terrorists"],
  #   [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
  #   title="Test hipergeométrico de 'terrorist','terrorists' y 'terrorism' (Religión)",
  #   save_to=(folder_path + "hg_terorrism_religion_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   "terrorist",
  #   [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestina","palestinian","palestinians"],["afghan", "afghans", "afghanstan"],["pakistan","pakistani","pakistanis"]],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de las nacionalidades vs. 'terrorist' (Nacionalidad)",
  #   save_to=(folder_path + "terrorism_nationality2_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["iraqi", "italian", "arab","palestinian","pakistani","afghan"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Promedio W2V del contexto de 'terrorist' (Nacionalidad)",
  #   save_to=(folder_path + "terrorism_nationality_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["gunman","gang","fanatic","extremist","money"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Promedio W2V del contexto de 'terrorist' (Perfil)",
  #   save_to=(folder_path + "terrorism_profile_w2v_" + str(window_size) + ".png")
  # ),

  # st.chart_w2v_average_for(
  #   "terrorist",
  #   [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de cada religión vs. 'terrorist' (Religión)",
  #   save_to=(folder_path + "terorrism_religion2_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["muslim","christian","jew"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de 'terrorist' (Religión)",
  #   save_to=(folder_path + "terorrism_religion_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["rat","hunt","cage","nest","arrest","prison","hideout"],
  #   ["muslim","muslims","islam"],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de 'muslim' (Deshumanización)",
  #   save_to=(folder_path + "terorrism_muslim_dehumanization2_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["rat","hunt","cage","nest","arrest","prison","hideout"],
  #   ["terrorist","terrorism","terrorists"],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de 'terrorist' (Deshumanización)",
  #   save_to=(folder_path + "terorrism_dehumanization2_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "terrorist",
  #   [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestina","palestinian","palestinians"],["afghan", "afghans", "afghanstan"],["pakistan","pakistani","pakistanis"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de las nacionalidades vs. 'terrorist' (Nacionalidad)",
  #   save_to=(folder_path + "terrorism_nationality2_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   ["iraqi", "italian", "arab","palestinian","pakistani","afghan"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'terrorist' (Nacionalidad)",
  #   save_to=(folder_path + "terrorism_nationality_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   ["gunman","gang","fanatic","extremist","money"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'terrorist' (Perfil)",
  #   save_to=(folder_path + "terrorism_profile_w2v_th_" + str(window_size) + ".png")
  # ),

  # st.chart_w2v_threshold_for(
  #   "terrorist",
  #   [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de religiones vs. 'terrorist' (Religión)",
  #   save_to=(folder_path + "terorrism_religion2_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   ["muslim","christian","jew"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'terrorist' (Religión)",
  #   save_to=(folder_path + "terorrism_religion_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   ["rat","hunt","cage","nest","arrest","prison","hideout"],
  #   ["muslim","muslims","islam"],
  #   smoothing=3,
  #   title="Threshold W2V de 'muslim' (Deshumanización)",
  #   save_to=(folder_path + "terorrism_muslim_dehumanization2_w2v_th_" + str(window_size) + ".png")
  # )


  # st.chart_w2v_threshold_for(
  #   ["rat","hunt","cage","nest","arrest","prison","hideout"],
  #   ["terrorist","terrorism","terrorists"],
  #   smoothing=3,
  #   title="Threshold W2V de 'terrorist' (Deshumanización)",
  #   save_to=(folder_path + "terorrism_dehumanization2_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["terrorist","terrorism","terrorists"],
  #   [["gun","machinegun","pistol","shoot","shooting","shooter"],["bomb","bombing","bomber","explosive","explosion"],["fire","burn","arson","arsonist"]],
  #   smoothing=3,
  #   title="PPMI de terrorist contra distintas armas",
  #   save_to=(folder_path + "terorrism_weapons_pmi" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   ["gun", "bomb", "arson"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'terrorist' (Armas)",
  #   save_to=(folder_path + "terrorism_weapons_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["gun", "bomb", "arson"],
  #   ["terrorist","terrorists","terrorism"],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de 'terrorist' (Armas)",
  #   save_to=(folder_path + "terrorism_weapons_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   ["terrorist","terrorism","terrorists"],
  #   [["gun","machinegun","pistol","shoot","shooting","shooter"],["bomb","bombing","bomber","explosive","explosion"],["fire","burn","arson","arsonist"]],
  #   title="Test hipergeométrico de 'terrorist','terrorists' y 'terrorism' (Armas)",
  #   save_to=(folder_path + "terrorism_weapons_hg" + str(window_size) + ".png")
  # )

  ## Rusia como enemigo

  # st.chart_pmi_for(
  #   ["russia","russian","russians"],
  #   [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["ally","allies"],["worker","workers","job","work"],["bride","brides","mailorder"]],
  #   smoothing=3,
  #   title="PPMI de 'russia','russian' y 'russians'",
  #   save_to=(folder_path + "russia_associations_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["russia","russian","russians"],
  #   [["rat","rats"],["scurry","swarm","slither","scurrying","slithering","swarming","swarmed","scurried","slithered"],["breed","breeding"],["hunt","hunted","hunting","trap","trapped","net","netting","snare","snaring","bait","baiting"],["entrapment","capture","capturing","cage","caged"],["nest","lair","nests","lairs"]],
  #   smoothing=3,
  #   title="PPMI de 'russia','russian' y 'russians' (Deshumanización)",
  #   save_to=(folder_path + "russia_dehumanization_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["rat","rats","scurry","swarm","slither","scurrying","slithering","swarming","swarmed","scurried","slithered","breed","breeding","hunt","hunted","hunting","trap","trapped","net","netting","snare","snaring","bait","baiting","entrapment","capture","capturing","cage","caged","nest","lair","nests","lairs"],
  #   [["russia","russian","russians"],["italy","italian","italians"],["spain","spanish"],["canada","canadian","canadians"],["mexico","mexican","mexicans"]],
  #   smoothing=3,
  #   title="PPMI de vocabulario relacionado a rodeores, insectos y enfermedades (Deshumanización)",
  #   save_to=(folder_path + "russia_countries_dehumanization_" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["russia","russian","russians"],
  #   [["violent","violence"],["execute","execution","executions"],["love","romance"],["friend","friends"],["he"],["she"]],
  #   smoothing=3,
  #   title="PPMI de 'russia','russian' y 'russians' (Violencia)",
  #   save_to=(folder_path + "russia_violence_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   "russian",
  #   [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["ally","allies"],["worker","workers","job","work"],["bride","brides","mailorder"]],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de asociaciones vs 'russian'",
  #   save_to=(folder_path + "russia_associations2_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["communist","mafia","gangster","ally","worker","bride"],
  #   ["russian","russians","russia"],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de 'russian'",
  #   save_to=(folder_path + "russia_associations_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   "rat",
  #   [["russia","russian","russians"],["italy","italian","italians"],["mexico","mexican","mexicans"]],
  #   smoothing=3,
  #   title="Promedio W2V de 'rat' (Deshumanización)",
  #   save_to=(folder_path + "russia_countries_rat_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   "russian",
  #   [["violent","violence"],["execute","execution","executions"],["love","romance"],["friend","friends"]],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de otredad violenta y amistad vs. 'russian' (Violencia)",
  #   save_to=(folder_path + "russia_violence2_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(
  #   ["violent","execution","romantic","friend"],
  #   ["russian","russians","russia"],
  #   smoothing=3,
  #   title="Promedio W2V de los contextos de 'russian' (Violencia)",
  #   save_to=(folder_path + "russia_violence_w2v_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "russian",
  #   [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["ally","allies"],["worker","workers","job","work"],["bride","brides","mailorder"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de estereotipos vs. 'russia'",
  #   save_to=(folder_path + "russia_associations2_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   ["communist","mafia","gangster","ally","worker","bride"],
  #   ["russian","russians","russia"],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'russia' (Estereotipos)",
  #   save_to=(folder_path + "russia_associations_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "rat",
  #   [["russia","russian","russians"],["italy","italian","italians"],["spain","spanish"],["canada","canadian","canadians"],["mexico","mexican","mexicans"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de países vs. 'rat' (Deshumanización)",
  #   save_to=(folder_path + "russia_countries_rat_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   ["violent","execution","romantic","friend"],
  #   ["russian","russians","russia"],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'russian' (Otredad y violencia)",
  #   save_to=(folder_path + "russia_violence_w2v_th_" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   ["russia","russian","russians"],
  #   [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["ally","allies"],["worker","workers","job","work"],["bride","brides","mailorder"]],
  #   title="Test hipergeométrico de 'russia','russian' y 'russians'",
  #   save_to=(folder_path + "hg_russia_associations_" + str(window_size) + ".png"),
  #   smoothing=3
  # )

  # st.chart_hypergeo_for(
  #   ["russia","russian","russians"],
  #   [["violent","violence"],["execute","execution","executions"],["love","romance"],["friend","friends"]],
  #   title="Test hipergeométrico de 'russia','russian' y 'russians' (Violencia)",
  #   save_to=(folder_path + "hg_russia_violence_" + str(window_size) + ".png")
  # )




  ## Rol de la mujer

  # st.chart_pmi_for(
  #   [
  #     "yielding",
  #     "cheerful",
  #     "shy",
  #     "affectionate",
  #     "flatterable",
  #     "loyal",
  #     #"feminine",
  #     "sympathetic",
  #     "sensitive",
  #     "understanding",
  #     "compassionate",
  #     # "eager to soothe hurt feelings",
  #     "soft",
  #     "warm",
  #     "tender",
  #     "gullible",
  #     "childlike",
  #     "sweet", # does not use harsh language
  #     "loving",
  #     "gentle"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Palabras asociadas a femeneidad en 1974 (PPMI)",
  #   save_to=(folder_path + "bsri_fem_pmi" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   [
  #     "yielding",
  #     "cheerful",
  #     "shy",
  #     "affectionate",
  #     "flatterable",
  #     "loyal",
  #     # "feminine",
  #     "sympathetic",
  #     "sensitive",
  #     "understanding",
  #     "compassionate",
  #     # "eager to soothe hurt feelings",
  #     "soft",
  #     "warm",
  #     "tender",
  #     "gullible",
  #     "childlike",
  #     "sweet", # does not use harsh language
  #     "loving",
  #     "gentle"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Palabras asociadas a femeneidad en 1974 (HG)",
  #   save_to=(folder_path + "bsri_fem_hg" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   [
  #     "selfreliant",
  #     # "defends own beliefs",
  #     "independent",
  #     "athletic",
  #     "assertive",
  #     "strong",
  #     "forceful",
  #     "analytical",
  #     # "leadership ability",
  #     "brave",# "willing to take risks",
  #     "decisive",
  #     "selfsufficient",
  #     "dominant",
  #     # "masculine",
  #     "assured",#"willing to take a stand",
  #     "aggressive",
  #     "leader", # acts as a leader
  #     "individualistic",
  #     "competitive",
  #     "ambitious"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Palabras asociadas a masculinidad en 1974 (PPMI)",
  #   save_to=(folder_path + "bsri_masc_pmi" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   [
  #     "selfreliant",
  #     # "defends own beliefs",
  #     "independent",
  #     "athletic",
  #     "assertive",
  #     "strong",
  #     "forceful",
  #     "analytical",
  #     # "leadership ability",
  #     "brave",# "willing to take risks",
  #     "decisive",
  #     "selfsufficient",
  #     "dominant",
  #     # "masculine",
  #     "assured",#"willing to take a stand",
  #     "aggressive",
  #     "leader", # acts as a leader
  #     "individualistic",
  #     "competitive",
  #     "ambitious"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Palabras asociadas a masculinidad en 1974 (HG)",
  #   save_to=(folder_path + "bsri_masc_hg" + str(window_size) + ".png")
  # )


  # st.chart_pmi_for(
  #   [
  #     "helpful",
  #     "moody",
  #     "conscientious",
  #     "theatrical",
  #     "happy",
  #     "unpredictable",
  #     "reliable",
  #     "jealous",
  #     "truthful",
  #     "secretive",
  #     "sincere",
  #     "conceited",
  #     "likable",
  #     "solemn",
  #     "friendly",
  #     "inefficient",
  #     "adaptable",
  #     "unsystematic",
  #     "tactful",
  #     "conventional"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Palabras neutrales en 1974 (PPMI)",
  #   save_to=(folder_path + "bsri_neu_pmi" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   [
  #     "helpful",
  #     "moody",
  #     "conscientious",
  #     "theatrical",
  #     "happy",
  #     "unpredictable",
  #     "reliable",
  #     "jealous",
  #     "truthful",
  #     "secretive",
  #     "sincere",
  #     "conceited",
  #     "likable",
  #     "solemn",
  #     "friendly",
  #     "inefficient",
  #     "adaptable",
  #     "unsystematic",
  #     "tactful",
  #     "conventional"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Palabras neutrales en 1974 (HG)",
  #   save_to=(folder_path + "bsri_neu_hg" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   [
  #     "beautician",
  #     "caregiver",
  #     "cheerleader",
  #     "dancer",
  #     "decorator",
  #     "designer",
  #     "dietician",
  #     "florist",
  #     "hairdresser",
  #     "homemaker",
  #     "housekeeper",
  #     "model",
  #     "nanny",
  #     "nurse",
  #     "receptionist",
  #     "stylist",
  #     "typist"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Roles femeninos (PPMI)",
  #   save_to=(folder_path + "roles_fem_pmi" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   [
  #     "beautician",
  #     "caregiver",
  #     "cheerleader",
  #     "dancer",
  #     "decorator",
  #     "designer",
  #     "dietician",
  #     "florist",
  #     "hairdresser",
  #     "homemaker",
  #     "housekeeper",
  #     "model",
  #     "nanny",
  #     "nurse",
  #     "receptionist",
  #     "stylist",
  #     "typist"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Roles femeninos (HG)",
  #   save_to=(folder_path + "roles_fem_hg" + str(window_size) + ".png")
  # )


  # st.chart_pmi_for(
  #   [
  #     "assistant",
  #     "cashier",
  #     "clerk",
  #     "doctor",
  #     "editor",
  #     "lawyer",
  #     "poet",
  #     "reporter",
  #     "servant",
  #     "worker"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Roles neutrales (PPMI)",
  #   save_to=(folder_path + "roles_neu_pmi" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   [
  #     "assistant",
  #     "cashier",
  #     "clerk",
  #     "doctor",
  #     "editor",
  #     "lawyer",
  #     "poet",
  #     "reporter",
  #     "servant",
  #     "worker"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Roles neutrales (HG)",
  #   save_to=(folder_path + "roles_neu_hg" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   [
  #     "architect",
  #     "carpenter",
  #     "coach",
  #     "contractor",
  #     "detective",
  #     "electrician",
  #     "engineer",
  #     "farmer",
  #     "firefighter",
  #     "gambler",
  #     "inventor",
  #     "machinist",
  #     "mechanic",
  #     "officer",
  #     "physicist",
  #     "pilot",
  #     "programmer",
  #     "rancher",
  #     "sheriff",
  #     "soldier"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Roles masculinos (PPMI)",
  #   save_to=(folder_path + "roles_masc_pmi" + str(window_size) + ".png")
  # )

  # st.chart_hypergeo_for(
  #   [
  #     "architect",
  #     "carpenter",
  #     "coach",
  #     "contractor",
  #     "detective",
  #     "electrician",
  #     "engineer",
  #     "farmer",
  #     "firefighter",
  #     "gambler",
  #     "inventor",
  #     "machinist",
  #     "mechanic",
  #     "officer",
  #     "physicist",
  #     "pilot",
  #     "programmer",
  #     "rancher",
  #     "sheriff",
  #     "soldier"
  #   ],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Roles masculinos (HG)",
  #   save_to=(folder_path + "roles_masc_hg" + str(window_size) + ".png")
  # )

  # st.chart_w2v_average_for(["she","he"],[
  #     "architect",
  #     "carpenter",
  #     "coach",
  #     "contractor",
  #     "detective",
  #     "electrician",
  #     "engineer",
  #     "farmer",
  #     "firefighter",
  #     "gambler",
  #     "inventor",
  #     "machinist",
  #     "mechanic",
  #     "officer",
  #     "physicist",
  #     "pilot",
  #     "programmer",
  #     "rancher",
  #     "sheriff",
  #     "soldier"
  #   ],
  #   smoothing=3,
  #   title="Roles masculinos (Promedio W2V)",
  #   save_to=(folder_path + "roles_masc_w2v" + str(window_size) + ".png"))


  # st.chart_w2v_threshold_for(["she","he"],[
  #     "architect",
  #     "carpenter",
  #     "coach",
  #     "contractor",
  #     "detective",
  #     "electrician",
  #     "engineer",
  #     "farmer",
  #     "firefighter",
  #     "gambler",
  #     "inventor",
  #     "machinist",
  #     "mechanic",
  #     "officer",
  #     "physicist",
  #     "pilot",
  #     "programmer",
  #     "rancher",
  #     "sheriff",
  #     "soldier"
  #   ],
  #   smoothing=3,
  #   title="Roles masculinos (Threshold W2V)",
  #   save_to=(folder_path + "roles_masc_w2v_th" + str(window_size) + ".png"))


  # st.chart_w2v_average_for(["she","he"],[
  #     "beautician",
  #     "caregiver",
  #     "cheerleader",
  #     "dancer",
  #     "decorator",
  #     "designer",
  #     "dietician",
  #     "florist",
  #     "hairdresser",
  #     "homemaker",
  #     "housekeeper",
  #     "model",
  #     "nanny",
  #     "nurse",
  #     "receptionist",
  #     "stylist",
  #     "typist"
  #   ],
  #   smoothing=3,
  #   title="Roles femeninos (Promedio W2V)",
  #   save_to=(folder_path + "roles_fem_w2v" + str(window_size) + ".png"))


  # st.chart_w2v_threshold_for(["she","he"],[
  #     "beautician",
  #     "caregiver",
  #     "cheerleader",
  #     "dancer",
  #     "decorator",
  #     "designer",
  #     "dietician",
  #     "florist",
  #     "hairdresser",
  #     "homemaker",
  #     "housekeeper",
  #     "model",
  #     "nanny",
  #     "nurse",
  #     "receptionist",
  #     "stylist",
  #     "typist"
  #   ],
  #   smoothing=3,
  #   title="Roles femeninos (Threshold W2V)",
  #   save_to=(folder_path + "roles_fem_w2v_th" + str(window_size) + ".png"))


  # st.chart_w2v_average_for(["she","he"],[
  #     "assistant",
  #     "cashier",
  #     "clerk",
  #     "doctor",
  #     "editor",
  #     "lawyer",
  #     "poet",
  #     "reporter",
  #     "servant",
  #     "worker"
  #   ],
  #   smoothing=3,
  #   title="Roles neutrales (Promedio W2V)",
  #   save_to=(folder_path + "roles_neu_w2v" + str(window_size) + ".png")
  # )


  # st.chart_w2v_threshold_for(["she","he"],[
  #     "assistant",
  #     "cashier",
  #     "clerk",
  #     "doctor",
  #     "editor",
  #     "lawyer",
  #     "poet",
  #     "reporter",
  #     "servant",
  #     "worker"
  #   ],
  #   smoothing=3,
  #   title="Roles neutrales (Threshold W2V)",
  #   save_to=(folder_path + "roles_neu_w2v_th" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(["educated","education","school","study","studies","educate"],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Educación (PPMI)",
  #   save_to=(folder_path + "gender_educacion_pmi" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(["work","worker","working","works","job","jobs","employee"],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="Asociación con 'worker','job' y verbos alusivos (PPMI)",
  #   save_to=(folder_path + "gender_work_pmi" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(["accountant","accounting","accountants"],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="PPMI de 'accountant'",
  #   save_to=(folder_path + "gender_accountant_pmi" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(["cook","cooking","chef","cooks","chefs"],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="PPMI de 'cook'/'chef'",
  #   save_to=(folder_path + "gender_cook_pmi" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(["lawyer","attorney","lawyers","attorneys"],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="PPMI de 'lawyer'",
  #   save_to=(folder_path + "gender_lawyer_pmi" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(["secretary","secretaries","secretarial"],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="PPMI de 'secretary'",
  #   save_to=(folder_path + "gender_secretary_pmi" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(["engineer","engineers","engineering"],
  #   [["she","her","hers"],["him","his","he"]],
  #   smoothing=3,
  #   title="PPMI de 'engineer'",
  #   save_to=(folder_path + "gender_engineer_pmi" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "accountant",
  #   [["she","her","hers"],["he","him","his"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contexts de 'accountant'",
  #   save_to=(folder_path + "gender_accountant_w2v_th" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "cook",
  #   [["she","her","hers"],["he","him","his"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'cook'/'chef'",
  #   save_to=(folder_path + "gender_cook_w2v_th" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "lawyer",
  #   [["she","her","hers"],["he","him","his"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'lawyer'",
  #   save_to=(folder_path + "gender_lawyer_w2v_th" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "secretary",
  #   [["she","her","hers"],["he","him","his"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'secretary'",
  #   save_to=(folder_path + "gender_secretary_w2v_th" + str(window_size) + ".png")
  # )

  # st.chart_w2v_threshold_for(
  #   "engineer",
  #   [["she","her","hers"],["he","him","his"]],
  #   smoothing=3,
  #   title="Threshold W2V de los contextos de 'engineer'",
  #   save_to=(folder_path + "gender_engineer_w2v_th" + str(window_size) + ".png")
  # )



  # st.chart_pmi_for(
  #   ["kitchen","cook","serve","dinner"],
  #   [["she","her","hers"],["him","his","he"]],
  #   title="PPMI de 'kitchen,'cook','serve','dinner'",
  #   save_to=(folder_path + str(window_size) + "_kitchen_cook_serve_dinner.png")
  # )




  ## Homosexualidad estereotípica y dañina


  # st.chart_pmi_for(
  #   ["gay","homosexual","lesbian","gays","homosexuals","lesbians"],
  #   [["sad","sadness","tragic","tragedy"],["happy","joy","happiness"]],
  #   title="PPMI de 'gay' (Tono narrativo)",
  #   smoothing=3,
  #   save_to=(folder_path + "gay_tragedy_pmi" + str(window_size) + ".png")
  # )

  # st.chart_pmi_for(
  #   ["tragic","tragedy","death","suicide"],
  #   [["man","men"],["woman","women"],["gay","homosexual","lesbian","gays","homosexuals","lesbians"]],
  #   title="PPMI de 'tragedy'",
  #   smoothing=3,
  #   save_to=(folder_path + "gay_tragedy2_pmi" + str(window_size) + ".png")
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
