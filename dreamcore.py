#  dreamcore.py, functions here are used in main.py

import numpy as np
import librosa.feature
from scipy.stats import norm

'''
According to Dickson and Schubert (2020), researchers compared nine features of music that successfully and 
unsuccessfully aids sleep, finding three of them differed significantly. Successful music has a lower main frequency 
register, more smoothly connected notes, and lower rhythmic activity. This function can extract these three features.

Finding the main frequency register of music by measuring spectral centroid, and finding the articulation of music by 
measuring mean decay slope are similar to the methods used in research, but according to the research, they used aural 
analysis to find the rhythmic activity, which is impossible to replicate in the code, so I designed my approach to 
measure this value.
'''


def analyze(filename):
    # Load the audio as a waveform `y`
    # Store the sampling rate as `sr`
    y, sr = librosa.load(filename)

    # Measure spectral centroid
    centroids = librosa.feature.spectral_centroid(y=y, sr=sr)
    mean_centroid = np.mean(centroids)
    # print('main frequency register: {:.2f} Hz'.format(mean_centroid))

    # Measure articulation
    envelope = librosa.onset.onset_strength(y=y, sr=sr)
    decay_slopes = np.diff(envelope)
    mean_decay_slope = np.mean(decay_slopes[decay_slopes < 0])
    # print('mean decay slope: {:.2f}'.format(mean_decay_slope))

    # Find the rhythmic activity or complexity
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr)
    activity = np.std(np.diff(onset_frames))
    # print('rhythmic activity: {:.2f}'.format(activity))

    features = {'mfr': mean_centroid, 'articulation': mean_decay_slope, 'rhythmic_activity': activity}
    return features


'''
Assessment function of features extracted.
According to Dickson and Schubert (2020), I developed the criteria directly based on specific data came form their 
research. However the weight of each features are determined on my personal experience and own understanding of the 
literature. The accuracy of comparative weight can be further improved by the referral of more researches, scientific 
experiments, or machine learning approaches.
'''


def assess(features):
    score = 60
    factor_mfr = 75000
    factor_articulation = 50
    factor_rhythmic_activity = -1
    '''
    factors = {
        'mfr': {'weight': 75000, 'mean_success': 1822, 'sd_success': 810, 'mean_unsuccess': 2423, 'sd_unsuccess': 1075},
        'articulation': {'weight': 50, 'mean_success': -1.8, 'sd_success': .71, 'mean_unsuccess': -2.25, 'sd_unsuccess': .88},
        'rhythmic_activity': {'weight': -1}
    }
    '''
    # Assess main frequency register
    mean_success_mfr = 1822
    sd_success_mfr = 810
    mean_unsuccess_mfr = 2423
    sd_unsuccess_mfr = 1075

    score_mfr = assess_feature(features['mfr'], mean_success_mfr, sd_success_mfr, mean_unsuccess_mfr, sd_unsuccess_mfr)
    score_mfr *= factor_mfr

    # Assess articulation
    mean_success_articulation = -1.8
    sd_success_articulation = .71
    mean_unsuccess_articulation = -2.25
    sd_unsuccess_articulation = .88

    score_articulation = assess_feature(features['articulation'], mean_success_articulation, sd_success_articulation, mean_unsuccess_articulation, sd_unsuccess_articulation)
    score_articulation *= factor_articulation

    # Assess rhythmic activity
    score_rhythmic_activity = factor_rhythmic_activity * features['rhythmic_activity']

    # Put things together
    score += int(score_mfr + score_articulation + score_rhythmic_activity)

    if score >= 100:
        score = 100

    return score


def assess_feature(feature, mean_success, sd_success, mean_unsuccess, sd_unsuccess):
    pdf_success = norm.pdf(feature, mean_success, sd_success)  # Calculate the pdf value for successful
    pdf_unsuccess = norm.pdf(feature, mean_unsuccess, sd_unsuccess)  # and unsuccessful distributions
    score_feature = (pdf_success - pdf_unsuccess)
    return score_feature


'''
Dickson, G. T., & Schubert, E. (2020). Musical features that aid sleep. Musicae Scientiae, 1–19.
https://doi.org/10.1177/1029864920972161
'''
