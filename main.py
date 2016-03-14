from pymongo import MongoClient
from paper import *
import json


f = open('pselected.json')
j = json.load(f)

for i in j:
    p = Paper(i['doi'])
    result_f = open('result', 'a')
    error_f = open('error-log', 'a')
    try:
        result_f.write(str(
            '%s\n' % str({i['doi']: p.get_centiment_with_paperid()})
        ))
    except Exception as e:
        error_f.write('%s\t%s\n' % (i['doi'], e.message))
        continue
