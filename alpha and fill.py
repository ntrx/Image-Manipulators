#!/usr/bin/env python

# Script removing all white and similar to white (manually selected) colours
# fill it with alpha-channel and filling figure founded there 


from PIL import Image
import collections
import os

nato_blue = (128, 224, 255, 255)
nato_green = (170, 255, 170, 255)
nato_red = (255, 128, 128, 255)
black = (0,0,0,255)
alpha = (255,255,255,0)


# format settings
img_format = '.png'
work_image = ""
#  remove white limit
limit = 206   

filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in filelist:
    if f.find(img_format) >= 0:

        work_image = f
        img = Image.open(work_image)
        width, height = img.size
        rimg = Image.new('RGBA',(width, height),alpha)
        img = img.convert("RGBA")
        datas = img.getdata()
        print("Found image: %s (w=%d, h=%d)" % (work_image, width, height))     

        # Found colours over than limited value and exchange it with alpha channel
        # another colors fill with black color.
        new_datas = []
        for item in datas:
            if item[0] >= limit and item[1] >= limit and item[2] >= limit:
                new_datas.append(alpha)
            else:
                new_datas.append(black)
        # Put new array with points to image
        rimg.putdata(new_datas)     

        # When founded first pixel with black colour and in this line
        # while not found black pixel filling pixels with selected colour
        # First left half, second - right half
        if True:
            # fill left half
            for y in range(0, height):
                x = 0
                while x <= int(width/2): 
                    if rimg.getpixel((x, y)) == black:
                        while x <= int(width/2) and rimg.getpixel((x+1, y)) != black:
                            rimg.putpixel((x+1, y), nato_blue)
                            x = x+1
                    x = x+1
            # fill right half
            for y in range(0, height):
                x = width-1
                while x >= int(width/2): 
                    if rimg.getpixel((x, y)) == black:
                        while x >= int(width/2) and rimg.getpixel((x-1, y)) != (black):
                            rimg.putpixel((x-1, y), nato_blue)
                            x = x-1
                    x = x-1
        # Save it to file
        rimg.save("edit " + work_image, 'PNG')

          
        #print("new data len = ", len(new_datas))
        #counts = collections.Counter(new_datas)
        #MostCommonPoint = max(counts, key=counts.get)
        #print("MostCommonPoint = ", MostCommonPoint)
