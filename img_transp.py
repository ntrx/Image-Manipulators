#!/usr/bin/env python

# Image transparent maker and convertor to RGBA format


from PIL import Image
import paramiko
import os
import struct

# server settings
bs_host = '127.0.0.1'
bs_user = 'ntrx'
bs_pass = '1111'
bs_port = 22

# format settings
img_format = '.png'
rgba_format = '.smb'

# Convert white background into alpha channel in PNG files
go_transparent = True


filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in filelist:
    if f.find(img_format) >= 0:

        img_source = f
        img_output = img_source
        img_upload = img_output
        smb_output = img_source.replace(img_format, rgba_format)

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
            img.save(img_source, "PNG")

        if go_transparent:
            img_output = img_source


        im = Image.open(img_output)
        width, height = im.size



        # delete exists file
        if os.path.isfile(smb_output):
            os.remove(smb_output)
            
        while not os.path.exists(smb_output):
            print('%s => %s [w=%d, h=%d]' % (img_source, smb_output, width, height))
            if os.path.exists(smb_output) and os.path.getsize(smb_output) == 0:
                break
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
            sftp.get(remotepath='//home//' + bs_user + '//' + smb_output, localpath=os.getcwd() + '\\' + smb_output)
            sftp.close()


        # put size to file header
        f = open(smb_output, "rb+")
        byte_arr = struct.pack('<i', int(width))
        f.seek(0)
        f.write(byte_arr)
        byte_arr = struct.pack('<i', int(height))
        f.seek(4)
        f.write(byte_arr)
        f.close()


