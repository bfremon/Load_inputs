#!/usr/bin/env python3

import os
import unittest
import pandas as pd
from Load_inputs import load_inputs

class test_load_inputs(unittest.TestCase):
    test_path = os.path.join(os.getcwd(),
                                  'tmp_test')
    data_path = os.path.join(test_path,
                             'data')
    sheet_name_removed_path = os.path.join(test_path,
                                           'sheet_name_selection')

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
        self.assertRaises(SyntaxError, load_inputs)
        no_dir_path = os.path.join(self.test_path,
                                   'no_dir')
        self.assertRaises(SyntaxError, load_inputs, no_dir_path)        
        self._mk_data_path()
        os.chmod(self.data_path, 0o200)
        self.assertRaises(OSError, load_inputs, self.data_path)
        os.chmod(self.data_path, 0o600)


    def mk_input_files(self, dst_path = None, ext = 'csv',
                       n_files = 2, n_sheets = None):
        if dst_path is None:
            dst_path = self.data_path
        self._mk_data_path(path = dst_path)
        input_datas = {}
        input_paths = {}
        n_datas = 0
        if n_sheets is None:
            n_datas = n_files
        else:
            if len(n_sheets) != n_files:
                raise ValueError('len(n_sheets) should be equal to n_files')
            for n_sheet in n_sheets:
                n_datas += n_sheet
        for i in range(n_datas):
            input_datas[i] = pd.DataFrame({'a': [ i, ],
                                           'b': [ i + 1, ]})
        if ext == 'csv':       
            for k in input_datas:
                input_paths[k] = os.path.join(dst_path,
                                              '%s.csv' % k)
                input_datas[k].to_csv(input_paths[k], sep = ';')
        else:
            sheet_cnt = 0
            if n_sheets is not None:
                input_cnt = 0
                for n_sheet in n_sheets:
                    input_path = os.path.join(dst_path,
                                              '%s.xlsx' % input_cnt)
                    with pd.ExcelWriter(input_path) as writer:
                        for i in range(n_sheet):
                            input_paths[sheet_cnt] = input_path 
                            sh_name = 'Sheet %i' % int(i)
                            input_datas[sheet_cnt].to_excel(writer, 
                                                      sheet_name = sh_name)
                            sheet_cnt += 1
                    input_cnt += 1
                assert sheet_cnt == n_datas
            else:
                for k in input_datas:
                    input_paths[k] = os.path.join(dst_path,
                                                  '%s.xlsx' % k)
                    input_datas[k].to_excel(input_paths[k])
        conc_data = pd.concat([ input_datas[k] for k in input_datas ])
        return (conc_data, input_paths)
    
        
    def test_csv(self):
        conc_data = self.mk_input_files()[0]
        out_data = load_inputs(self.data_path)
        self._drop_orig_cols(out_data)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(conc_data.equals(out_data))


    def test_multiple_csv(self):
        conc_datas = self.mk_input_files(n_files = 20)
        conc_data = conc_datas[0]
        out_data = load_inputs(self.data_path)
        self._drop_orig_cols(out_data)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(conc_data.equals(out_data))

        
    def _add_col(self, input_paths, input_idx, ext):
        if ext == 'csv':
            data_i = pd.read_csv(input_paths[input_idx], sep = ';')
        else:
            data_i = pd.read_excel(input_paths[input_idx])
        data_i.insert(len(data_i.columns), 'c',
                      [ 1 for i in range(len(data_i)) ])
        if ext == 'csv':
            data_i.to_csv(input_paths[input_idx], sep = ';')
        else:
            data_i.to_excel(input_paths[input_idx])

            
    def test_csv_n_cols_different(self):
        conc_data, input_paths = self.mk_input_files()
        self._add_col(input_paths, 1, 'csv')
        self.assertRaises(ValueError, load_inputs,
                          self.data_path)

        
    def test_xls_n_cols_different(self):
        ext = 'xlsx'
        conc_data, input_paths = self.mk_input_files(ext = ext)
        self._add_col(input_paths, 1, ext)
        self.assertRaises(ValueError, load_inputs,
                          self.data_path, ext = ext)

        
    def _1sheet_excel(self, ext, n_files):
        conc_data = self.mk_input_files(ext = 'xlsx',
                                        n_files = n_files)[0]
        out_data = load_inputs(self.data_path, ext = ext)
        self._drop_orig_cols(out_data)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(conc_data.equals(out_data))

        
    def test_1sheet_excel(self):
        self._1sheet_excel('xlsx', n_files = 2)
        self.assertRaises(NotImplementedError, load_inputs,
                          self.data_path, 'xls')

        
    def test_multiple_excel(self):
        self._1sheet_excel('xlsx', n_files = 10)


    def _drop_orig_cols(self, data):
        for col_lab in ['orig_path', 'orig_sheet', 'Unnamed: 0']:
            try:
                data.drop(columns = [col_lab,], 
                      inplace = True)
            except KeyError:
                pass

            
    def test_multiple_excel_multiple_sheets(self):
        conc_data, input_paths = self.mk_input_files(ext = 'xlsx',
                                                     n_files = 3,
                                        n_sheets = [1, 2, 3])
        out_data = load_inputs(self.data_path, ext = 'xlsx')
        self._drop_orig_cols(out_data)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(conc_data.equals(out_data))

        with pd.ExcelWriter(input_paths[2], mode = 'a',
                            engine = 'openpyxl') as writer:
            wrong_col_data = pd.DataFrame({'a': [1, ], 'b': [5, ],
                                           'c': [6, ]})
            wrong_col_data.to_excel(writer,
                                    sheet_name = 'wrong_sheet')
        self.assertRaises(ValueError, load_inputs, self.data_path,
                          ext = 'xlsx')

    def test_excel_sheet_name_selection(self):
        conc_data, input_paths = self.mk_input_files(ext = 'xlsx',
                                                     n_files = 3,
                                        n_sheets = [1, 2, 3])
        out_data = load_inputs(self.data_path, ext = 'xlsx', 
                               sheet_name = [ 'Sheet 0', 'Sheet 1' ])
        # Creating a directory with same content as above, but with only 2 sheets in
        # 3rd file, used as correct result
        sel_conc_data = self.mk_input_files(self.sheet_name_removed_path,
                                            ext = 'xlsx',
                                            n_files = 3,
                                            n_sheets = [1, 2, 2])[0]
        self._drop_orig_cols(out_data)
        out_data = out_data.sort_values(by = 'a', axis = 'rows')
        self.assertTrue(out_data.equals(sel_conc_data))


    def _clean_test_path(self, test_path): 
        for root, dirs, files in os.walk(self.test_path):
            for f in files:
                f_path = os.path.join(root, f)
                os.unlink(f_path)
        for root, dirs, files in os.walk(self.test_path):
            for d in dirs:
                d_path = os.path.join(root, d)
                os.rmdir(d_path)

                
    def tearDown(self):
        self._clean_test_path(self.data_path)
        self._clean_test_path(self.sheet_name_removed_path)
        os.rmdir(self.test_path)

if __name__ == '__main__':
    unittest.main()
