import sys
sys.path.append('..')
from repo import config as CONFIG
import matplotlib.pyplot as plt
import pickle
import math

with open(CONFIG.wordsim_path + "combined_with_w2v.p", 'rb') as f:
  word_list = pickle.load(f, encoding='latin-1')

# Select those above the arbitrary cut made by looking at the word list
above_cut = [pair for pair in word_list if float(pair["human_dist"]) >= 5.5]
above_cut = sorted(above_cut, key=lambda pair: pair["w2v_dist"])
# Keep the 90% with highest w2v distance score
cut = len(above_cut) - math.floor(0.8*len(above_cut))
above_cut = above_cut[:cut]
last = above_cut[len(above_cut) - 1]["w2v_dist"]
print("Cut point: " + str(last))

def set_color(human, w2v):
  if human < 5.5:
    return 'b'
  else:
    if w2v >= last:
      return 'r'
    else:
      return 'g'

x = [pair["human_dist"] for pair in word_list]
y = [pair["w2v_dist"] for pair in word_list]
c = [set_color(float(pair["human_dist"]), float(pair["w2v_dist"])) for pair in word_list]

plt.scatter(x, y, c=c)
plt.title("Cut point: " + str(last))
plt.show()
