import numpy as np
import time
import sys
sys.path.append('./players')

import playerConfig
import MyPlayer as player1dist
import PlayerGood as player2dist

class Game():
 def __init__(self, player1, player2,total1=0,total2=0):
  self.player_positions=[0]*2
  self.players=[0]*2
  self.totals=[0]*2
  self.known_player_positions=[0]*2
  for i in range(2):
   self.player_positions[i]=np.random.randint(0,playerConfig.MAX_STATE,playerConfig.DIMENSION)
   self.known_player_positions[i]=np.array([playerConfig.MAX_STATE]*playerConfig.DIMENSION)
  self.players[0]=player1
  self.players[1]=player2
  self.totals[0]=total1
  self.totals[1]=total2
  self.step=0
  return

 def GenKnownPositions(self,actual_positions=[],previous_positions=[],step=0):
  new_positions=actual_positions.copy()
  if playerConfig.MAX_STATE//2-step>0:
   new_positions+=np.random.randint(0,playerConfig.MAX_STATE//2-step,actual_positions.shape[0])
  pp=previous_positions[new_positions>previous_positions].copy()
  new_positions[new_positions>previous_positions]=pp
  return new_positions

 def GetScore(self,pos1,pos2):
  s=(np.array(pos1-pos2)*playerConfig.Weights).sum()+(np.random.rand()-0.5)
  if s>0:
   return 0
  else:
   return 1


 def Step(self,person=0):
  steps=[0]*2
  for i in range(2):
   self.known_player_positions[i]=self.GenKnownPositions(actual_positions=self.player_positions[i],
                                previous_positions=self.known_player_positions[i],
                                step=self.step)
  i=person

  steps[i]=self.players[i].Step(step=self.step,
                                 own_state=self.player_positions[i],
                                 known_state_opponent=self.known_player_positions[(i+1)%2])
  self.step+=1
  if steps[i]==playerConfig.PASS:
    self.totals[i]-=playerConfig.Prices[playerConfig.PASS]
    self.totals[(i+1)%2]+=playerConfig.Prices[playerConfig.PASS]
    return playerConfig.PASS

  if steps[i]==playerConfig.ACT:
     score=self.GetScore(self.player_positions[0],self.player_positions[1])
     if score==i:
      self.totals[i]+=playerConfig.Prices[playerConfig.ACT]
      self.totals[(i+1)%2]-=playerConfig.Prices[playerConfig.ACT]
     if score==(i+1)%2:
      self.totals[i]-=playerConfig.Prices[playerConfig.ACT]
      self.totals[(i+1)%2]+=playerConfig.Prices[playerConfig.ACT]
     return playerConfig.ACT

  if steps[i]==playerConfig.LOOK:
    self.totals[i]-=playerConfig.Prices[playerConfig.LOOK]
    self.totals[(i+1)%2]+=playerConfig.Prices[playerConfig.LOOK]
    return playerConfig.LOOK




total1=0
total2=0

ITTS=10000
for itt in range(ITTS):
# print("Game",itt)
 for person in range(2):
  player1=player1dist.Player()
  player2=player2dist.Player()
  game=Game(player1,player2,total1,total2)
#  print('actual:',game.player_positions)

  cycle=0
  person_act=person
  while True and cycle<10:
#   s=time.time()
   result=game.Step(person=person_act)
#   print('person:',person_act,'result:',result)
#   print(np.array(game.totals)/itt)
#   print(person_act,'result:',playerConfig.Actions[result],'time ',time.time()-s)
#   print(person_act,'result:',playerConfig.Actions[result])
   if result==playerConfig.ACT or result==playerConfig.PASS:
    break
   cycle+=1
   person_act+=1
   person_act%=2

  total1=game.totals[0]
  total2=game.totals[1]

print(np.array(game.totals)/ITTS)
