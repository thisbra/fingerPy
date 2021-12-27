import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import resample
from scipy.signal import find_peaks
from SNR import SNR


def sigMain(sig, duration):


    sig = resample(sig, (len(sig) * 2) + int(0.1 * len(sig)))

    n = len(sig)


    # --- GET AND CONVERT TIMESTAMPS
    # initial_time = timestamps[0]
    # finish_time = timestamps[-1]
    # elapsed_time = finish_time-initial_time
    # number_of_seconds = elapsed_time/1000000
    
    print("Duration: " + str(duration))
    print("N: " + str(n))

    dt = duration / n
    t = np.linspace(0, duration, n)


    # --- GET FREQUENCIES VECTOR
    fcomp = np.fft.fft(sig,n)
    PSD = fcomp * np.conj(fcomp) / n
    freq = (1/(dt*n)) * np.arange(n)
    print(freq[0:45])
    L = np.arange(1, np.floor(n/2), dtype="int")

   # --- PLOT FREQUENCY SPECTRUM
    # signalsTest.plotSpecttrum(freq, PSD, L)
    # print(PSD[-1], PSD[1])
    # print(fcomp[1], fcomp[-1])
    # plt.plot(freq, fcomp)
    # plt.xlim(freq[0], freq[int(np.floor(len(freq)/2))])
    # plt.grid()

    # --- SELECT SPECIFIED FREQUENCY FOR FILTERING
    ffilt = fcomp
    freqMin = 0.38 #Hz
    freqMax = 2    #Hz
    for f in range(1,int(np.floor(len(freq)/2))):
        tempFreq = freq[f]
        if tempFreq <= freqMin or tempFreq >= freqMax:
            ffilt[f] = 0
            ffilt[-f] = 0


    # print(ffilt)
    # print("original: ", fcomp)
    # print("filtered: ",ffilt)
    PSDfilt = ffilt * np.conj(ffilt) / n


    # --- IFFT TO GET FILTERED SIGNAL
    sigfilt = np.real(np.fft.ifft(ffilt))
    for nc in range(len(sigfilt)):
        sigfilt[nc] = sigfilt[nc].real

    # --- PAD FILTERED SIGNAL
    nInds = int(len(sigfilt)*0.02)      # percetage of padding
    sigfilt[0:nInds] = sigfilt[nInds*2:nInds:-1]
    sigfilt[-1-nInds:-1] = sigfilt[-1-(nInds*2):-1-nInds]

    fig,axs = plt.subplots(2,1)

    plt.sca(axs[0])
    # --- PLOT ORIGINAL SIGNAL
    plt.plot(t, np.real(sig), label='Original signal')

    # --- PLOT FILTERED SIGNAL
    plt.plot(t, sigfilt, label="Filtered Signal")


    # --- GENERATE AND PLOT PEAKS sigfilt

    # MAX PEAKS
    horzdist = 12
    peaks = find_peaks(sigfilt, height=1, distance=horzdist)
    height = peaks[1]['peak_heights']
    peak_pos = t[peaks[0]]
    plt.scatter(peak_pos, height, color="r", label="Max peaks", marker=".")

    # MIN PEAKS
    invsig = sigfilt * -1
    minima = find_peaks(invsig.real, distance=horzdist)
    min_pos = t[minima[0]]
    min_height = invsig[minima[0]]
    min_height = min_height * -1
    plt.scatter(min_pos, min_height, color="y", label="Min peaks", marker=".")

    # --- HRV ---
    # print(peaks[0])
    timePeaksms = t[peaks[0]]*1000
    # print(t[peaks[0]])
    print(timePeaksms)
    # print(len(peaks[0]))


    rrIntervals = [0 for i in range(len(timePeaksms)-1)]
    for b in range(len(timePeaksms)-1):
        rrIntervals[b] = timePeaksms[b+1] - timePeaksms[b]


    print(rrIntervals)

    variabilities = [0 for i in range(len(rrIntervals)-1)]
    for v in range(len(rrIntervals)-1):
        variabilities[v] = rrIntervals[v+1] - rrIntervals[v]

    print(variabilities)

    soma = 0
    MSSD = [0 for i in range(len(variabilities))]
    for s in range(len(variabilities)):
        soma = soma + (variabilities[s]**2)
        # print(soma)

    rMSSD = np.sqrt(soma/len(variabilities))    #ms
    HRV = rMSSD

    # --- BPM ---
    nbpMAX = len(peak_pos)
    nbpMIN = len(min_pos)
    nbp = (nbpMIN + nbpMAX) / 2
    nbpm = int(np.around(60 * nbp / duration))


    # --- SNR ---
    SignalToNoiseRatio = abs((SNR(sig, sigfilt)).real)  # dB

    # --- PLOTS
    plt.legend()
    plt.title("Beats per Minute: %i  |  Heart-rate-variability: %i ms  |  SNR: %.4E dB" % (nbpm, HRV, SignalToNoiseRatio), fontdict={'fontsize': 20, 'fontweight': 'bold'})
    plt.suptitle("Raw FFT")
    plt.ylabel("Amplitude")
    # plt.xlabel("Time (s)")
    plt.grid()

    plt.sca(axs[1])
    plt.plot(freq[L[0:int(len(L)/2)]], np.real(PSD[L[0:int(len(L)/2)]]), color="g", label="Original PSD")
    plt.plot(freq[L[0:int(len(L)/2)]], np.real(PSDfilt[L[0:int(len(L)/2)]]), color="r", label="Filtered PSD", linestyle="--")
    # plt.title("Frequecy spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylim(-0.15, max(np.real(PSDfilt[L]))*1.1)
    plt.legend()
    plt.grid()
    plt.show()

    return HRV

