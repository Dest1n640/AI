import numpy as np
import playerConfig


class Player():
 def __init__(self):
  return

 def Step(self,step=0,own_state=[],known_state_opponent=[]):
  score=((np.array(own_state)-np.array(known_state_opponent))*playerConfig.Weights).sum()
  if score>0:
   return playerConfig.ACT
  if score<0:
   return playerConfig.PASS
  return playerConfig.LOOK

