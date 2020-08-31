from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
import copy 




def spectra_baseline(sig, Wn, iterations):
    sig_work = copy.copy(sig)
 
    b, a = signal.butter(1, Wn)
    for i in range(int(round(iterations))-1):
        fgust = signal.filtfilt(b, a, sig_work,  padlen=len(sig)-1)
        less = fgust <= sig_work
        sig_work[less] = fgust[less]
    fgust = signal.filtfilt(b, a, sig_work,  padlen=len(sig)-1)
    return fgust
