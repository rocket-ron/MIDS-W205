
'''

			g1		g2		g3		g4		g5		g6		g7		r1		r2		b1		y1
g1			0		0		0		0		0		0		0		0		0		1 		1
g2			0		0		0		0		0		0		0		0		0		1 		1
g3			0		0		0		0		0		0		0		0		0		1       1
g4			0		0		0		0		0		0		0		0		0		1 		0
g5			0		0		0		0		0		0		0		0		0		1 		0
g6			0		0		0		0		0		0		0		0		0		1 		1
g7			0		0		0		0		0		0		0		0		0		0		0
r1			0		0		0		0		0		0		1 		0		0		0		1
r2			0		0		0		0		0		0		0		0		0		0		1 
b1			0		0		0		0		0		1 		0		1 		0		0		1
y1			0		0		0		0		0		0		0		0		1 		0		0

sum			0		0		0		0		0		1 		1 		1 		1 		6		7

			g1		g2		g3		g4		g5		g6		g7		r1		r2		b1		y1
g1			0		0		0		0		0		0		0		0		0		1/6 	1/7
g2			0		0		0		0		0		0		0		0		0		1/6 	1/7
g3			0		0		0		0		0		0		0		0		0		1/6     1/7
g4			0		0		0		0		0		0		0		0		0		1/6 	0
g5			0		0		0		0		0		0		0		0		0		1/6 	0
g6			0		0		0		0		0		0		0		0		0		1/6 	1/7
g7			0		0		0		0		0		0		0		0		0		0		0
r1			0		0		0		0		0		0		1 		0		0		0		1/7
r2			0		0		0		0		0		0		0		0		0		0		1/7 
b1			0		0		0		0		0		1 		0		1 		0		0		1/7
y1			0		0		0		0		0		0		0		0		1 		0		0

'''

import numpy as np
nodes = 11 
M_link = np.zeros((nodes, nodes)) 

M_link[0,9] 	= 1
M_link[0,10]	= 1

M_link[1,9]		= 1
M_link[1,10]	= 1

M_link[2,9]		= 1
M_link[2,10]	= 1

M_link[3,9]		= 1
M_link[4,9]		= 1

M_link[5,9]		= 1
M_link[5,10]	= 1

M_link[7,6]		= 1
M_link[7,10]	= 1

M_link[8,10]	= 1

M_link[9,5]		= 1
M_link[9,7]		= 1
M_link[9,10]	= 1

M_link[10,8]	= 1

print(M_link)


# Next we need to create the adjacency matrix by dividing each column by its sum:

M_adj = np.empty((nodes, nodes))
for j in range(nodes):
	if M_link[:,j].sum() > 0:
		M_adj[:,j] = M_link[:,j] / M_link[:,j].sum()
	else:
		M_adj[:,j] = 0
np.set_printoptions(precision=4)
print(M_adj)

# Finally we need to apply the `pagerank` function, which will apply page transitions iteratively to a randomly initialized distribution over the pages, until convergence.
def pagerank(M_adj, d=0.85, square_error=1e-5):

	nodes = M_adj.shape[0] 

	V_pr = np.random.rand(nodes)

	v_pr = V_pr / V_pr.sum() 
	last_v = np.ones((nodes)) 
	M_hat = d * M_adj + (1-d)/nodes * np.ones((nodes, nodes)) 
	while np.square( v_pr - last_v).sum() > square_error:
		last_v =  v_pr
		v_pr= M_hat.dot(v_pr) 
	return v_pr

print pagerank(M_adj)
