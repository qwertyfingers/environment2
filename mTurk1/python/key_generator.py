import string
import random
import csv
from mTurk1.models import Key_sim_pair

def key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def key_checker(check_key,key_file):
   
    f = open(key_file, 'rt')
    reader=csv.reader(f)
    file_data=[]
    for i, row in enumerate(reader): #i acts as loop counter, row as the string froma row in reader
        file_data.append(row)
    f.close()
    files_to_return=[]
    for i,row in enumerate(file_data):
        if check_key in row:
            files_to_return.append(file_data[i][1])
        
    if len(files_to_return)>=1:
        return files_to_return
    else:
        return None
    

def generate_key_sim_pair(sim_file,key_length=6):
    key=key_generator(key_length)
    reward=key_generator(key_length)
    key_sim_pair=Key_sim_pair(key=key,simulation=sim_file,reward_key=reward)
    return key_sim_pair


    