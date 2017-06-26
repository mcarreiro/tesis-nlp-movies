import sys
sys.path.append('..')
from repo.cooccurrence_matrix import CooccurrenceMatrix

if len(sys.argv) > 1:
  print("Building matrices for: ", sys.argv[1], " second windows")
  CooccurrenceMatrix.build_all(sys.argv[1])
else:
  print("Building matrices for: 5 second windows")
  CooccurrenceMatrix.build_all()
