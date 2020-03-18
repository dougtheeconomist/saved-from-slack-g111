weights = []
students = ["Darrel", "Nick", "Charlie", "Doug", "Devin", "Emily", "Jessica", "Karen", "Ngoc"]

import sys
import random

if len(weights) != len(students):
    weights = [1 for student in students]

result = random.choices(range(len(students)), weights)[0]

print(students[result])

n = len(weights)
adj = 0.1/n
new_total = n*adj + sum(weights)
weights = [(w+adj)/new_total for w in weights]
weights[result] = 0

with open(sys.argv[0], 'r') as filehandle:
    lines = filehandle.readlines()

lines[0] = f'weights = {str(weights)}\n'

with open(sys.argv[0], 'w') as filehandle:
    filehandle.writelines(lines)