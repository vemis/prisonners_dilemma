from Prisoners_dilemma import *

#made in Python 3.8.12
#What reward matrix do you want?
#Should be in format:
#S > P > R > T
#               Player2_silent   Player2_speak
# Player1_silent    [R,R],             [S,T],
# Player1_speak     [T,S],             [P,P]
rewards = [
                    [1,1],             [3,0],
                    [0,3],             [2,2]
]

#How many iterations do you want to run?
itr_num = 5

#Noise == chances of reversing an entity's decision - from 0.0 to 1.0
noise = 0.0

#How many of which entities do you want to use? - the sum of all numbers must be even
prisoners_number_type = {
    Kavka : 0,
    Podrazak : 100,
    TFT : 900,
    TFT2 : 0,
    Dobry : 0,
    Spatny : 0,
    Rozmar : 0,
    Velky_pes : 0,
    Maly_pes : 0
}

#Do you want a graph? True/False
graph = True

#What percentage of the entities with worst score from set of entities 
#do you want to change for the entities with best score per iteration?
#numbers from 0.0 to 1.0
per_change = 0.1


###########################
###########################
###########################
###########################
###########################

#Do not change, unless you know what you are doing
all_prg_iterations(interrogation, itr_num, prisoners_number_type, graph ,False, per_change, True, rewards,
            noise)