#!/usr/bin/env python3

import os
import unittest
import pandas as pd
from Load_data import load_data

class test_Load_data(unittest.TestCase):
    test_path = os.path.join(os.getcwd(),
                                  'tmp_test')
    data_path = os.path.join(test_path,
                             'data')
    def setUp(self):
        if not os.path.exists(self.test_path):
            os.mkdir(self.test_path)

            
    def _mk_data_path(self, path = None):
        if path is None: 
            if not os.path.exists(self.data_path):
                os.mkdir(self.data_path)
        else:
            os.mkdir(path)
            
            
    def test_data_path_exists_and_is_readable(self):
        if os.path.exists(self.data_path):
            os.rmdir(self.data_path)
        self.assertRaises(SyntaxError, load_data)
        no_dir_path = os.path.join(self.test_path,
                                   'no_dir')
        self.assertRaises(SyntaxError, load_data, no_dir_path)        
        self._mk_data_path()
        os.chmod(self.data_path, 0o200)
        self.assertRaises(OSError, load_data, self.data_path)
        os.chmod(self.data_path, 0o600)


    def mk_input_files(self, ext = 'csv', n_files = 2):
        self._mk_data_path()
        input_datas = {}
        input_paths = {}
        for i in range(n_files):
            input_datas[i] = pd.DataFrame({'a': [ i, ], 'b': [ i + 1, ]})
        if ext == 'csv':       
            for k in input_datas:
                input_paths[k] = os.path.join(self.data_path, '%s.csv' % k)
                input_datas[k].to_csv(input_paths[k], sep = ';')
        else:
            for k in input_datas:
                input_paths[k] = os.path.join(self.data_path, '%s.xlsx' % k)
                input_datas[k].to_excel(input_paths[k])
        conc_data = pd.concat([ input_datas[k] for k in input_datas ])
        return (conc_data, input_paths)
    
        
    def test_csv(self):
        conc_data = self.mk_input_files()[0]
        out_data = load_data(self.data_path)
        out_data.drop(columns = ['orig', 'Unnamed: 0'],
                      inplace = True)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(conc_data.equals(out_data))


    def test_multiple_csv(self):
        conc_data = self.mk_input_files(n_files = 20)[0]
        out_data = load_data(self.data_path)
        out_data.drop(columns = ['orig', 'Unnamed: 0'],
                      inplace = True)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(conc_data.equals(out_data))

    def _add_col(self, input_paths, input_idx, ext):
        if ext == 'csv':
            data_i = pd.read_csv(input_paths[input_idx], sep = ';')
        else:
            data_i = pd.read_excel(input_paths[input_idx])
        data_i.insert(len(data_i.columns), 'c', [ 1 for i in range(len(data_i)) ])
        if ext == 'csv':
            data_i.to_csv(input_paths[input_idx], sep = ';')
        else:
            data_i.to_excel(input_paths[input_idx])

            
    def test_csv_n_cols_different(self):
        conc_data, input_paths = self.mk_input_files()
        self._add_col(input_paths, 1, 'csv')
        self.assertRaises(ValueError, load_data, self.data_path)

        
    def test_xls_n_cols_different(self):
        ext = 'xlsx'
        conc_data, input_paths = self.mk_input_files(ext = ext)
        self._add_col(input_paths, 1, ext)
        self.assertRaises(ValueError, load_data, self.data_path, ext = ext)

        
    def _1sheet_excel(self, ext, n_files):
        conc_data = self.mk_input_files(ext = 'xlsx', n_files = n_files)[0]
        out_data = load_data(self.data_path, ext = ext)
        out_data.drop(columns = ['orig', 'Unnamed: 0'],
                      inplace = True)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(conc_data.equals(out_data))

        
    def test_1sheet_excel(self):
        self._1sheet_excel('xlsx', n_files = 2)
        self.assertRaises(NotImplementedError, load_data,
                          self.data_path, 'xls')

        
    def test_multiple_excel(self):
        self._1sheet_excel('xlsx', n_files = 10)
        
        
    def tearDown(self):
        for root, dirs, files in os.walk(self.test_path):
            for f in files:
                f_path = os.path.join(root, f)
                os.unlink(f_path)
        for root, dirs, files in os.walk(self.test_path):
            for d in dirs:
                d_path = os.path.join(root, d)
                os.rmdir(d_path)
        os.rmdir(self.test_path)
            
if __name__ == '__main__':
    unittest.main()
