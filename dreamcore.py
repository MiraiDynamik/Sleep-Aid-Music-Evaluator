#  Sleep-Aid-Music-Evaluator/dreamcore.py, functions here are used in main.py

import numpy as np
import librosa.feature
from scipy.stats import norm

'''
Dickson and Schubert (2020) compared nine features of music that successfully and unsuccessfully aid sleep, finding that 
three differed significantly. Successful music has a lower main frequency register, more smoothly connected notes, and 
lower rhythmic activity. This function can extract these three features.

Finding the main frequency register of music by measuring spectral centroid and finding the articulation of music by 
measuring mean decay slope is similar to the methods used in research, but according to the research, they used aural 
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

    # Measure tempo
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    seconds_per_beat = 60/tempo
    # print('tempo: {:.2f} bpm'.format(tempo))

    # Find the rhythmic activity or complexity
    onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    onset_diff = np.diff(onset_frames)

    for i in range(len(onset_diff)):
        # print(onset_diff[i])
        # print(4 * seconds_per_beat)
        if onset_diff[i] >= 4 * seconds_per_beat:
            onset_diff[i] = 4 * seconds_per_beat  # cap pauses longer than 4 beats

    activity = np.std(onset_diff)
    # print('rhythmic activity: {:.2f}'.format(activity))

    '''
    Here, I obtained the derivative of stdev to prevent the same rhythm pattern gets higher activity when it becomes 
    slower; then, I put the derivative onto an exponential to better distinguish between rhythm patterns with high 
    activity and make rhythmic patterns with low activity relatively closer.
    '''

    features = {
        'mfr': mean_centroid,
        'articulation': mean_decay_slope,
        'rhythmic_activity': activity
    }
    return features


'''
Assessment function of features extracted.
According to Dickson and Schubert (2020), I developed the criteria based on specific data directly from their research. 
However, the weight of each feature is determined by my personal experience and my own understanding of the literature. 
The referral of more research, scientific experiments, or machine learning approaches can further improve the accuracy 
of comparative weight.
'''


def assess(features):
    score = 50
    factor_mfr = 75000
    factor_articulation = 70
    factor_rhythmic_activity = -20

    # Assess main frequency register
    mean_success_mfr = 1822
    sd_success_mfr = 810
    mean_unsuccess_mfr = 2423
    sd_unsuccess_mfr = 1075

    score_mfr = assess_feature(
        features['mfr'],
        mean_success_mfr,
        sd_success_mfr,
        mean_unsuccess_mfr,
        sd_unsuccess_mfr
    )
    score_mfr *= factor_mfr

    # Assess articulation
    mean_success_articulation = -1.8
    sd_success_articulation = .71
    mean_unsuccess_articulation = -2.25
    sd_unsuccess_articulation = .88

    score_articulation = assess_feature(
        features['articulation'],
        mean_success_articulation,
        sd_success_articulation,
        mean_unsuccess_articulation,
        sd_unsuccess_articulation
    )
    score_articulation *= factor_articulation

    # Assess rhythmic activity
    score_rhythmic_activity = factor_rhythmic_activity * features['rhythmic_activity']

    # Put things together
    score += int(score_mfr + score_articulation + score_rhythmic_activity)
    print(str(score_mfr) + ' ' + str(score_articulation) + ' ' + str(score_rhythmic_activity))

    if score >= 100:
        score = 100
    if score <= 0:
        score = 0

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
