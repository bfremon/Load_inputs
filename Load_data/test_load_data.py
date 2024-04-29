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

        
    def test_csv(self):
        self._mk_data_path()
        data1 = pd.DataFrame({'a': [1,], 'b': [2,]})
        data2 = pd.DataFrame({'a': [3,], 'b': [4,]})
        data1.to_csv(os.path.join(self.data_path, '1.csv'), sep = ';')
        data2.to_csv(os.path.join(self.data_path, '2.csv'), sep = ';')
        sum_data = pd.concat([data1, data2])
        out_data = load_data(self.data_path)
        out_data.drop(columns = ['orig', 'Unnamed: 0'],
                      inplace = True)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(sum_data.equals(out_data))

        
    def _1sheet_excel(self, ext):
        self._mk_data_path()
        data1 = pd.DataFrame({'a': [1,], 'b': [2,]})
        data2 = pd.DataFrame({'a': [3,], 'b': [4,]})
        data1.to_excel(os.path.join(self.data_path, '1.%s' % ext))
        data2.to_excel(os.path.join(self.data_path, '2.%s' % ext))
        sum_data = pd.concat([data1, data2])
        out_data = load_data(self.data_path, ext = ext)
        out_data.drop(columns = ['orig', 'Unnamed: 0'],
                      inplace = True)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(sum_data.equals(out_data))

        
    def test_1sheet_excel(self):
        self._1sheet_excel('xlsx')
        self.assertRaises(NotImplementedError, load_data,
                          self.data_path, 'xls')
        
        
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
