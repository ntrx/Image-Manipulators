#!/usr/bin/env python

# Image transparent maker and convertor to RGBA format


from PIL import Image
import paramiko
import os
import struct

# source for non-transparent file
img_source = 'headquarters_unit'
# Make this file transparent (white to alpha channel), True if yes.
go_transparent = True

# format settings
img_format = '.png'
rgba_format = '.smb'



# server settings
bs_host = '192.168.9.111'
bs_user = 'ntrx'
bs_pass = '1111'
bs_port = 22


img_output = img_source

img_upload = img_output + img_format
if not go_transparent:
    smb_output = img_source + rgba_format
else:
    smb_output = img_source + '_a' + rgba_format
        

paramiko.util.log_to_file('history.log')


if go_transparent:
    img = Image.open(img_upload)
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save(img_source + '_a' + img_format, "PNG")

if go_transparent:
    img_output = img_source + '_a' + img_format


im = Image.open(img_output)
width, height = im.size



print(width, height)


# put file to server
transport = paramiko.Transport(bs_host, bs_port)
transport.connect(username=bs_user, password=bs_pass)
sftp = paramiko.SFTPClient.from_transport(transport)
sftp.put(localpath=os.getcwd()+'\\'+img_output, remotepath='//home//' + bs_user + '//' + img_output)

# convert file on server
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(bs_host, bs_port, bs_user, bs_pass)
client.exec_command("convert %s rgba:%s" % (img_output, smb_output))
client.close()

# get back file
sftp.get(remotepath='//home//' + bs_user + '//' + smb_output, localpath=os.getcwd() + '\\' + img_source + rgba_format)
sftp.close()


# put size to file header
f = open(img_source + rgba_format, "rb+")
byte_arr = struct.pack('<i', int(width))
f.seek(0)
f.write(byte_arr)
byte_arr = struct.pack('<i', int(height))
f.seek(4)
f.write(byte_arr)
f.close()


