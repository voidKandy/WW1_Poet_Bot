import os
import re

os.chdir('./poems')
parent = os.listdir()
folders = []
rename_list = []
for filename in parent:
    if filename[0] == '.':
        continue
    special_chars = re.findall(r'[^A-Za-z0-9._]', filename)
    path = './'    
    if special_chars:
        newname = re.sub(r'[^A-Za-z0-9._-]','',filename)
        rename_list.append((os.path.join(path, filename), os.path.join(path, newname)))
for oldname, newname in rename_list:
    os.rename(oldname, newname)
print('[DONE]')   

