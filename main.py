from pymongo import MongoClient
from paper import *
import json


result_f = open('result', 'a')
error_f = open('error-log', 'a')


for i in open('selected_ids.json'):
    paper_id = i.strip()
    try:
        p = Paper(paper_id)
        result_f.write(str(
            '%s\n' % str({paper_id: p.get_centiment_with_paperid()})
        ))
    except Exception as e:
        error_f.write('%s\t%s\n' % (paper_id, e.message))
        continue
