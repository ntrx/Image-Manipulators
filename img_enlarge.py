#!/usr/bin/env python

# Enlarge image to specified size


from PIL import Image
import os
import struct


# format settings
img_format = '.png'
new_size = 512


filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in filelist:
    if f.find(img_format) >= 0:

        print("Enlarging", f)
        img = Image.open(f)
        width, height = img.size
                
        img = img.convert("RGBA")
        datas = img.getdata()
        rimg = Image.new('RGBA', (new_size, new_size),(0,0,0,0))
        rimg.paste(img,(0,0))
        rimg.save('new_' + f, "PNG")
                    
