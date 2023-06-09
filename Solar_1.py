import os
from typing import List
from astropy.io import fits
from astropy.io.fits import HDUList
from matplotlib import pyplot as plt
import numpy as np

def master_image(images: List[np.ndarray]) -> np.ndarray:
    stacked_array = np.stack(images)
    return np.median(stacked_array, axis=0)

def normalize_array(a):
    return a/np.max(a)

def normalize_flat(a):
    return a/np.median(a)

def image_bin(a, y_c, index):
    sum_flux = 0
    count = 0
    for i in range(-3,4):
        for j in range(-3, 4):
            sum_flux+=a[16][y_c+j][index+i]
            count = count+1
    return sum_flux/count

def flux_rms(a, y_c, index):
    sum_flux = 0
    count = 0
    for i in range(-10,11):
        for j in range(-10, 11):
            sum_flux+=(a[16][y_c+j][index+i])**2
            count = count+1
    return sum_flux//count 

sun_radius = 30

path = os.getcwd() + "/data/fits/"
filenames = os.listdir(path)
filenames.sort()

print(filenames)

hdu_list = HDUList()
print('Reading FITS files...')
for filename in filenames:
    print(f'Read {filename}')
    hdu_list.append(fits.open(path + filename)[0])

images = []
for hdu in hdu_list:
    images.append(hdu.data)

hdu_list.close()

print('Starting image processing...')
print(master_image(images[0:5]))

start_h = 0
end_h = 0

images.append((images[15] - master_image(images[5:9]))/(normalize_flat(master_image(images[10:14])-master_image(images[0:4]))))


print(len(images[16][0]))
for i in range(len(images[16][0])):
    if(images[16][0][i]>sun_radius):
        start_h = i
        break;

for i in range(len(images[16][0])):
    if(images[16][0][3905-i]>sun_radius):
        end_v = i
        break;


start_v = 0
end_v = 0
print(len(images[16]))
for i in range(len(images[16])):
    if(images[16][i][3905]>sun_radius):
        start_v = i
        break;

y_c = start_v + (len(images[16]) - start_v)//2
x_c = start_h + (len(images[16][0]) - start_h - end_h)//2

print("center of sun")
print(x_c)
print(y_c)
print(images[16][y_c][x_c])

print("Datas of sun")

sun_data_x = []
sun_data_y = []

radius = 0

for i in range(x_c):
    if(images[16][y_c][i]>sun_radius and radius==0):
        radius = i

radius = x_c - radius
print(radius)

for i in range(x_c):
    if(i%100 == 0 and (x_c - i) < radius):
        sun_data_x.append(x_c - i)
        sun_data_y.append(image_bin(images, y_c, i))
        print(image_bin(images, y_c, i))

sun_data_y = normalize_array(sun_data_y)

print("Plot: data of sun")
plt.plot(sun_data_x, sun_data_y, marker='o')
plt.xlabel("radius (pixel)")
plt.ylabel("normalized flux")
plt.show()

print("Plot: mu")

mu_data_x = []
mu_data_y = []

edd_data_y = []
mu = 0

for i in range(x_c):
    if(i%100 == 0 and (x_c - i) < radius):
        mu = (1-((x_c - i)/radius)**2)**0.5
        mu_data_x.append(mu)
        mu_data_y.append(image_bin(images, y_c, i))
        edd_data_y.append((2+3*mu)/5)
        print(image_bin(images, y_c, i))

mu_data_y = normalize_array(mu_data_y)

plt.plot(mu_data_x, mu_data_y, color='g', label='solar data', marker='o')
plt.plot(mu_data_x, edd_data_y, color='r', label='eddington modle')
plt.xlabel("mu")
plt.ylabel("normalized flux")
plt.show()

print("flux RMS")

rms_data_x = []
rms_data_y = []

for i in range(x_c):
    if(i%100 == 0 and (x_c - i) < radius):
        rms_data_x.append(x_c - i - 2)
        rms_data_y.append(flux_rms(images, y_c, i))
        print(flux_rms(images, y_c, i))
        
plt.plot(rms_data_x, rms_data_y, marker='o')
plt.xlabel("radius (pixel)")
plt.ylabel("flux rms")
plt.show()

    
