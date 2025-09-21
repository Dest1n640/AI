import re 

text = open("text.txt", 'r')
k = 0
pattern = r'(\w+(о|е|и)\s+\w+(ть|ти|л|ла|ло|ли|ешь|ет|ем|ете|ут|ют|ишь|ит|им|ите|ат|ят|у|ю)(ся|сь)?)|(\w+(ть|ти|л|ла|ло|ли|ешь|ет|ем|ете|ут|ют|ишь|ит|им|ите|ат|ят|у|ю)(ся|сь)?\s+\w+(о|е|и))'

for i in text:
  res = re.search(pattern, i)
  if res:
    k+=1
    print(i, end='')
print(k)
