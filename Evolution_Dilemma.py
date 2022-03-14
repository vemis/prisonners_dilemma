from Prisoners_dilemma import *

#How many iterations do you want to run?
itr_num = 4

#How many of which entities do you want to use? - the sum of all numbers must be even
prisoners_number_type = {
    Kavka : 11,
    Test_Pod : 0,
    Podrazak : 1,
    TFT : 0,
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
#numbers from 0 to 1
per_change = 0.1


###########################
###########################
###########################
###########################
###########################
all_prg_iterations(interrogation, itr_num, prisoners_number_type, graph ,False, per_change, True)