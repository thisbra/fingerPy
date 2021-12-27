import numpy as np
import scipy

def SNR(sig, sigfilt):

    signp = np.array(sig)
    Psig = ( signp@signp ) / len(sig)
    # print("Potencia sinal original:", Psig)

    sigfiltnp = np.array(sigfilt)
    Psigfilt = ( sigfiltnp@sigfiltnp ) / len(sigfilt)
    # print("Potencia sinal filtrado:", Psigfilt)

    snr = 10*np.log10(Psigfilt / Psig)

    return snr