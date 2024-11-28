#from pymisp import MISPEvent, MISPObject
import json
import binascii
import io

misperrors = {'error': 'Error'}
mispattributes = {'input': ['attachment'],
                  'output': ['freetext', 'text']}

moduleinfo = {
    'version': '0.1',
    'author': 'BDF',
    'module-type': ['import'],
    'name': 'Graal import',
    'description': 'Module to import Graal file into MISP.',
    'requirements': ['PyMISP'],
    'features': "Retrieve the Routing BIC and the Institution name from the Graal file.",
    'references': ['xxxxxx'],
    'input': 'TXT format file.',
    'logo': '',
    'output': 'BIC and Institution name',
}

moduleconfig = []

def handler(q=False):
    if q is False:
        return False
    #q = json.loads(q)
    filename = q['attachment']

    try:
        my_list = []
        
        with open (filename) as f:
            lines = f.readlines()
            columns = []
            
            i = 1
            for line in lines:
                line = line.strip()
                if line:
                    if i == 1:
                        columns = [item.strip() for item in line.split('\t')]
                        i = i+1
               
                    else:
                        d = {} # dictionary to store file data (each line)
                        data = [item.strip() for item in line.split('\t')]
                        for index, elem in enumerate(data):
                            if columns[index] in ("INSTITUTION NAME","ROUTING BIC"):
                                d[columns[index]] = data[index]

                        my_list.append(d) # append dictionary to list

        return {json.dumps(my_list, indent=4)}
        #print(json.dumps(my_list, indent=4))
        
    except Exception as e:
        print(e)
        err = "Couldn't analyze file. Error was: " + str(e)
        misperrors['error'] = err
        return misperrors


def introspection():
    return mispattributes


def version():
    moduleinfo['config'] = moduleconfig
    return moduleinfo