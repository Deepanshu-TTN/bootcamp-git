import re
import requests
import json
import time


def get_NPI_list(npi_file):
    '''
    This function reads npi numbers from a file\n
    Takes in input the filename of a file with inputs in each line\n
    Filters out invalid NPI numbers and returns a valid NPI numbers list
    '''
    with open(npi_file, 'r') as f:
        return re.findall(r'[0-9]{10}', f.read())
    

def generate_npi_objects(npi_list):
    '''
    This function gets information based on the input npi numbers list\n
    Takes in a list of npi numbers, writes the outputs in out.json file and returns the dictionary of the objects
    '''
    return_dict = dict()
    for npi in npi_list:
        r = requests.post("https://npiregistry.cms.hhs.gov/RegistryBack/npiDetails", json={"number":npi})

        #(number:npi_object) key pair is added where only non empty outer most fields of the objects exist
        return_dict[npi] = dict([(key, value) for key, value in r.json().items() if value])

    with open('out.json', 'a') as out:
        json.dump(return_dict, out, indent=4)
    
    return return_dict


npilist = (get_NPI_list('.npis'))
start_time = time.time()
generate_npi_objects(npilist)
endtime = time.time()
print(endtime-start_time)
print(endtime, start_time)