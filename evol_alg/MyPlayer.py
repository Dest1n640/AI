import numpy as np
import random
import playerConfig

POPULATION_SIZE = 200
GENOME_LENGTH = 8
MUTATION_RATE = 0.05
TOURNAMENT_SIZE = 5
NUM_GENERATIONS = 100

def create_dna():
    dna = []
    for _ in range(4):
        pass_threshold = random.randint(0, 10)
        act_threshold = random.randint(pass_threshold, 10)
        dna.extend([act_threshold, pass_threshold])
    return dna
  
def selection(animals_with_winnings):
  contenders = random.sample(animals_with_winnings, TOURNAMENT_SIZE)
  
  contenders.sort(key = lambda item: item[1], reverse=True)
  
  return contenders[0][0]

def crossover(parent1_dna, parent2_dna):
  split_point = random.randint(1, GENOME_LENGTH - 1)
  child_dna = parent1_dna[:split_point] + parent2_dna[split_point:]
  
  return child_dna

def mutate(player_dna):
  mutated_dna = []
  random_gen = random.randint(0, 8)
  for i, gene in enumerate(player_dna):
    if random.random() < MUTATION_RATE:
      mutated_dna.append(random.randint(0, 9))
    else:
      mutated_dna.append(gene)
  return mutated_dna



class Player():
    def __init__(self):
      self.champion_dna = [8, 1, 6, 0, 7, 3, 7, 3]
    
    def _make_decision(self, round_index, card_value):
      act_threshold_index = round_index * 2
      pass_threshold_index = round_index * 2 + 1
      
      act_threshold = self.champion_dna[act_threshold_index]
      pass_threshold = self.champion_dna[pass_threshold_index]
      
      if card_value >= act_threshold:
        return playerConfig.ACT
      elif card_value <= pass_threshold:
        return playerConfig.PASS
      else:
        return playerConfig.LOOK

    def Step(self, step=0, own_state=[], known_state_opponent=[]):
      score = ((np.array(own_state) - np.array(known_state_opponent)) * playerConfig.Weights).sum()
      my_card_for_this_round = own_state[step]
      decision = self._make_decision(step, my_card_for_this_round)
      return decision
      

class TrainingPlayer:
  def __init__(self, dna):
    self.dna = dna 
  
  def make_decision(self, round_index, card_value):
    act_threshold_index = round_index * 2
    pass_threshold_index = round_index * 2 + 1
      
    act_threshold = self.dna[act_threshold_index]
    pass_threshold = self.dna[pass_threshold_index]
    
    if card_value > act_threshold:
      return playerConfig.ACT
    elif card_value < pass_threshold:
      return playerConfig.PASS
    else:
      return playerConfig.LOOK

def simulate_one_game(player1, player2):
  p1, p2 = TrainingPlayer(player1), TrainingPlayer(player2)
  
  p1_cards = sorted(random.sample(range(10), 4), reverse=True)
  p2_cards = sorted(random.sample(range(10), 4), reverse=True)
  
  for i in range(4):
    decision1 = p1.make_decision(i, p1_cards[i])
    decision2 = p2.make_decision(i, p2_cards[i])
    
    if decision1 == playerConfig.PASS:
      return -playerConfig.Prices[playerConfig.PASS]
    if decision2 == playerConfig.PASS:
      return playerConfig.Prices[playerConfig.PASS]

    if decision1 == playerConfig.ACT or decision2 == playerConfig.ACT:
      score1 = p1_cards[i] * playerConfig.Weights[i]
      score2 = p2_cards[i] * playerConfig.Weights[i]
      if score1 > score2:
        return playerConfig.Prices[playerConfig.ACT]
      if score1 < score2:
        return -playerConfig.Prices[playerConfig.ACT]
      return 0
  return 0
          
def calculate_fitness(candidate_dna, opponents):
  total_score = 0
  for opponents_dna in opponents:
    for _ in range(10):
      total_score += simulate_one_game(candidate_dna, opponents_dna)  
      total_score -= simulate_one_game(opponents_dna, candidate_dna)
  return total_score / (len(opponents) * 20)
    

print("--- НАЧАЛО ТРЕНИРОВКИ: Поиск лучшей стратегии ---")

# Создаем стартовую популяцию
population = [create_dna() for _ in range(POPULATION_SIZE)]

# Эталонные стратегии для оценки
opponents = [create_dna() for _ in range(10)] # Набор случайных для разнообразия
opponents.append([6, 2, 6, 2, 6, 2, 6, 2]) # Агрессивный
opponents.append([9, 5, 9, 5, 9, 5, 9, 5]) # Осторожный

best_dna_overall = []
best_fitness_overall = -float('inf')

for generation in range(NUM_GENERATIONS):
    # Оцениваем приспособленность ("забег")
    population_with_scores = [
        (dna, calculate_fitness(dna, opponents)) for dna in population
    ]
    
    # Находим лучшего в этом поколении
    best_in_gen_dna, best_in_gen_fitness = max(population_with_scores, key=lambda item: item[1])
    if best_in_gen_fitness > best_fitness_overall:
        best_fitness_overall = best_in_gen_fitness
        best_dna_overall = best_in_gen_dna
    
    print(f"Поколение {generation+1:3}/{NUM_GENERATIONS} | Лучший счет: {best_fitness_overall:6.2f} | ДНК: {best_dna_overall}")

    # Создаем следующее поколение
    next_generation = [best_dna_overall] # Элитизм: лучший всегда выживает
    for _ in range(POPULATION_SIZE - 1):
        parent1 = selection(population_with_scores)
        parent2 = selection(population_with_scores)
        child = crossover(parent1, parent2)
        mutated_child = mutate(child)
        next_generation.append(mutated_child)
    
    population = next_generation

print("\n--- ТРЕНИРОВКА ЗАВЕРШЕНА! ---")
print(f"Найдена лучшая стратегия с ДНК: {best_dna_overall}")
print("СКОПИРУЙТЕ ЭТОТ СПИСОК И ВСТАВЬТЕ ЕГО В ПЕРЕМЕННУЮ 'self.champion_dna' В КЛАССЕ Player ВЫШЕ.")
