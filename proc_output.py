#!/usr/bin/python
# -*- coding: utf-8 -*-

from copy import deepcopy
import os
import json
import time
import shutil
from pprint import pprint

import smallfile
from smallfile import SMFResultException, KB_PER_GB

work_dirs = ['./_mnt_gfs_smf_']

def parse_result (ifname, results):
    with open(ifname, 'rt') as infile:
        j = json.load(infile)
        params = j['params']
        rets = j['results']
        result = dict()
        #print (params['top'])
        result['top'] = params['top']
        result['operation'] = params['operation']
        result['files-per-thread'] = params['files-per-thread']
        result['threads'] = params['threads']
        result['file-size'] = params['file-size']
        result['file-per-dir-size'] = params['files-per-dir']
        result['total-files']=rets['total-files']
        result['total-io-requests']=rets['total-io-requests']

        if 'total-data-GB' in rets:
            result['total-data-GB']=rets['total-data-GB']
        else:
            result['total-data-GB']=0

        if 'pct-files-done'in rets:
            result['pct-files-done']=rets['pct-files-done']
        else:
            result['pct-files-done']=0

        result['elapsed-time']=rets['elapsed-time']

        if 'files-per-sec' in rets:
            result['files-per-sec']=rets['files-per-sec']
        else:
            result['files-per-sec']=0

        if 'total-IOPS' in rets:
            result['total-IOPS']=rets['total-IOPS']
        else:
            result['total-IOPS']=0

        if 'total-MiBps' in rets:
            result['total-MiBps']=rets['total-MiBps']
        else:
            result['total-MiBps']=0

        results.append(result)

def proc_one_dir(work_dir, results):
    for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            print('文件名：%s' % filename)
            print('文件完整路径：%s\n' % file_path)
            parse_result(file_path, results)

results = []

for work_dir in work_dirs:
    proc_one_dir(work_dir, results)

#for ret in results:
#    pprint(ret)

with open('result.csv', 'wt') as ofile:
    rec = results[0]
    for key in rec.keys():
        print ("%s " % key, end='', file=ofile)
    print ("\n", end='', file=ofile)
    for rec in results:
        for key in rec.keys():
            print ("%s " % rec[key], end='', file=ofile)
        print ("\n", end='', file=ofile)
