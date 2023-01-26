#Task:1 – Hello World!###
x=input ("Type your name:")
print ("Hi" + x + "How are you doing?")
print("Welcome to the programming course," + x + "!")

#Task:2 – Reversed Words###
string= input("Type in a word: ")
print()
reverese = ''
for i in range(len(string),0,-1):
    reverese += string[i-1]
print(reverese)

#Task:3 – Fibonacci Numbers###

number = int(input("Please put the number:"))
f0 = 0
f1 = 1
if number <= 0:
  print(f0)
else:
  print(f0, ',' ,f1,end = '')
  for x in range(2,number):
    f_next = f0+f1
    print(',', f_next, end ='')
    f0 = f1
    f1 = f_next

#Task:4 – Selective Printing###
number = int(input("Please put the number:"))
for i in range(0, number, 1):
    if i % 3 != 0:
        print(i)

#Task 05 – Triangle Checking###
x, y, z = input("Enter three length of triangle by giving space between them:").split()
if x + y > z or y + z > x or x + z > y:
    flag = 1
else:
    flag = 0
while flag == 1:
    if x == y == z:
        print("Equilateral triangle")
        breakpoint
    elif x == y or y == z or x == z:
        print("Isosceles triangle")
        breakpoint
    else:
        print("Scalene triangle")
        break
else:
    print("Plese put the input again")
    x, y, z = input("Enter three length of triangle by giving space between them:").split()

#Task:6 – Decimal to Octal Conversion###
decimal = int(input("Enter the non-negative integer number"))
octal = []
i = 0
if decimal < 0:
  print("You didn't put the postivie integer number")
elif decimal == 0:
  print(0)
else:
  while(decimal!=0):
    remainder = decimal % 8
    octal.append(remainder)
    decimal = int(decimal/8)
    i = i+1
octal.reverse()
print(*octal,sep='')
