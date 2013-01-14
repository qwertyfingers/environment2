import os
import csv



def check_sim_file(sim_file):
    file_check=os.path.isfile(sim_file) #check that the file exists - true if exists, otherwise false
    if file_check==True:
        result="File found"
        setup_files=[]
        setup_files.append(read_setup_file(sim_file,"sim_settings_file")[0])
        setup_files.append(read_setup_file(sim_file,"view_file")[0])
        setup_files.append(read_setup_file(sim_file,"agents_file")[0])
        
        return setup_files
    else:
        result="Error: The file could not be found"
        return result
    
    
def read_setup_file(sim_file,setup_file):
    f = open(sim_file, 'rt')
    reader=csv.reader(f)
    file_data=[]
    for i, row in enumerate(reader): #i acts as loop counter, row as the string froma row in reader
        file_data.append(row)
    f.close()
    files_to_return=[]
    for i,row in enumerate(file_data):
        if setup_file in row:
            #fix: file data contains reference to setup file, but not a file location
            files_to_return.append(file_data[i][1])    
    if len(files_to_return)>=1:
        return files_to_return
    else:
        return None