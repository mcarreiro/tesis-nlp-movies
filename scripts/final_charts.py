import sys
import os
sys.path.append('..')
from repo.statistician import Statistician

folder_path = "../final_charts/"
if not os.path.exists(folder_path):
  os.makedirs(folder_path)

freq_st = Statistician()
# freq_st.chart_frequency_for(
#   [["she", "her", "hers", "herself"],["he", "him", "his", "himself"],["woman"],["man"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_pronouns.png")
# )

# res = {}
# fem = freq_st.word_frequency_for(["she","her","hers", "herself"])
# masc = freq_st.word_frequency_for(["he","him","his", "himself"])
# for y in range(1930,2016):
#   res[y] = masc[y] / fem[y]
# for_chart = freq_st.format_for_chart(res)
# for_chart = freq_st.smoothed(for_chart,3)
# freq_st.chart([for_chart],
#   ["Frecuencia H / frecuencia M"],
#   title="Proporción de pronombres femeninos y masculinos",
#   save_to=folder_path + "freq_pronoun_comparison.png",
#   vertical_markers=[1945,1968],
#   axes=["Año", "Fracción H/M"])


st = Statistician(10)
window_size = 10

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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Palabras asociadas a femeneidad en 1974 (PPMI)",
#   highlights=[1945,1968],
#   save_to=(folder_path + "gender_bsri_fem_pmi_" + str(window_size) + ".png")
# )

# ### ANEXO
# for size in [3,5,10,20]:
#   new_st = Statistician(size)
#   new_st.chart_pmi_for(
#     [
#       "yielding",
#       "cheerful",
#       "shy",
#       "affectionate",
#       "flatterable",
#       "loyal",
#       #"feminine",
#       "sympathetic",
#       "sensitive",
#       "understanding",
#       "compassionate",
#       # "eager to soothe hurt feelings",
#       "soft",
#       "warm",
#       "tender",
#       "gullible",
#       "childlike",
#       "sweet", # does not use harsh language
#       "loving",
#       "gentle"
#     ],
#     [["she","her","hers","herself"],["him","his","he","himself"]],
#     smoothing=3,
#     title="Palabras asociadas a femeneidad (PPMI). Ventana " + str(size) + " segundos",
#     save_to=(folder_path + "a_gender_bsri_fem_pmi_" + str(size) + ".png")
#   )


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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Palabras asociadas a masculinidad en 1974 (PPMI)",
#   save_to=(folder_path + "gender_bsri_masc_pmi_" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   title="Palabras asociadas a masculinidad en 1974 (Robustez de asociación)",
#   save_to=(folder_path + "gnder_bsri_masc_hg_0sm_" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Palabras asociadas a masculinidad en 1974 (Robustez de asociación)",
#   save_to=(folder_path + "gender_bsri_masc_hg_" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Palabras neutrales en 1974 (PPMI)",
#   save_to=(folder_path + "gender_bsri_neu_pmi_" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Roles femeninos (PPMI)",
#   save_to=(folder_path + "gender_roles_fem_pmi_" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Roles femeninos (Robustez de asociación)",
#   save_to=(folder_path + "gender_roles_fem_hg_" + str(window_size) + ".png")
# )


# st.chart_w2v_threshold_for(["she","he"],[
#   "architect",
#   "carpenter",
#   "coach",
#   "contractor",
#   "detective",
#   "electrician",
#   "engineer",
#   "farmer",
#   "firefighter",
#   "gambler",
#   "inventor",
#   "machinist",
#   "mechanic",
#   "officer",
#   "physicist",
#   "pilot",
#   "programmer",
#   "rancher",
#   "sheriff",
#   "soldier"
# ],
# smoothing=3,
# title="Roles masculinos (Threshold W2V)",
# save_to=(folder_path + "gender_roles_masc_w2v" + str(window_size) + ".png"))

# st.chart_w2v_threshold_for(["she","he"],[
#   "beautician",
#   "caregiver",
#   "cheerleader",
#   "dancer",
#   "decorator",
#   "designer",
#   "dietician",
#   "florist",
#   "hairdresser",
#   "homemaker",
#   "housekeeper",
#   "model",
#   "nanny",
#   "nurse",
#   "receptionist",
#   "stylist",
#   "typist"
# ],
# smoothing=3,
# title="Roles femeninos (Threshold W2V)",
# save_to=(folder_path + "gender_roles_fem_w2v" + str(window_size) + ".png"))

# st.chart_w2v_threshold_for(["she","he"],[
#   "assistant",
#   "cashier",
#   "clerk",
#   "doctor",
#   "editor",
#   "lawyer",
#   "poet",
#   "reporter",
#   "servant",
#   "worker"
# ],
# smoothing=3,
# title="Roles neutrales (Threshold W2V)",
# save_to=(folder_path + "gender_roles_neu_w2v" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Roles masculinos (PPMI)",
#   save_to=(folder_path + "gender_roles_masc_pmi_" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   title="Roles masculinos (Robustez de asociación)",
#   save_to=(folder_path + "gender_roles_masc_hg_" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Roles neutrales (PPMI)",
#   save_to=(folder_path + "gender_roles_neu_pmi" + str(window_size) + ".png")
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
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Roles neutrales (Robustez de asociación)",
#   save_to=(folder_path + "gender_roles_neu_hg" + str(window_size) + ".png")
# )

# st.chart_pmi_for(["engineer","engineers","engineering"],
#   [["she","her","hers", "herself"],["him","his","he", "himself"]],
#   smoothing=3,
#   title="PPMI de 'engineer', 'engineers' y 'engineering'",
#   save_to=(folder_path + "gender_engineer_pmi" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   "engineers",
#   [["she","her","hers", "herself"],["him","his","he", "himself"]],
#   smoothing=3,
#   title="Threshold W2V de 'engineers'",
#   save_to=(folder_path + "gender_engineer_w2v_th" + str(window_size) + ".png")
# )

# st.chart_pmi_for(["accountant","accounting","accountants"],
#   [["she","her","hers", "herself"],["him","his","he", "himself"]],
#   smoothing=3,
#   title="PPMI de 'accountant', 'accountants' y 'accounting'",
#   save_to=(folder_path + "gender_accountant_pmi" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   "accountants",
#   [["she","her","hers", "herself"],["him","his","he", "himself"]],
#   smoothing=3,
#   title="Threshold W2V de 'accountants'",
#   save_to=(folder_path + "gender_accountant_w2v_th" + str(window_size) + ".png")
# )

# st.chart_pmi_for(["chef","chefs"],
#   [["she","her","hers", "herself"],["him","his","he", "himself"]],
#   smoothing=3,
#   title="PPMI de 'chef' y 'chefs'",
#   save_to=(folder_path + "gender_chef_pmi" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   "chef",
#   [["she","her","hers", "herself"],["him","his","he", "himself"]],
#   smoothing=3,
#   title="Threshold W2V 'chef'",
#   save_to=(folder_path + "gender_chef_w2v_th" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   "cook",
#   [["she","her","hers", "herself"],["him","his","he", "himself"]],
#   smoothing=3,
#   title="Threshold W2V de 'cooks'",
#   save_to=(folder_path + "gender_cook_w2v_th" + str(window_size) + ".png")
# )

# st.chart_pmi_for(["cook","cooks","cooking"],
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="PPMI de 'cook', 'cooks' y 'cooking'",
#   save_to=(folder_path + "gender_cook_pmi" + str(window_size) + ".png")
# )

# st.chart_pmi_for(["nurse","nurses"],
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="PPMI de 'nurse' y 'nurses'",
#   save_to=(folder_path + "gender_nurse_pmi" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   "nurse",
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Threshold W2V de 'nurse'",
#   save_to=(folder_path + "gender_nurse_w2v_th" + str(window_size) + ".png")
# )

# st.chart_pmi_for(["realtor","realestate","realtors"],
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="PPMI de 'realtor', 'real estate' y 'realtors'",
#   save_to=(folder_path + "gender_realtor_pmi" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   "realtor",
#   [["she","her","hers","herself"],["him","his","he","himself"]],
#   smoothing=3,
#   title="Threshold W2V de 'realtor'",
#   save_to=(folder_path + "gender_realtor_w2v_th" + str(window_size) + ".png")
# )

#############################################
# Terrorism ##


# freq_st.chart_frequency_for(
#   [["iraq", "iraqis", "iraqi"],["afghan", "afghans","afghanistan"],["palestine","palestinian"],["arab","arabs"],["terrorism","terrorist","terrorists"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "terror_freq_paises_sm3.png")
# )

# freq_st.chart_frequency_for(
#   [["iraq", "iraqis", "iraqi"],["afghan", "afghans","afghanistan"],["palestine","palestinian"],["arab","arabs"],["terrorism","terrorist","terrorists"]],
#   title="Frecuencia por año",
#   save_to=(folder_path + "terror_freq_paises_sm0.png")
# )

# st.chart_pmi_for(
#   ["terrorism","terrorist","terrorists"],
#   [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestine","palestinian","palestinians"],["afghan", "afghans", "afghanstan"],["pakistan","pakistani","pakistanis"]],
#   smoothing=3,
#   title="PPMI de 'terrorist','terrorists' y 'terrorism' (Nacionalidad)",
#   save_to=(folder_path + "terrorism_nationality_pmi_" + str(window_size) + ".png")
# )

# st.chart_hypergeo_for(
#   ["terrorism","terrorist","terrorists"],
#   [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestine","palestinian","palestinians"],["afghan", "afghans", "afghanstan"],["pakistan","pakistani","pakistanis"]],
#   title="Robustez de asociación de 'terrorist','terrorists' y 'terrorism' (Nacionalidad)",
#   save_to=(folder_path + "terrorism_nationality_hg_" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   "terrorist",
#   [["iraq", "iraqis", "iraqi"],["italian","italy","italians"],["arab","arabs"],["palestine","palestinian","palestinians"],["afghan", "afghans", "afghanstan"],["pakistan","pakistani","pakistanis"]],
#   smoothing=3,
#   title="Threshold W2V de los contextos de las nacionalidades vs. 'terrorist' (Nacionalidad)",
#   save_to=(folder_path + "terrorism_nationality2_w2v_th_" + str(window_size) + ".png")
# )

# st.chart_pmi_for(
#   ["terrorism","terrorist","terrorists"],
#   [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
#   smoothing=3,
#   title="PPMI de 'terrorist','terrorists' y 'terrorism' (Religión)",
#   save_to=(folder_path + "terorrism_religion_pmi_" + str(window_size) + ".png")
# )

# st.chart_hypergeo_for(
#   ["terrorism","terrorist","terrorists"],
#   [["islam", "muslim", "muslims"],["christian","christians","christianity"],["jew","judaism","jews"]],
#   title="Robustez de asociación de 'terrorist','terrorists' y 'terrorism' (Religión)",
#   save_to=(folder_path + "terorrism_religion_hg" + str(window_size) + ".png")
# )

# st.chart_w2v_average_for(
#   ["muslim","christian","jew"],
#   ["terrorist","terrorists","terrorism"],
#   smoothing=3,
#   title="Promedio W2V de los contextos de 'terrorist' (Religión)",
#   save_to=(folder_path + "terorrism_religion_w2v_" + str(window_size) + ".png")
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
#   title="Threshold W2V de los contextos de 'muslim' (Deshumanización)",
#   save_to=(folder_path + "terorrism_muslim_dehumanization2_w2v_th_" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   ["rat","hunt","cage","nest","arrest","prison","hideout"],
#   ["terrorist","terrorism","terrorists"],
#   smoothing=3,
#   title="Threshold W2V de los contextos de 'terrorist' (Deshumanización)",
#   save_to=(folder_path + "terorrism_dehumanization2_w2v_th_" + str(window_size) + ".png")
# )

# # ANEXO
# st.chart_pmi_for(
#   ["muslim","islam","muslims"],
#   [["rat","rats"],["hunt","hunted","hunting"],["cage","caged","cages"],["nest","nesting"],["arrest","arrested","arrests"],["prison","prisons","prisoner","prisoners"],["hideout","refuge","shelter"]],
#   smoothing=3,
#   title="PPMI de 'terrorist','terrorists' y 'terrorism' (Deshumanización)",
#   save_to=(folder_path + "terorrism_deshumanization_" + str(window_size) + ".png")
# )

# # ANEXO
# st.chart_pmi_for(
#   ["terrorism","terrorist","terrorists"],
#   [["rat","rats"],["hunt","hunted","hunting"],["cage","caged","cages"],["nest","nesting"],["arrest","arrested","arrests"],["prison","prisons","prisoner","prisoners"],["hideout","refuge","shelter"]],
#   smoothing=3,
#   title="PPMI de 'muslim', 'muslims' e 'islam' (Deshumanización)",
#   save_to=(folder_path + "terorrism_muslim_deshumanization2_" + str(window_size) + ".png")
# )

# st.chart_pmi_for(
#   ["terrorist","terrorism","terrorists"],
#   [["gun","machinegun","pistol","shoot","shooting","shooter"],["bomb","bombing","bomber","explosive","explosion"],["fire","burn","arson","arsonist"]],
#   smoothing=3,
#   title="PPMI de 'terrorist', 'terrorism' y 'terrorists'",
#   save_to=(folder_path + "terrorism_weapons_pmi_" + str(window_size) + ".png")
# )

# st.chart_hypergeo_for(
#   ["terrorist","terrorism","terrorists"],
#   [["gun","machinegun","pistol","shoot","shooting","shooter"],["bomb","bombing","bomber","explosive","explosion"],["fire","burn","arson","arsonist"]],
#   title="Robustez de asociación de 'terrorist','terrorists' y 'terrorism' (Armas)",
#   save_to=(folder_path + "terrorism_weapons_hg_" + str(window_size) + ".png")
# )



#############################################
# Russia ##

# freq_st.chart_frequency_for(
#   [["russia", "russian", "russians"],["communist", "communism", "communists","commie","commies"],["mob","mobster","gangster","mafia","gangsters"]],
#   smoothing=3,
#   title="Frecuencia por año",
#   save_to=(folder_path + "freq_russia.png")
# )

# st.chart_pmi_for(
#   ["russia","russian","russians"],
#   [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["poor","poverty","hunger"],["bride","brides","mailorder"]],
#   smoothing=3,
#   title="PPMI de 'russia','russian' y 'russians'",
#   save_to=(folder_path + "russia_associations_pmi" + str(window_size) + ".png")
# )


# st.chart_hypergeo_for(
#   ["russia","russian","russians"],
#   [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["poor","poverty","hunger"],["bride","brides","mailorder"]],
#   title="Robustez de asociación para 'russia'",
#   save_to=(folder_path + "russia_associations_hg_" + str(window_size) + ".png"),
#   smoothing=3
# )

# st.chart_w2v_threshold_for(
#   "russian",
#   [["communist","communism","communists","commies","commie"],["mob","mobster","gangster","mafia","gangsters"],["poor","poverty","hunger"],["bride","brides","mailorder"]],
#   smoothing=3,
#   title="Threshold W2V de los contextos de estereotipos vs. 'russia'",
#   save_to=(folder_path + "russia_associations2_w2v_th_" + str(window_size) + ".png")
# )

# st.chart_w2v_threshold_for(
#   ["communist","gangster","poor","bride"],
#   ["russian","russians","russia"],
#   smoothing=3,
#   title="Threshold W2V de los contextos de 'russia' (Estereotipos)",
#   save_to=(folder_path + "russia_associations_w2v_th_" + str(window_size) + ".png")
# )

# st.chart_pmi_for(
#   ["communist","communism","communists","commies","commie"],
#   [["russia","russian","russians"],["italy","italian","italians"],["france","french"],["china","chinese"]],
#   smoothing=3,
#   title="PPMI de 'communist'",
#   save_to=(folder_path + "russia_countries_communism_pmi" + str(window_size) + ".png")
# )

# st.chart_pmi_for(
#   ["mob","mobster","gangster","mafia","gangsters"],
#   [["russia","russian","russians"],["italy","italian","italians"],["france","french"],["china","chinese"]],
#   smoothing=3,
#   title="PPMI de 'gangster'",
#   save_to=(folder_path + "russia_countries_mob_pmi" + str(window_size) + ".png")
# )

# freq_st.chart_frequency_for(
#   [["stroganoff"],["caviar"],["kasha"],["kissel"],["knish"],["pirozhki"],["sorrel"],["orlov"]],
#   smoothing=3,
#   title="Frecuencia por año de comida rusa",
#   save_to=(folder_path + "russian_food.png")
# )
# [Beef Stroganoff,/Bliny,Caviar,Chicken Kiev,Coulibiac,Dressed herring,Golubtsy,Guriev porridge,Kasha,Kissel,Knish,Kholodets,Kulich,Medovukha,Mimosa salad,Oladyi,Olivier salad,Paskha,Pelmeni,Pirog,Pirozhki,Pozharsky cutlet,Rassolnik,Sbiten,Shchi,Solyanka,Sorrel soup,Syrniki,Ukha,Vatrushka,Veal Orlov,Vinegret,Zakuski]
# ["stroganoff",/"bliny","caviar","kiev",/"coulibiac",/"golubtsy",/"guriev","kasha","kissel","knish",/"kholodets",/"kulich",/"kedovukha",/"oladyi",/"paskha",/"pelmeni",/"pirog","pirozhki","pozharsky",/"rassolnik",/"sbiten",/"shchi",/"solyanka","sorrel",/"syrniki",/"ukha",/"vatrushka","orlov",/'vinegret',/"zakuski"]

# freq_st.chart_frequency_for(
#   [["comrade"],["glasnost"],["gulag"],["intelligentsia"],["perestroika"],["politburo"],["tzar","tsar"],["commissar"],["apparatchik"],["agitprop"]],
#   smoothing=3,
#   title="Frecuencia por año de vocabulario de la Rusia Soviética",
#   save_to=(folder_path + "russian_vocab.png")
# )

# st.chart_pmi_for(
#   ["russia","russian","russians"],
#   [["communist","communism","communists","commies","commie"],["comrade","glasnost","gulag","intelligentsia","perestroika","politburo","tzar","tsar","commissar","apparatchik","agitprop"],["stroganoff","caviar","kasha","kissel","knish","pirozhki","sorrel","orlov"]],
#   smoothing=3,
#   title="PPMI de vocabulario cultural ruso",
#   save_to=(folder_path + "russia_culture_" + str(window_size) + ".png")
# )

# st.chart_pmi_for(
#   ["russia","russian","russians"],
#   [["communist","communism","communists","commies","commie"],["glasnost","gulag","intelligentsia","perestroika","politburo","tzar","tsar","commissar","apparatchik","agitprop"],["stroganoff","kasha","kissel","knish","pirozhki","sorrel","orlov"]],
#   smoothing=3,
#   title="PPMI de vocabulario cultural ruso (sin 'comrade' ni 'caviar')",
#   save_to=(folder_path + "russia_culture_ex_" + str(window_size) + ".png")
# )
