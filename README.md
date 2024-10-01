The project was started in March 2024 as the create task of AP CSP exam 2024.

It can give scores to indicate whether a music can facilitate sleep.

The project consist of a python backend and a web GUI, but it is a local eel app instead of a web app.

Dickson and Schubert (2020) compared nine features of music that successfully and unsuccessfully aid sleep, finding that three differed significantly. Successful music has a lower main frequency register, more smoothly connected notes, and lower rhythmic activity. dreamcore.py can extract these three features.

Finding the main frequency register of music by measuring spectral centroid and finding the articulation of music by measuring mean decay slope are close simulations to the methods used in research, but according to the research, they used aural analysis to find the rhythmic activity, which is impossible to replicate in the code. My approach will calculate the entropy of the rhythms to quantify the rhythmic activity.

According to Dickson and Schubert (2020), I developed the criteria based on specific data directly from their research. However, the weight of each feature(when calculating the final score) is determined by my personal experience and understanding of the literature. The referral of more research, quantitative experiments, or machine learning approaches can further improve the accuracy of the weights of the three features.

Dickson, G. T., & Schubert, E. (2020). Musical features that aid sleep. Musicae Scientiae, 1–19.
https://doi.org/10.1177/1029864920972161
