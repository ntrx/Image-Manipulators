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
go_transparent = False
# If need enlarge image
go_enlarge = False
enlarge_to = 0.2 # scale



filelist = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in filelist:
    if f.find(img_format) >= 0:

        img_source = f
        img_output = img_source
        img_upload = img_output
        smb_output = img_source.replace(img_format, rgba_format)

        if os.path.exists(smb_output):
            print(smb_output,' exists.')
            continue

        paramiko.util.log_to_file('history.log')

        img = Image.open(img_upload)
        width, height = img.size

        if go_transparent:            
            img = img.convert("RGBA")
            datas = img.getdata()
            if go_enlarge:
                rimg = Image.new('RGBA',(width+int(width*enlarge_to), height+int(height*enlarge_to)),(0,0,0,0))
                rimg.paste(img,(int(width*enlarge_to),int(height*enlarge_to)))
                datas = rimg.getdata()
            
                                        


            newData = []
            for item in datas:
                '''
                    NATO colours:
                    white -> alpha channel = 0,0,0,0
                    black: 255, 255, 255, 255
                    Blue: 128, 224, 255, 255
                    Green: 170, 255, 170, 255
                    Red: 255, 128, 128, 255
                '''
                if item[0] == 128 and item[1] == 224 and item[2] == 255:
                    newData.append((255, 128, 128, 255))
                else:
                    newData.append(item)

            if not go_enlarge:
                img.putdata(newData)
                img.save(img_source, "PNG")
            else:
                rimg.putdata(newData)
                rimg.save(img_source, "PNG")
                    

        if go_transparent:
            img_output = img_source


        print('%s => %s [w=%d, h=%d]' % (img_source, smb_output, width, height))
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
        success = False
        while not success:
            try:
                sftp.file(smb_output, 'r')
                success = True
            except:
                print('error')                    

        sftp.get(remotepath='//home//' + bs_user + '//' + smb_output, localpath=os.getcwd() + '\\' + smb_output)
        
        sftp.close()
    
        while os.path.getsize(smb_output) == 0:
            print('%s => %s [w=%d, h=%d]' % (img_source, smb_output, width, height))
            transport = paramiko.Transport(bs_host, bs_port)
            transport.connect(username=bs_user, password=bs_pass)
            sftp = paramiko.SFTPClient.from_transport(transport)
            sftp.get(remotepath='//home//' + bs_user + '//' + smb_output, localpath=os.getcwd() + '\\' + smb_output)
            sftp.close()


        # create output dir
        dir_name = 'output'
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        # put size to file header with creating new file
        f = open(dir_name+'\\r_'+smb_output, "wb+")
        byte_arr = struct.pack('<i', int(width))
        f.seek(0)
        f.write(byte_arr)
        byte_arr = struct.pack('<i', int(height))
        f.seek(4)
        f.write(byte_arr)
        byte_arr = struct.pack('<d', 0)
        f.write(byte_arr)
        f.close()

        out = open(smb_output, 'rb+')       

        first = True
        with open(dir_name + '\\r_' + smb_output, 'ab+') as output:
            if first:
                output.seek(16)
                first = False
            output.write(out.read())
        out.close()
        output.close()



