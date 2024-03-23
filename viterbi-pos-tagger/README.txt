
----------HOW TO RUN-----------------------------------------------------------------

run `python postagger.py` in terminal with the necessary data in the working dir and installed python version


----------HOW OOV ITEMS WERE HANDLED------------------------------------------------------

In the program, out-of-vocabulary items are initially handled by being passed into max_prob() function.
The transition HMM probabilities were pracically only used as small constant was the likelihood for all OOV items...
now it defaults to using the base probability of the current POS tag without penalization
