import numpy as np

k = int(input())
matrix = []

for i in range(k):
  row_str = input()
  str_list = row_str.split()
  int_list = [int(num) for num in str_list]
  matrix.append(int_list)

