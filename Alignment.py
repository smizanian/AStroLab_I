import os
from astropy.io import fits
from astropy.io.fits import HDUList

import numpy as np


path = os.getcwd() + "/master-az5/"
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

maxim = 0
maxim_cor_x = 0
maxim_cor_y = 0

cor_x = 0
cor_y = 0

image_count = 0
max_cor_x = []
max_cor_y = []
x_shift = []
y_shift = []

for i in images:
    cor_y = 0
    maxim = 0
    for j in i:
        cor_x = 0
        for k in j:
            if k > maxim:
                maxim = k
                maxim_cor_x = cor_x
                maxim_cor_y = cor_y
            cor_x = cor_x + 1
        cor_y = cor_y + 1
    print(maxim_cor_x)
    max_cor_x.append(maxim_cor_x)
    x_shift.append(maxim_cor_x - max_cor_x[0])
    print(maxim_cor_y)
    max_cor_y.append(maxim_cor_y)
    y_shift.append(maxim_cor_y - max_cor_y[0])
    image_count = image_count + 1

merge_image = []
merge_image_raw = []
for j in range (len(images[0]) - max(y_shift)):
    merge_image_raw = []
    for k in range (len(images[0][0]) - max(x_shift)):
        merge_image_raw.append(0)
        for i in range(len(images)):
            merge_image_raw[k] = merge_image_raw[k] + images[i][j + y_shift[i]][k + x_shift[i]]
    merge_image.append(merge_image_raw)

hdu = fits.PrimaryHDU(merge_image)
hdulist = fits.HDUList([hdu])
hdulist.writeto('Star_1s_ISO100_Mizanian_Hajian.fits')            



