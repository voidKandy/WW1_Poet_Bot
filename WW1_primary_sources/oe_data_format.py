import os
import json

json_doc = []
war_fldr = 'warpoems'
war_lst = os.listdir(war_fldr)
ww1_fldr = 'poems'
ww1_lst = os.listdir(ww1_fldr)
poems = []

for f in ww1_lst:
    if f.startswith('.'):
        continue
    with open(f'{ww1_fldr}/{f}','r') as file:
            poem = file.read()
            poem = poem.replace('\n','').replace(r'\s+', ' ')
            poems.append(poem)
for f in war_lst:
    if f.startswith('.'):
        continue
    with open(f'{war_fldr}/{f}','r') as file:
            poem = file.read()
            poem = poem.replace('\n','').replace(r'\s+', ' ')
            poems.append(poem)


for poem in poems:
    data_frmt = {"prompt": '', "completion": poem} 
    json_doc.append(data_frmt)

with open('oe_data.json','w') as write_file:
        json.dump(json_doc, write_file)
key = input('Done')
if key =='':
    sys.exit()
