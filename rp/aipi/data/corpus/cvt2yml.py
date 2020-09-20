# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import io
import yaml
import csv

def csv2list(csv_file='ChatbotData.csv'):
    corpus_list = dict()
    corpus_list["conversations"] = []
    corpus_list['categories'] = 'chichat'

    raw_list = []
    with io.open(csv_file, 'rt', encoding="utf-8") as csvfile:
        utt = csv.reader(csvfile, delimiter=',')
        for row in utt:
            print row[0].encode('utf-8')
            input_utt = row[0].encode('utf-8').replace('!','').replace('?','')
            response = row[1].encode('utf-8').replace('!','').replace('?','')
            category = row[2]#0/1/2
            corpus_list['conversations'].append([input_utt, response])

    return corpus_list


corpus_list = csv2list('ChatbotData.csv')

with io.open('data.yml', 'w', encoding="utf-8") as outfile:
    yaml.safe_dump(corpus_list, outfile, allow_unicode=True, explicit_start=True)

