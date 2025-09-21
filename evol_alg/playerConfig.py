import numpy as np

DIMENSION=4
MAX_STATE=10

PASS=0
ACT=1
LOOK=2

Actions=[0]*3
Actions[ACT]='Act'
Actions[PASS]='Pass'
Actions[LOOK]='Look'

Prices=[0]*3
Prices[ACT]=10
Prices[PASS]=3
Prices[LOOK]=1

Weights=np.array([3,2,4,1])
