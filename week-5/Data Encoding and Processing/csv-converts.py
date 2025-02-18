import csv
import json
from io import StringIO

def csv_to_json(filename):
    '''
    This function creates a json file from input csv file

    '''
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=';')
        csv_data = list()
        csv_headers = list()

        for row in csv_reader:
            if csv_reader.line_num == 1:
                csv_headers = row
            else:
                try:
                    assert len(row) != 0
                    csv_data.append(dict([(key,row[csv_headers.index(key)])for key in csv_headers]))
                except AssertionError:
                    print(f"Empty row encountered at line {csv_reader.line_num}")
        
        with open(f"{filename[:-3]}json", 'w+') as jsonfile:
            json.dump((csv_data), jsonfile, indent=4)


# csv_to_json('username.csv')


def json_to_csv(filename):
    data = list()
    with open(filename, 'r') as jsonfile:
        data = json.load(jsonfile)
    header = data[0].keys()

    with open(f"{filename}.csv", 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(header)
        csvwriter.writerows(items.values() for items in data)


# json_to_csv("username.json")


def dict_to_comma_string(dictionary):
    emulator_file = StringIO()
    emulator_file.write(";".join(dictionary.keys())+"\n")
    emulator_file.write(";".join(str(value) for value in dictionary.values())+"\n")
    emulator_file.seek(0)
    print(emulator_file.read())

dictionary =     {
        "Username": "grey07",
        " Identifier": 2070,
        "First name": "Laura",
        "Last name": "Grey"
    }

dict_to_comma_string(dictionary)