import matplotlib.pyplot as plt
import numpy             as np
import scipy.io.wavfile  as siw
import sys
import copy

# Convert stereo to mono

# Also, shorten long audio files (at the moment, to be the first 20s),
# in order to have more reasonable file sizes

# ------------------------------------------------------------------------
# ------------------------- read in and setup-----------------------------

# Read in wave file, and have these pieces:
#    rate : sampling frequency (units of Hz)
#    data : 1- or 2-D array of time series

# read in the information
infile_wav  = '07062015_lions.wav' # '07062029_chimp.wav'
max_seconds = 20



rate, data    = siw.read(infile_wav)
try:
    Nchannel, N = np.shape(data.T)     # number of channels, number of time pts
except:
    # is mono
    N        = len(data)
    Nchannel = 1
dtype_dat   = data.T.dtype.name    # store type of data, for writing out
out_base    = infile_wav.replace('.wav', '')  # output base

# -------------------- check length, and maybe shorten ---------------------

# output the full number of data points by default, but shorten if
# max_seconds is less
MAX_N      = N 
ts         = 1./rate
maxnwanted = int(max_seconds / ts)

if maxnwanted < MAX_N:
    MAX_N = maxnwanted

# ------------------------ combine channels, if necessary -------------------

if Nchannel == 1 :
    print("This file is mono-- no channels to combine!")
    mono_arr = copy.deepcopy(data)
else:    

    # initialize and declare 
    mono_arr    = np.zeros(N)   # float at the moment

    # average the channels
    for n in range(Nchannel):
        mono_arr+= data.T[n]
    mono_arr/= Nchannel

# ------------------------ write output -------------------

# Write out mono array in units of input data.

# MAX_N will either be 'N' (for short clips) or 'maxnwanted' (for
# long clips

out_f = out_base + '_mono_short.wav'
siw.write(out_f, rate, mono_arr[:MAX_N].astype(dtype_dat)) 
print("Wrote output:  {}".format(out_f))

print("Done!")
