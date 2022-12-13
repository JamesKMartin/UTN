#Task:1 - String Length###
input_string = input("Please enter the string")
length = 0
for x in input_string:
    length = length + 1
print(length)

#Task:2 – Largest List###
import random

number = random.sample(range(1, 100), 10)
print(number)
max = number[0]
for i in range(len(number)):
    if number[i] > max:
        max = number[i]
    else:
        i = i + 1
print(max)

#Task:3 – Character Frequency###

input_string = input("Please enter the string")
string = input_string.replace(' ', '')
count_dist = {}
for i in string:
    if i in count_dist.keys():
        count_dist[i] = count_dist[i] + 1
    else:
        count_dist[i] = 1
print(count_dist)

#Task:4 – Sorted List of Tuples###

res = []
import random

for i in range(0, 10):
    rand = random.sample(range(1, 100), 3)
    res.append((rand[0], rand[1], rand[2]))
# print(res)
sorted_list = sorted(res, key=lambda x: x[2])
print(sorted_list)

#Task:5 – Check Brackets###
input_string = input("Please enter the mathematical expression string")
openbracket = 0
closebracket = 0
for i in input_string:
    if i == '(':
        openbracket = openbracket + 1
    elif i == ')':
        closebracket = closebracket + 1
if openbracket == closebracket:
    print("Correct input")
else:
    print("Incorrect input")

#Task:6 – Check Brackets II###
input_string = input("Please enter the mathematical expression string")
dist = {}
for i in input_string:
    if i in dist.keys():
        dist[i] = dist[i] + 1
    else:
        dist[i] = 1

if ('(' in dist) & (')' in dist) & ('[' in dist) & (']' in dist) & ('{' in dist) & ('}' in dist):
    if (dist['('] == dist[')']) & (dist['['] == dist[']']) & (dist['{'] == dist['}']):
        print("Correct input")
    else:
        print("Incorrect input")
else:
    print("Incorrect input")

#Task:7 – Queue###
queue = []
while True:
    names = input("write names. If you want to stop type next")
    if names != 'next':
        queue.append(names)
        continue
    else:
        for i in range(len(queue)):
            # print(queue[-1])
            print(queue.pop(0))
        break

#Task:8 – Unlimited Power###

def power(x, n):
    if n == 0:
        return 1
    elif n >= 1:
        return x * power(x, n - 1)


# print(power(3,2))

#Task:9 – Unlimited Power II###
def factorial(x):
    if x == 0:
        return 1
    elif x >= 1:
        return x * factorial(x - 1)


def unlimited_power(n):
    value = 0
    if n == 0:
        return 1
    elif n >= 1:
        for i in range(0, n):
            value = value + n ** i / factorial(i)
        return value


unlimited_power(3)