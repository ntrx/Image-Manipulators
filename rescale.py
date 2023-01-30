#!/usr/bin/env python

# Downscale image to specified size


from PIL import Image
import os
import struct

import cv2
import numpy as np



# format settings
img_format = '.jpg'
scale = 4


filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in filelist:
    if f.find(img_format) >= 0:

        
        img = Image.open(f)
        print("Downscaling image ", f)
        width = int(img.width / scale)
        height = int(img.height / scale)
              

        r_img = img.resize((width, height), Image.Resampling.LANCZOS)
        filename = os.path.split(f)
        print(filename)
        r_img.save(os.path.split(f)[1] + '.png', format="png")

                    