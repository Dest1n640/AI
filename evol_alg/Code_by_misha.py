import numpy as np
import playerConfig


class Player():
 def __init__(self):
  return

 def Step(self,step=0,own_state=[],known_state_opponent=[]):
  own=np.array(own_state,float)
  known=np.array(known_state_opponent,float)
  w=playerConfig.Weights

  # Оставшийся диапазон роста известного состояния соперника
  r=max(0,playerConfig.MAX_STATE//2-step)
  # Смещение ожидания из-за недооценки соперника в known_state_opponent
  # За шаг известные координаты могут увеличиться равномерно в [0, r-1]
  # Ожидаемая прибавка по каждой координате ~ (r-1)/2, взвешиваем суммой весов
  bias=w.sum()*(r-1)/2 if r>0 else 0

  # Оценка детерминированной части s без шума + учёт смещения
  est=((own-known)*w).sum()+bias

  # Шум равномерный в [-0.5,0.5], значит p_win = P(s+U>0) = clip(0.5+est,0,1)
  p_win=min(max(0.5+est,0.0),1.0)

  ev_act=playerConfig.Prices[playerConfig.ACT]*(2*p_win-1)
  ev_pass=-playerConfig.Prices[playerConfig.PASS]

  # Если действовать выгоднее с запасом — атакуем
  if ev_act>ev_pass+0.5:
   return playerConfig.ACT

  # Если действовать сильно хуже PASS — пасуем, особенно когда улучшения ждать неоткуда
  if ev_act<ev_pass-0.5 or r==0:
   return playerConfig.PASS

  # Пограничная зона: подождать ещё один шаг на случай улучшения информации/позиции
  return playerConfig.LOOK
