import numpy as np
import set_bits
def independent_vectors(A,v):
    """
    A is a matrix of row vectors to test for
    independence. v is a selection of row vectors
    of length number of rows of A. v is a bit
    string of 1 if row included and 0 if not included.

    Eg,

>>> xh = np.array([1,2,3])
>>> yh = np.array([3,1,0])
>>> zh = np.array([1,0,0])
>>> A = np.array([
	[xh[0],yh[0],zh[0]],
	[xh[1],yh[1],zh[1]],
	[xh[2],yh[2],zh[2]]])
>>> v = [1,1,1]
>>> print independent_vectors(A,v)
True
    """
    independent = False
    minor = set_bits.MinorRow(A.T,v)
    for j in range(2**minor.shape[0]):
	w = set_bits.Base(j,2,minor.shape[0])
	if set_bits.Cardinality(w) == minor.shape[1]:
		minor2 = set_bits.MinorCol(minor,w)
		if np.linalg.det(minor2) <> 0:
			independent = True
			break
    if set_bits.Cardinality(v) == 0:
	independent = True
    return independent
