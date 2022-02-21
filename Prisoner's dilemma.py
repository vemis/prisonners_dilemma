#           P2_silent   P2_speak
# P1_silent 1/1         3/0
# P1_speak  0/3         2/2
#

#           P2_speak_f   P2_speak_t
# P1_speak_f  1/1          3/0
# P1_speak_t  0/3          2/2
#

#classes of prisoners taken from:
#https://misantrop.info/veznovo-dilema-a-komunity/
#https://php.vrana.cz/veznovo-dilema.php

#LEADING VARIABLES STARTS ON LINE 172

from cgi import test
import random
from tokenize import Double
from typing import Counter
import typing_extensions
import matplotlib.pyplot as plt



class Prisoners:
    def __init__(self) -> None:
        self.years = 0 #years in prison
        self.history = [],[]
    
#allways silent = always false
class Kavka(Prisoners):
    def cooperation(self):
        return False

#allways speak = alwys true
class Podrazak(Prisoners):
    def cooperation(self):
        return True

#TIT-FOR-TAT - start false, if opponent true - true too in next round
class TFT(Prisoners):
    def cooperation(self):
        if len(self.history[0]) == 0:
            return False
        else: 
            if self.history[1][-1] == False:
                return False
            if self.history[1][-1] == True:
                return True

#TIT-FOR-2-TAT - 
class TFT2(Prisoners):
    def cooperation(self):
        if len(self.history[0]) <= 1:
            return False
        else:            
            if self.history[1][-1] == True and self.history[1][-2] == True:
                return True
            else:
                return False

#most false, 1 in 4 true
class Dobry(Prisoners):
    def cooperation(self):
        return random.randint(0, 3) == 0

#most true, 1 in 4 false
class Spatny(Prisoners):
    def cooperation(self):
        return random.randint(0, 3) != 0
        
#pseudo-random choice
class Rozmar(Prisoners):
    def cooperation(self):
        return bool(random.getrandbits(1))

#[1]start false, [2]if both false in previous game then false, [3]if enemy true then true, 
#[4]if true and enemy false then true, [5]if both true then false
class Velky_pes(Prisoners):
    def cooperation(self):
        if len(self.history[0]) == 0:#[1]
            return False
        else:
            if self.history[0][-1] == False and self.history[1][-1] == False:#[2]
                return False
            if self.history[0][-1] == True and self.history[1][-1] == False:#[4]
                return True
            if self.history[0][-1] == True and self.history[1][-1] == True:#[5]
                return False
            elif self.history[1][-1] == True:#[3]
                return True

#[1]start true, [2]if both false in previous game then false, [3]if enemy true then true, 
#[4]if true and enemy false then true, [5]if both true then false
class Maly_pes(Prisoners):
    def cooperation(self):
        if len(self.history[0]) == 0:#[1]
            return True
        else:
            if self.history[0][-1] == False and self.history[1][-1] == False:#[2]
                return False
            if self.history[0][-1] == True and self.history[1][-1] == False:#[4]
                return True
            if self.history[0][-1] == True and self.history[1][-1] == True:#[5]
                return False
            elif self.history[1][-1] == True:#[3]
                return True
            

def interrogation(P1, P2):
    Prisoner1 = P1.cooperation()
    Prisoner2 = P2.cooperation()
    
    P1.history[0].append(Prisoner1) 
    P1.history[1].append(Prisoner2)
    P2.history[0].append(Prisoner2)
    P2.history[1].append(Prisoner1)

    if Prisoner1 == False and Prisoner2 == False:
        P1.years += 1
        P2.years += 1
        return [1,1]
    
    if Prisoner1 == True and Prisoner2 == False:
        P1.years += 0
        P2.years += 3
        return [0,3]

    if Prisoner1 == False and Prisoner2 == True:
        P1.years += 3
        P2.years += 0
        return [3,0]

    if Prisoner1 == True and Prisoner2 == True:
        P1.years += 2
        P2.years += 2
        return [2,2]


def commands(command):
    pass




"""
P1 = Kavka()
P2 = Podrazak()
P3 = TFT()
P4 = TFT2()
P5 = Rozmar()
P6 = Velky_pes()
P7 = Maly_pes()
P8 = Spatny()
"""

#
"""
a = str()
while a != "exit":
    a = input()
"""
#

###for TD: possible classes
#prisoners_classes = Prisoners.__subclasses__()
#testP = prisoners_classes[0]()


#specific prisoners(classes) and their number - even number required
prisoners_number_type = {
    Kavka : 1,
    Podrazak : 1,
    TFT : 0,
    TFT2 : 0,
    Dobry : 0,
    Spatny : 0,
    Rozmar : 0,
    Velky_pes : 0,
    Maly_pes : 0
}

#
#number of interrogations
itr_num = 3

#GENERATINS - EVOLUTION
#population change
change_num = 5
population_red = 0.4
population_inc = 0.1

#prisoners1[0].years += 0
#prisoners1[1].years += 0
#prisoners1[2].years += 0
#prisoners1[3].years += 0
#prisoners1[4].years += 0
#prisoners1[5].years += 0
#prisoners1[6].years += 0
#prisoners1[7].years += 0



prisoners1 = []

#makes classes into given number of instances 
for sp_class in prisoners_number_type:
    for number in range(int(prisoners_number_type[sp_class])):
        prisoners1.append(sp_class())

#check if number is even
if len(prisoners1) % 2 != 0:
    print("Number is not even --> exit")
    print("Number: " + str(len(prisoners1)))
    exit()


#experimental prisoners 
#prisoners1 = [P1, P2, P3, P4, P5, P6, P7, P8]



#a = random.choice(prisoners2)
#input()


#makes every 2 random prisoners to interrogate for n times
def iteration(interrogation, itr_num, prisoners1):
    prisoners2 = []
    for p in prisoners1:
        prisoners2.append(p)
    
    for n in range(itr_num):
        random.shuffle(prisoners2)

        for i in range(0, int(len(prisoners1)), 2):
        #print("Začátek")
            a = prisoners2[i]
            b = prisoners2[i+1]
            interrogation(a, b)
            #print(str(type(a).__name__) + "    " + str(type(b).__name__))


def bubbleSort(arr):
    n = len(arr)
 
    # Traverse through all array elements
    for i in range(n-1):
    # range(n) also work but outer loop will repeat one time more than needed.
 
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1] :
                arr[j], arr[j + 1] = arr[j + 1], arr[j]






"""
test = []


#print(Kavka)
#print(type(prisoners1[1]))
#print(prisoners1[1].years)
test.append(type(prisoners1[0])())
#print(prisoners1[1])
#prisoners1[1] = None
#prisoners1[1] = Kavka()
#prisoners1(prisoners1[1])
print(test[0].years)

"""

##############################################
##Celá věc s vyřazováním horších vězňů..?
##############################################


#TD: Nefunguje, při 60 Kavkách a 2 Podrazácích hned při první iteraci 62 Kavek..?
#
#
#
for i in prisoners1:
    print(i.years)
print()

prisoners_len = len(prisoners1)
n = round(population_red * prisoners_len)
n2 = population_inc * prisoners_len
prisoners_classes_num = []

print("n = " + str(n))
print("len(prisoners1) = " + str(len(prisoners1)))

for k in range(change_num):
    iteration(interrogation, 1, prisoners1)
    
    print("Po iteraci")
    print("Iterace " + str(k))
    for i in prisoners1:
        print(str(type(i).__name__) + " " + str(i.years))
    print()

    #is_sorted = True #is_sorted algorithm not correct
    for i in range(n):
        #is_sorted = True
        for j in range(0, prisoners_len-i-1):
            if prisoners1[j].years > prisoners1[j + 1].years :
                prisoners1[j], prisoners1[j + 1] = prisoners1[j + 1], prisoners1[j]
                
            #    is_sorted = False

        #for i2 in prisoners1:
        #    print(str(type(i2).__name__) + " " + str(i2.years))
        #print()


        #print("###################")
        #print(prisoners1)
        prisoners1.pop()
        #print(prisoners1)
        #print("###################")
        
        #for i2 in prisoners1:
        #    print(str(type(i2).__name__) + " " + str(i2.years))
        #print()
        #if is_sorted == True:
        #    break
        
    
    ##
    print("Vyřazení nejhoršího")
    print("Iterace " + str(k))
    for i in prisoners1:
        print(str(type(i).__name__) + " " + str(i.years))
    print()
    ##
    
    for i in range(n):
        #is_sorted = True
        for j in range(len(prisoners1)-1, 0+i, -1):
            if prisoners1[j].years < prisoners1[j - 1].years :
                prisoners1[j], prisoners1[j - 1] = prisoners1[j - 1], prisoners1[j]
                
                #is_sorted = False
        #if is_sorted == True:
        #    break
    
    ##
    print("Seřazení - od nejmenšího:")
    print("Iterace " + str(k))
    for i in prisoners1:
        print(str(type(i).__name__) + " " + str(i.years))
    print()
    ##
    
    for i in range(n):
        prisoners1.append(type(prisoners1[0+i])())
    
    ##
    print("Přidání nejlepšího:")
    print("Iterace " + str(k))
    for i in prisoners1:
        print(str(type(i).__name__) + " " + str(i.years))
    print()
    ##

    #Number of prisoners in classes + Reset years
    prisoners_classes = []
    for i in prisoners1:
        prisoners_classes.append(str(type(i).__name__))
        i.years = 0
    prisoners_classes_num.append(Counter(prisoners_classes))
    #print(Counter(mylist))
    print("k + " + str(k))
    
    

print(prisoners_classes_num)


#print(prisoners1)
print()
for i in prisoners1:
    print(i.years)




exit()

iteration(interrogation, itr_num, prisoners1)

"""
mylist = [1,7,7,7,3,9,9,9,7,9,10,0]   
print(Counter(mylist))
"""

#makes graph
#TD: repair - if more than 1 instance of the same class - only one char
x = []#"Prvni", "Druhy", "Trati", "Ctvrty", "P", "S", "S", "O"
y = []
for i in prisoners1:
    print(str(type(i).__name__) + " " + str(i.years))
    
    if not x:
        x.append(str(type(i).__name__))##
        y.append(i.years)###########
    else:
        if str(type(i).__name__) == x[-1]:
            y[-1] += i.years
        else:
            x.append(str(type(i).__name__))##
            y.append(i.years)###########
    #print("konec")

i = 0
for sp_class in prisoners_number_type:
    if int(prisoners_number_type[sp_class]) != 0:
        y[i] = y[i] / int(prisoners_number_type[sp_class])
        i += 1
        
print(x)
print(y)
plt.bar(x, y)
plt.show()


"""
def iteration(interrogation, itr_num, prisoners1):
    for n in range(itr_num):
        prisoners2 = []
        for p in prisoners1:
            prisoners2.append(p)
    
        for i in range(0, int(len(prisoners1)/2)):
        #print("Začátek")
            a = random.choice(prisoners2)
            prisoners2.remove(a)
            b = random.choice(prisoners2)
            prisoners2.remove(b)
            interrogation(a, b)
            #print(str(type(a).__name__) + "    " + str(type(b).__name__))
"""



"""
data = {'apple': 10, 'orange': 15, 'lemon': 5, 'lime': 20}
names = list(data.keys())
values = list(data.values())

fig, axs = plt.subplots(1, 3, figsize=(9, 3), sharey=True)
axs[0].bar(names, values)
axs[1].scatter(names, values)
axs[2].plot(names, values)
fig.suptitle('Categorical Plotting')
plt.show()
"""


#print(interrogation(P1, P2))#.cooperation()

"""
for i in range(0,10):
    if interrogation(P2, P5) == [2,2]:
        print("-------- 2,2 --------")

print("Roky P1: " + str(P1.years))
print("Roky P5: " + str(P5.years))
"""
"""
for i in range(0,1000):
    interrogation(P2, P4)
print("Roky P2: " + str(P2.years))
print("Roky P4: " + str(P4.years))
"""
"""
for i in range(0,1000):
    interrogation(P2, P3)
print("Roky P1: " + str(P2.years))
print("Roky P3: " + str(P3.years))
"""
"""
for i in range(0,10):
    interrogation(P1, P2)
print("Roky P1: " + str(P1.years))
print("Roky P2: " + str(P2.years))
"""


#matrix = [2],[]
#print(len(matrix[0]))

#test = interrogation(True, False)
#print(test)
#print("Prisoner1's got " + str(test[0]))
#print("Prisoner2's got " + str(test[1]))

