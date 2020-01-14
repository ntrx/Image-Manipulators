Here is some scripts for image processing for work

All scripts have settings in header and works with all files in folder (which files is actually is based on extension which setups in settings)

Requires: Python 3.5+, paramiko (for ssh), PIL (image processing), some default modules.
Input: png file(s) or rgba file(s)

alpha and fill.py:
 exchange white color with alpha channel (transparency color) and others color with user selected color, after it fill figure which we got and fill it with another selected color.
 
 img_transp.py:
 exchange white color with alpha channel (transparency color) and create RGBA file with additional 16 bytes in header with size in first 8 bytes (9-16 bytes is reserved)
 
 smb_png.py:
   try to extract RGBA format to png
