from Prisoners_dilemma import *

#How many iterations do you want to run?
itr_num = 10

#How many of which entities do you want to use? - the sum of all numbers must be even
prisoners_number_type = {
    Kavka : 0,
    Test_Pod : 0,
    Podrazak : 2,
    TFT : 10,
    TFT2 : 0,
    Dobry : 0,
    Spatny : 0,
    Rozmar : 0,
    Velky_pes : 0,
    Maly_pes : 0
}

#Do you want a graph? True/False
graph = True


###########################
###########################
###########################
###########################
###########################
all_prg_iterations(interrogation, itr_num, prisoners_number_type, graph ,True, 0, False)