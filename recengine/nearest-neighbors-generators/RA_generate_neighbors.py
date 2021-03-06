# This program generates for each userid, 5 nearest neighbors, by using collaborative filterting. In particular, the sparse matrix
# of userid/event is generated, then one takes the dot product of this matrix (normalized) with itself. 
# This program should load csv files generated by RASparse_rowcol_generator.py (there are 2 files below since I did this in two stages).

from scipy import sparse
import pandas as pd
from scipy.sparse import coo_matrix
import numpy as np
from sklearn.preprocessing import normalize

# Load in all row/column/id entries which will form our sparse matrix.
df_rowcols1 = pd.read_csv('../RA_row_col_id_urlSept25_2.csv', delim_whitespace=True)
df_rowcols2 = pd.read_csv('../RA_row_col_id_urlSept25_2Part2.csv', delim_whitespace=True)
rowcols = [df_rowcols1,df_rowcols2]
df_rowcols = pd.concat(rowcols, ignore_index=True).drop_duplicates()


# Generate sparse userid/event matrix.
rows = np.array(df_rowcols['row'])
columns = np.array(df_rowcols['column'])
data = [1.0]*len(columns)
X = coo_matrix((data, (rows,columns)), shape=(75988+1,25022+1))

# Normalize all of the columns
X_n = normalize(X, norm='l2', axis=1)

# Take dot product with transpose to generate matrix of user/user similarity.
Y = X_n.dot(X_n.T)

# Output the nearest neighbors (5) for each userid, by taking the top 5 entries from each row in Y.
print 'n1 n2 n3 n4 n5 row'
for i in range(0, 75988+1):
	row_nn = np.squeeze(np.asarray(Y.getrow(i).todense()))
	nnarr = np.argsort(row_nn)[-5:]
	print nnarr[0], nnarr[1], nnarr[2], nnarr[3], nnarr[4], i
