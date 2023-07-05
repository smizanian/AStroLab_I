import numpy as np
from astropy.io import fits
from astropy.utils.data import get_pkg_data_filename

def differential_photometry(frame, posx, posy, exptime):
    N = len(frame)
    M = len(frame[0])
    sigma = np.zeros(0)
    sum_minus_sky = np.zeros(0)
    SNR = np.zeros(0)
    dmax = 30
    circle = np.zeros((dmax-2, N, M))
    for d in range(2, dmax):
        sum = 0
        count = 0
        bkg_noise = np.zeros(0)
        for i in range(N):
            for j in range(M):
                if (i-posx)**2 + (j-posy)**2 <= d**2:
                    circle[d-2][i][j] = 10
                    sum += frame[i][j]
                    count += 1
                if (dmax+5)**2 <= (i-posx)**2 + (j-posy)**2 <= (dmax+14)**2:
                    bkg_noise = np.append(bkg_noise, frame[i][j])
                    circle[d-2][i][j] = 3
        sky = np.median(bkg_noise)
        sigma = np.append(sigma, d)
        sum_minus_sky = np.append(sum_minus_sky, sum-count*sky)
        SNR = np.append(SNR, (sum-count*sky)/np.sqrt(sum+count))
    f = sum_minus_sky[np.argmax(SNR)]
    instrumental_mag = -2.5*np.log10(f/exptime)
    return instrumental_mag, SNR[np.argmax(SNR)], [sigma, SNR], circle[np.argmax(SNR)]

image_data = []
image_file = get_pkg_data_filename(r'Star_1s_ISO100_Mizanian_Hajian.fits')
fits.info(image_file)
image_data.append(fits.getdata(image_file))
master = np.array(image_data[0])
mu = np.median(master)
sig = np.median(np.abs(master - np.median(master)))
print(mu, sig)
detect_limit = 100

check = np.zeros(np.shape(master))
color_number = 1

positions = []
for i in range(len(master)):
    for j in range(len(master[0])):
        if master[i][j] > detect_limit:
            positions.append([j, i])

print(len(positions))

filtered_pos = []
for i in range(len(positions)):
    check_n = 0
    for j in range(i):
        if np.abs(positions[i][0]-positions[j][0]) > 20 and np.abs(positions[i][1]-positions[j][1]) > 20:
            check_n += 1
    if check_n == i:
        filtered_pos.append(positions[i])

print(filtered_pos, len(filtered_pos))

inst_mag = []
SNRtot = []
for i in range(len(filtered_pos)):
    frame = master[filtered_pos[i][1]-40:filtered_pos[i]
                   [1]+40, filtered_pos[i][0]-40:filtered_pos[i][0]+40]
    mag, SNR, SNRplot, maskplot = differential_photometry(frame, 50, 50, 5)
    inst_mag.append(mag)
    print(mag)
    SNRtot.append(SNR)

print("---")

for i in range(len(inst_mag)):
    print(inst_mag[i] - min(inst_mag))

c = 1.22-min(inst_mag)

print("---")

print(c)

print("---")

true_mag = inst_mag + c
for i in range(len(true_mag)):
    print(true_mag[i])
