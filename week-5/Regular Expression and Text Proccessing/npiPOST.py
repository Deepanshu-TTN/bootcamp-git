import re
import requests
import json
import time
import concurrent.futures as concurrent_features


def get_NPI_list(npi_file):
    '''
    This function reads npi numbers from a file\n
    Takes in input the filename of a file with inputs in each line\n
    Filters out invalid NPI numbers and returns a valid NPI numbers list
    '''
    with open(npi_file, 'r') as f:
        return re.findall(r'[0-9]{10}', f.read())
    

def generate_npi_json(npi_list, output_json):
    '''
    This function gets information based on the input npi numbers list\n
    Takes in a list of npi numbers, writes the outputs in out.json file and returns the dictionary of the objects
    '''
    return_list = list()
    for npi in npi_list:
        r = requests.post("https://npiregistry.cms.hhs.gov/RegistryBack/npiDetails", json={"number":npi})

        #(number:npi_object) key pair is added where only non empty outer most fields of the objects exist
        return_list.append(dict([(key, value) for key, value in r.json().items() if value]))

    with open(output_json, 'a') as out:
        json.dump(return_list, out, indent=4)
    
    return return_list


def get_npi_object(npi_id):
    '''
    This function gets an object corresponding to npi number input\n
    returns a dictionary or NONE
    '''
    res = requests.post("https://npiregistry.cms.hhs.gov/RegistryBack/npiDetails", json={"number":npi_id})
    if res.json()=={}:
        return

    #(number:npi_object) key pair is added where only non empty outer most fields of the objects exist
    return dict((key,value) for key, value in res.json().items() if value)
    


if __name__ == '__main__':
    npilist = (get_NPI_list('.npis'))
    start_time = time.time()
    with concurrent_features.ThreadPoolExecutor(max_workers=40) as executor:
        dic_list = list(i for i in executor.map(get_npi_object, npilist) if i)

    with open('npi_objects.json', 'w') as out:
        json.dump(dic_list, out, indent=4)

    endtime = time.time()
    print(endtime-start_time)
    print(endtime, start_time)