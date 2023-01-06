# Task 01 – Dictionary##

# Replacing 0 balance where customers has no value in account
def span_dictionary(dist):
    for name in dist:
        print(name)
        if dist[name] == None and dist[name] == '':
            print(dist[name])
            dist[name] == 0
        else:
            print("No undefined customer balance")


# span_lamb = lambda name,dist: span_dictionary(name,dist)

# Removing customers who has 0 balance in account.
def remove_multiple(dist):
    for key in dist:
        if dist[key] == 0:
            dist.pop(key)


# adding customers
def add_customer(name, amount, dist):
    if name in dist.keys():
        pass
    else:
        dist[name] = amount


# deposit balance in existing account
def deposit(name, amount, dist):
    if name in dist.keys():
        dist[name] = dist[name] + amount
    else:
        add_customer(name, amount, dist)


# withdraw balance from existing account
def withdraw(name, amount, dist):
    
    if name in dist.keys():
        if dist[name] != 0 and dist[name] > amount:
            dist[name] = dist[name] - amount
        else:
            print("Not enough credit")
    else:
        print("You are not a registered customer")


# Testing
dist = {'John': None, 'Iris': 100, "Belliyar": 50}
span_dictionary(dist)
print(dist)

#Task-2:Classes ##

class Customer:
  def __init__(self, name, balance= 0.0):
    self.name = name
    self.balance = balance
  #def __str__(self):
    #return self.name, self.balance
c1= Customer('Robin')
c2= Customer('Claire')

def deposit(self, amount):
  if amount < 0:
    print('you can not deposit a negative amount')
  self.balance += amount
  return self.name, self.balance

def withdraw(self, amount):
  self.balance -=amount
  if self.balance < 0:
    print('you can not overdraw your account')
  return self.name, self.balance

class Savings(Customer):
  def __init__(self, name, balance=0.0, savings=0.0):
    self.balance = balance
    self.name = name
    self.savings = savings
c1=Savings('Robin')
c2=Savings('Claire')


def transtosav(self, amount):
    if amount < 0:
      print('you can not transfer a negative amount')
    self.savings += amount
    self.balance -=amount
    if self.balance < 0:
      print('you can not overdraw your account')
    return self.name, self.balance, self.savings

def transtobal(self, amount):
    if amount < 0:
      print('you can not transfer a negative amount')
    self.balance += amount
    self.savings -= amount
    if self.savings < 0:
      print('you can not have negative savings')
    return self.name, self.balance, self.savings

deposit(c1, 100)
print(c1.balance)
transtosav(c1, 50)
print(c1.balance, c1.savings)