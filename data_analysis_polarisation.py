
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import pandas as pd

""" This script is used to run additionnal analysis on the data obtained from the model simulation."""


# ------- Polarization 

""" We use a Kernel Density Estimate to compute a polarization score for each debate."""
# Extracting opinions 
#opinions = np.array([0, 0.1, 0.15, 0.8, 0.88, 0.85]).reshape(-1, 1)
#opinions2 = np.array([0.10,0.11,0.9,0.23,0.21,0.11,0.45,0.20,0.11,0.2])



def get_polarization_score(opinions, bandwith):

        opinions = opinions.reshape(-1, 1)
        # KDE
        kde = KernelDensity(kernel='gaussian', bandwidth=bandwith).fit(opinions)

        # generating linear space 
        s = np.linspace(0,1)
        e = kde.score_samples(s.reshape(-1,1))

        plt.plot(s, e)
        plt.scatter(opinions, [0 for x in opinions])
        plt.show()

        # Extracting the number of local maximums
        # TODO
        # see https://stackoverflow.com/questions/35094454/how-would-one-use-kernel-density-estimation-as-a-1d-clustering-method-in-scikit/35151947#35151947

        mi, ma = argrelextrema(e, np.less)[0], argrelextrema(e, np.greater)[0]
        # print("Minima:", mi, s[mi])
        # print("Maxima:", ma, s[ma])

        maxima = s[ma]
        nb_of_clusters = len(maxima)
        return nb_of_clusters


# print(get_polarization_score(opinions,0.05))

# print(get_polarization_score(opinions2,0.1))
# print(get_polarization_score(opinions2,0.05))

# ================= TESTS  - generating opinions to select best bandwith 


def test_bandwith():

    bandwiths = [0.5, 0.3, 0.2, 0.1, 0.05, 0.01]

    # case 1 : Evenly distributed

    rng = np.random.default_rng()
    random_opinions = [rng.random(50) for i in range(5)]

    # case 2 : bimodal opinions 

    mu_list = [(0.1, 0.8), (0.4, 0.6),(0.8, 0.9)]
    sigma_list = [(0.1, 0.1),(0.02,0.02), (0.01, 0.01)]
    bimodal_opinions = []
    for i in range(len(mu_list)):
        N=np.random.randint(10,40) # randomly generating the number of people to be drawn from distribution 1 
        mu, mu2 = mu_list[i]
        sigma, sigma2 = sigma_list[i]
        X1 = np.random.normal(mu, sigma, N)
        X2 = np.random.normal(mu2, sigma2, 50 - N)
        op = np.concatenate([X1, X2])
        bimodal_opinions += [op]


    # getting the scores

    for b in bandwiths:
        print(b)
        print()
        scores = []
        for op in bimodal_opinions:
            s = get_polarization_score(op, b)
            scores += [s]
            print(s)
        print('Average : ', np.average(scores) )
        print()


# ======================== TEST on real opinion data

# Choice of Bandwith 
bandwith = 0.1






# Compute the polarisation score

