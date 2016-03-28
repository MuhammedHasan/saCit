from pymongo import MongoClient
from paper import *
import json
import multiprocessing
from joblib import Parallel, delayed
import time
import ast

paper_ids = set([i.strip() for i in open('selected_ids.json')])

result_f = open('result')
paper_ids = paper_ids.difference(
    [ast.literal_eval(i).keys()[0] for i in result_f])
result_f.close()

result_f = open('error-log')
paper_ids = paper_ids.difference([i.split('\t')[0] for i in result_f])
result_f.close()

paper_ids = list(paper_ids)


# def job(paper_id):
#    result_f = open('result', 'a')
#    error_f = open('error-log', 'a')
#    p = Paper(paper_id)
#    result_f.write(str(
#        '%s\n' % str({paper_id: p.get_centiment_with_paperid()})
#    ))


def job(paper_id):
    result_f = open('result', 'a')
    error_f = open('error-log', 'a')
    try:
        p = Paper(paper_id)
        result_f.write(str(
            '%s\n' % str({paper_id: p.get_centiment_with_paperid()})
        ))
    except Exception as e:
        error_f.write('%s\t%s\n' % (paper_id, e.message))


num_cores = multiprocessing.cpu_count()
Parallel(n_jobs=num_cores)(delayed(job)(i) for i in paper_ids)
