#!/usr/bin/env python3

import os 
import sys
import pandas as pd

def load_data(data_path = None, ext = 'csv',
         sheet_name = None,  sep = ';'):
    input_files = []
    ret = None
    if data_path is None:
        data_path = os.path.join(os.getcwd(), 'data')
    else:
        data_path = os.path.join(data_path)
    sys.stderr.write('Assuming %s as input path%s' %
                    (data_path, os.linesep))
    if not os.path.exists(data_path):
        raise SyntaxError('Input path %s doesn\'t exist%s' %
                          (data_path, os.linesep))
    try:
        input_files = os.listdir(data_path)
    except:
        raise OSError()
    input_files = scan_by_ext(data_path, ext)
    ret = conc_input_files(input_files,
                           sep = sep,
                           sheet_name = sheet_name)
    return ret


def scan_by_ext(data_path, ext):
    '''Scan data_path for files ending with ext extension'''
    ret = []
    for root, dirs, files in os.walk(data_path):
        for f in files:
            f_path = os.path.join(root, f)
            bs = os.path.basename(f_path)
            try:
                bs_toks = bs.split('.')
            except ValueError:
                sys.stdout.write('ERR: no dot in basename:  %s' %
                                 f_path)
                next
            ext_f = bs_toks[-1]
            if ext_f in ext:
                ret += [ f_path ]
    return ret


def conc_input_files(input_files, sep, sheet_name):
    '''Concatenate input files'''
    ret = None
    for f_path in input_files:
        ext = os.path.basename(f_path).split('.')[-1]
        if ext == 'csv':
            input_data = pd.read_csv(f_path, sep = sep)
        else:
            input_data = pd.read_excel(f_path,
                                       sheet_name = sheet_name)
        input_data.insert(len(input_data.columns),
                          'orig',
                          [ f_path for i in range(len(input_data)) ])
        if ret is None:
            ret = input_data
        else:
            ret = pd.concat([ret, input_data])
    return ret
