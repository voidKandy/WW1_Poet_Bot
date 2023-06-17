import openai
import art
from colorama import *
import os
import sys
from tqdm import tqdm
import json
import time

json_doc = []
war_fldr = 'warpoems'
war_lst = os.listdir(war_fldr)
ww1_fldr = 'poems'
ww1_lst = os.listdir(ww1_fldr)
poems = []
for f in ww1_lst:
    if f.startswith('.'):
        continue
    try:
        with open(f'{ww1_fldr}/{f}','r') as file:
            poem = file.read()
            poem = poem.replace('\n','').replace(r'\s+', ' ')
            poems.append(poem)
            if 'AndThereWasaGreatCalm-ThomasHardy' in f:
                prompt = 'Write a poem about the end of the war, using the theme of disbelief that man could wreak such destruction.'
                data_frmt = {"prompt": prompt, "completion": poem} 
                json_doc.append(data_frmt)
                poems.remove(poem)
            if 'RepressionofWarExperience-SiegfriedSassoon' in f:
                prompt = 'Write a poem about trying to forget one’s experiences in the war, by paying attention to  the smallest of details in life'
                data_frmt = {"prompt": prompt, "completion": poem} 
                json_doc.append(data_frmt)
                poems.remove(poem)
            if 'ThePoetAsHero-SiegfriedSassoon' in f:
                prompt = 'Write a poem about hating the war, contrasting it with chivalric tales of glory'
                data_frmt = {"prompt": prompt, "completion": poem} 
                json_doc.append(data_frmt)
                poems.remove(poem)
            if 'DulceetDecorumEst-WilfredOwen' in f:
                prompt = 'Write a poem about the lies we are told about the glory of war, from the perspective of one who suffers the harsh reality'
                data_frmt = {"prompt": prompt, "completion": poem} 
                json_doc.append(data_frmt)
                poems.remove(poem)
    except Exception as e:
        print(f'Error reading file {f} : {e}')

#print(json_doc)
for f in war_lst:
    if f.startswith('.'):
        continue
    with open(f'{war_fldr}/{f}','r') as file:
            poem = file.read()
            poem = poem.replace('\n','').replace(r'\s+', ' ')
            poems.append(poem)

openai.api_key = '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'
prefix= 'Backwards engineer a prompt that would generate this poem: '
# got thru indx40/89
print(Fore.GREEN)
for poem in tqdm(poems):
    #print(poem)
    vinci_prmpt= (prefix + poem)
    poem_comp = openai.Completion.create(
        model = 'text-davinci-003',
        prompt = vinci_prmpt,
        temperature = .5,
        max_tokens = 50,
        top_p=.2,
        frequency_penalty=0,
        presence_penalty=0,
        stop=[":", ".", "   "]
    )
    for choice in poem_comp.choices:
        output = choice.text.split()
        poem_prompt = ' '.join(output)
    poem_prompt = poem_prompt.replace(r'\s+', ' ')
    #print(poem_prompt)
    data_frmt = {"prompt": poem_prompt, "completion": poem} 
    json_doc.append(data_frmt)
    time.sleep(5)


print(json_doc)
with open('data.json','w') as write_file:
        json.dump(json_doc, write_file)
key = input('Done')
if key =='':
    sys.exit()

