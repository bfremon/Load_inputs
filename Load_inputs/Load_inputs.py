#!/usr/bin/env python3

import os 
import sys
import pandas as pd

def load_inputs(data_path = None, ext = 'csv',
         sheet_name = None,  sep = ';'):
    input_files = []
    ret = None
    if data_path is None:
        data_path = os.path.join(os.getcwd(), 'data')
    else:
        data_path = os.path.join(data_path)
    if ext == 'xls':
        raise NotImplementedError('xls reading is not supported')
    sys.stderr.write('Searching %s files in %s%s' %
                    ( ext, data_path, os.linesep ))
    if not os.path.exists(data_path):
        raise SyntaxError('Input path %s doesn\'t exist%s' %
                          (data_path, os.linesep))
    try:
        input_files = os.listdir(data_path)
    except:
        raise OSError()
    input_files = scan_by_ext(data_path, ext)
    if ext == 'csv':
        ret = conc_csv_files(input_files,
                               sep = sep)
    else:
        ret = conc_xlsx_files(input_files, sheet_name)
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


def conc_xlsx_files(input_files, sheet_name):
    '''Concatenate xlsx files'''
    ret = None
    n_cols = -1
    n_inputs = 0
    datas = _flatten_xlsx(input_files)
    for f_path in datas:
        for sheet in datas[f_path]:
            input_data = datas[f_path][sheet]
            if sheet_name == None:
                ret, n_cols = _conc_sheet(ret, input_data, n_cols,
                                          n_inputs, f_path, sheet)
            elif sheet_name is not None:
                if sheet in sheet_name:
                    ret, n_cols = _conc_sheet(ret, input_data, n_cols,
                                n_inputs, f_path, sheet)
                else:
                    sys.stdout.write('%s: %s dropped%s'
                                     % (f_path, sheet, os.linesep))
        n_inputs += 1
    if ret is None:
        sys.stdout.write('No data returned with %s sheet_name selection'
                         % (sheet_name))
    return ret


def conc_csv_files(input_files, sep):
    '''Concatenate csv files'''
    ret = None
    n_cols = -1
    n_inputs = 0
    for f_path in input_files:
        ext = os.path.basename(f_path).split('.')[-1]
        input_data = pd.read_csv(f_path, sep = sep)
        n_cols = _chk_add_orig_col(input_data, n_cols,
                                   n_inputs, f_path)
        ret = _conc_data(ret, input_data)
        n_inputs += 1
    return ret


def _flatten_xlsx(input_files):
    '''Flatten excel input files for sorting by wanted sheetnames'''
    ret = {}
    for f_path in input_files:
        if not f_path in ret:
            ret[f_path] = {}
        datas = pd.read_excel(f_path, sheet_name = None)
        for sheet in datas:
            ret[f_path][sheet] = datas[sheet]
    return ret


def _conc_sheet(agg_data, input_data, n_cols, n_inputs, f_path, sheet):
    '''Concatenate sheet in input_data and add orig_sheet column'''
    ret = agg_data
    n_cols =_chk_add_orig_col(input_data, n_cols, n_inputs, f_path)
    _add_orig_col(input_data, label = sheet,
                  col_lab = 'orig_sheet')
    ret = _conc_data(ret, input_data)
    return (ret , n_cols)


def _chk_add_orig_col(input_data, n_cols, n_inputs, f_path):
    '''Check that number of columns is equal to other input_datas
    and add orig_col column'''
    ret = _chk_cols_nb(input_data, n_cols,
                          n_inputs, f_path)
    _add_orig_col(input_data, f_path, 'orig_path')
    return ret


def _chk_cols_nb(input_data, n_cols, n_inputs, f_path):
    '''Check that the number of columns is equal
    to other data_inputs'''
    if n_inputs == 0:
        return len(input_data.columns)
    elif len(input_data.columns) != n_cols:
         raise ValueError('Wrong number of columns in %s' % f_path)
    return n_cols


def _add_orig_col(input_data, label, col_lab):
    '''Add orig_col column with input file path'''
    input_data.insert(len(input_data.columns),
                      col_lab,
                      [ label for i in range(len(input_data)) ])

    
def _conc_data(agg_data, chunk_data):
    '''Aggregate chunk_data to agg_data'''
    ret = None
    if agg_data is None:
        ret = chunk_data
    else:
        ret = pd.concat([ agg_data, chunk_data ])
    return ret
