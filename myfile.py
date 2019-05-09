#!/usr/bin/python3
#-*- coding:utf-8 -*-

import os
import xlrd
import time
from MakeCode.daoCode import DaoCode
from  MakeCode.typeConversion import TypeConversion
from MakeCode.pojoCode import PojoCode
from MakeCode.sqlCode import SQLCode

class MyFile:
#create and output file to computer

    jtype = TypeConversion()

    #location of output
    dir_name='result'

    dir_entity='pojo'
    dir_dao='dao'

    dir_sql='sql'

    def __init__(s):
       if not os.path.exists(s.dir_name):
          os.mkdir(s.dir_name)
       if not os.path.exists(s.dir_name+'/'+s.dir_entity):
          os.mkdir(s.dir_name+'/'+s.dir_entity)
       if not os.path.exists(s.dir_name+'/'+s.dir_dao):
          os.mkdir(s.dir_name+'/'+s.dir_dao)
       if not os.path.exists(s.dir_name+'/'+s.dir_sql):
          os.mkdir(s.dir_name+'/'+s.dir_sql)

    def close(s):
        pass

    def output(s,fname,content):
        try:
           f = open(fname, 'w')
           try:
               f.write(content)
               f.flush()
           finally:
               f.close()
        except Exception as e:
           print('output file error')

    def read_xlsx(self, file_name):
        if file_name is None or len(file_name) < 1:
            return None
        adict = dict()
        try:
            excel = xlrd.open_workbook(file_name)
            sheels = excel.sheets()
            for x in sheels:
                tmp_col = list()
                name = x.name
                ncol = x.ncols
                nrow = x.nrows
                if name is None or len(name) < 1:
                    continue
                if ncol is None or ncol < 1:
                    continue
                if nrow is None or nrow < 1:
                    continue
                for y in range(1, nrow):
                    tmp_row = dict()
                    tmp_row['name'] = x.cell_value(y, 0)
                    tmp_row['type'] = x.cell_value(y, 1)
                    tmp_col.append(tmp_row)
                adict[name] = tmp_col
        except Exception as e:
            print(e)
            pass
        return adict

    def create_sql(self, file_name):
        sheets = self.read_xlsx(file_name)
        script = SQLCode.make(sheets)
        try:
            f = open(self.dir_name + '/' + self.dir_sql  + '/' + time.strftime('%Y-%m-%d-%H-%M-%S',time.localtime(time.time())) + '.sql', 'w')
            try:
                for x in script:
                    f.write(x+';\n')
                f.flush()
            finally:
                f.close()
        except Exception as e:
            print(e)

    def create_database(self, file_name):
        sheets = self.read_xlsx(file_name)
        script = SQLCode.make(sheets)
        return script

    def create_entity(s,tables, path='com'):
        if tables == None or len(tables)<1:
           return None
        for x,y in tables.items():
            id_name = 'id'
            id_type = 'String'
            for z in y:
                if z is None or len(z) < 2:
                    continue
                z['type'] = s.jtype.get(z['type'])
                if z['key']:
                    id_name = z['name']
                    id_type = z['type']
            con = PojoCode.make(x,y, path)
            s.output(s.dir_name+'/'+s.dir_entity+'/Tb'+x.capitalize()+'.java',con)

    def create_dao(s,tables, path='com'):
        if tables==None or len(tables)<1:
           return None
        for x,y in tables.items():
            id_name = 'id'
            id_type = 'String'
            for z in y:
                if z is None or len(z) < 2:
                    continue
                z['type'] = s.jtype.get(z['type'])
                if z['key']:
                    id_name = z['name']
                    id_type = z['type']
            con=DaoCode.make(x,y,id_name,id_type, path)
            s.output(s.dir_name+'/'+s.dir_dao+'/'+x.capitalize()+'Dao.java',con)

if __name__ == '__main__':
    m = MyFile()
    m.create_sql('temp.xlsx','hehe')
 
