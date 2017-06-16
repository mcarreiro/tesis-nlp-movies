import sys
sys.path.append('..')
from repo.cooccurrence_matrix import CooccurrenceMatrix

if len(sys.argv) > 1:
  CooccurrenceMatrix.build_all(sys.argv[1])
else:
  CooccurrenceMatrix.build_all()
