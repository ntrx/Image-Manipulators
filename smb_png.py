#!/usr/bin/env python

# SMB RGRA format to PNG convertor


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



filelist = [f for f in os.listdir('.') if os.path.isfile(f)]

for f in filelist:
    if f.find(rgba_format) >= 0:

        smb_input = f
        img_output = smb_input.replace(rgba_format, img_format)

        if os.path.exists(img_output):
            print(img_output,' exists.')
            continue

        paramiko.util.log_to_file('history.log')

        # get img size
        height = 0
        width  = 0
        fp = open(f, 'rb+')
        line = fp.read(4)
        width = int(struct.unpack('<i', line)[0])
        line = fp.read(4)
        height = int(struct.unpack('<i', line)[0])
        fp.close


        print('%s => %s' % (smb_input, img_output))
        transport = paramiko.Transport(bs_host, bs_port)
        transport.connect(username=bs_user, password=bs_pass)
        sftp = paramiko.SFTPClient.from_transport(transport)
        sftp.put(localpath=os.getcwd()+'\\'+smb_input, remotepath='//home//' + bs_user + '//' + smb_input)

        # convert file on server
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(bs_host, bs_port, bs_user, bs_pass)
        client.exec_command("convert -size %dx%d -depth 8 rgba:%s %s" % (width, height, smb_input, img_output))
        client.close()

        # get back file
        success = False
        while not success:
            try:
                sftp.file(img_output, 'r')
                success = True
            except:
                print('error')                    

        sftp.get(remotepath='//home//' + bs_user + '//' + img_output, localpath=os.getcwd() + '\\' + img_output)        
        sftp.close()
    
        while os.path.getsize(img_output) == 0:
            print('%s => %s' % (smb_input, img_output))
            transport = paramiko.Transport(bs_host, bs_port)
            transport.connect(username=bs_user, password=bs_pass)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(remotepath='//home//' + bs_user + '//' + img_output, localpath=os.getcwd() + '\\' + img_output)
            sftp.close()



