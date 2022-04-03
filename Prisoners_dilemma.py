#made in Python 3.8.12

#original reward matrix:
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

from cgi import test
from html import entities
import random
from tokenize import Double
from tracemalloc import stop
from typing import Counter
import typing_extensions
import xxlimited
import matplotlib.pyplot as plt
#from Iterated_Dilemma import rewards
#from Iterated_Dilemma import a


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



def interrogation(P1, P2, rewards, noise):
    Prisoner1 = P1.cooperation()
    Prisoner2 = P2.cooperation()
    
    P1.history[0].append(Prisoner1) 
    P1.history[1].append(Prisoner2)
    P2.history[0].append(Prisoner2)
    P2.history[1].append(Prisoner1)

    if noise != 0:
        if random.random() < noise:
            Prisoner1 = not Prisoner1
        if random.random() < noise:
            Prisoner2 = not Prisoner2


    if Prisoner1 == False and Prisoner2 == False:
        P1.years += 1
        P2.years += 1
        return rewards[0]#[1,1]
        #return [1,1]
    
    if Prisoner1 == True and Prisoner2 == False:
        P1.years += 0
        P2.years += 3
        return rewards[2]#[0,3]
        #return [0,3]

    if Prisoner1 == False and Prisoner2 == True:
        P1.years += 3
        P2.years += 0
        return rewards[1]#[3,0]
        #return [3,0]

    if Prisoner1 == True and Prisoner2 == True:
        P1.years += 2
        P2.years += 2
        return rewards[3]#[2,2]
        #return [2,2]


def commands(command):
    pass


#specific prisoners(classes) and their number - even number required
def all_prg_iterations(interrogation, itr_num, prisoners_number_type, graph ,classic_run, population_red, generations_run, rewards, noise):#Kavka, Podrazak, Test_Pod, TFT, TFT2, Dobry, Spatny, Rozmar, Velky_pes, Maly_pes, 
    
    test_percentage_gen = []

#number of interrogations
    itr_num = itr_num

#CLASSIC PRISONNER'S DILEMMA
    classic_run = classic_run

#GENERATINS - EVOLUTION
#percentage of the worst prisoners swaped with best
    population_red = population_red#0.1

#"GENERATINS - EVOLUTION"
    generations_run = generations_run

    change_num = itr_num
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


#makes every 2 random prisoners to interrogate for n times
    def iteration(interrogation, itr_num, prisoners1, rewards, noise):
        prisoners2 = []
        for p in prisoners1:
            prisoners2.append(p)
    
        for n in range(itr_num):
            random.shuffle(prisoners2)

            for i in range(0, int(len(prisoners1)), 2):
        #print("Začátek")
                a = prisoners2[i]
                b = prisoners2[i+1]
                interrogation(a, b, rewards, noise)
            #print(str(type(a).__name__) + "    " + str(type(b).__name__))


    ##############################################
    ##Generation/evolutin code - elimination
    ##############################################

    population_inc = 0.1

    prisoners_len = len(prisoners1)
    n = round(population_red * prisoners_len)
    n2 = population_inc * prisoners_len
    prisoners_classes_num = []

    def generations(interrogation, change_num, prisoners1, iteration, prisoners_len, n, prisoners_classes_num):
        #print("n = " + str(n))
        #print("len(prisoners1) = " + str(len(prisoners1)))

        prisoners_classes = []
        for i in prisoners1:
            prisoners_classes.append(str(type(i).__name__))
        prisoners_classes_num.append(Counter(prisoners_classes))

        for k in range(change_num):
            print("Iterace " + str(k))
            iteration(interrogation, 1, prisoners1, rewards, noise)

        #is_sorted = True #is_sorted algorithm not correct
            change = False
            popped = 0
            for i in range(n):
        #is_sorted = True
                for j in range(0, prisoners_len-i-1):
                    if prisoners1[j].years > prisoners1[j + 1].years :
                        prisoners1[j], prisoners1[j + 1] = prisoners1[j + 1], prisoners1[j]
                        change = True

                if change:
                    prisoners1.pop()
                    popped += 1
                    change = False

    
            for i in range(n):
        #is_sorted = True
                for j in range(len(prisoners1)-1, 0+i, -1):
                    if prisoners1[j].years < prisoners1[j - 1].years :
                        prisoners1[j], prisoners1[j - 1] = prisoners1[j - 1], prisoners1[j]
                
    
            for i in range(popped):#n --> bylo původně jako range(n)
                prisoners1.append(type(prisoners1[0+i])())

    #Number of prisoners in classes + Reset years
            prisoners_classes = []
            for i in prisoners1:
                prisoners_classes.append(str(type(i).__name__))
                i.years = 0
            prisoners_classes_num.append(Counter(prisoners_classes))
    
    
        print("Entities number by iterations:")
        print(prisoners_classes_num)

    t = 0
    p = 0
    if generations_run:
        generations(interrogation, change_num, prisoners1, iteration, prisoners_len, n, prisoners_classes_num) #(interrogation, change_num, prisoners1, iteration, prisoners_len, n, prisoners_classes_num, change)
        #print(prisoners_classes_num[0].values())
    #Graph
        x = []
        enti = {}
    
    #entities
        for i in prisoners_classes_num[0].keys():
            enti[i] = []
            for k in range(itr_num):
                enti[i].append(0)
        
        #print(enti)
    #y axises + x coordinates
        for i in range(itr_num):#+1
            x.append(i)
            for k in prisoners_classes_num[i].keys():
               enti[k][i] = prisoners_classes_num[i][k]
        #print("----------")
        print(enti)

    #Graph itself
        fig, ax = plt.subplots()
        ax.stackplot(x, enti.values(), labels=enti.keys(), alpha=0.8)#, labels=enti.keys()
    
        ax.legend(loc='upper left')
        ax.set_title('Vývoj populace')
        ax.set_xlabel('Iterace')
        ax.set_ylabel('Populace')
        plt.show()
    

    





#print(test_percentage_gen)

    if classic_run:
        iteration(interrogation, itr_num, prisoners1, rewards, noise)

    #makes graph
    #TD: repair - if more than 1 instance of the same class - only one char
        if graph:
            x = []#"Prvni", "Druhy", "Trati", "Ctvrty", "P", "S", "S", "O"
            y = []
            
            print("Entities and their score:")
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
            print("Average score of entity type:")
            print(x)
            print(y)
            plt.bar(x, y)
            plt.show()

