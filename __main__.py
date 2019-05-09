#!/usr/bin/python2

from mydb import MyDB
from myfile import MyFile
import os

class EJS:

   mydb=None
   myf=None
  
   def __init__(s):
       s.mydb=MyDB()
       s.myf=MyFile()   
       
   def cls(s):
       try:
            os.system('cls')
       except:
            try:
               os.system('clear')
            except:
               print('clear screen function error')

   def menu(self,items):
       while True:
            aset = set()
            for x in range(len(items)):
                aset.add(str(x))
                print('\t%d.%s'%(x, items[x]))
            tip=input('\n\n\t请输入选项:')
            if tip in aset:
                return tip

   def setDB(self):
       items = ['设置数据源（默认为localhost）']
       items.append('设置数据库名（默认为test）')
       items.append('设置用户名（默认为root）')
       items.append('返回并重新连接数据库')
       while True:
            print('---------------easy java sql-------------\n')
            print('数据源:%s\t数据库:%s\t用户:%s\t连接状态：%s\n\n' % (self.mydb.mysql_url,self.mydb.db_name,self.mydb.user_name,self.mydb.isconnect()))
            tip = self.menu(items)
            if tip == '0':
                self.seturl()
                continue
            if tip == '1':
                self.setdb_name()
                continue
            if tip == '2':
                self.setuser()
                continue
            if tip == '3':
                if self.mydb.reconnect():
                    break
                else:
                    tip2 = input('数据库连接失败...继续请输入q')
                    if tip2 == 'q':
                        break

   def main(s):
       items=['一键生成java实体类文件']
       items.append('一键生成mybatis框架的dao文件（增删查改）')
       items.append('从本地excel 表读取并构建数据库')
       items.append('从本地excel 表读取并生成sql脚本')
       items.append('设置数据库')
       items.append('退出')
       while True:
           s.cls()
           print('---------------easy java sql-------------\n')
           print('数据源:%s\t数据库:%s\t用户:%s\t连接状态：%s\n\n' % (s.mydb.mysql_url,s.mydb.db_name,s.mydb.user_name,s.mydb.isconnect()))
           tip = s.menu(items)
           if tip=='0':
                if s.mydb.isconnect():
                    s.create_entity()
                continue
           if tip=='1':
                if s.mydb.isconnect():
                    s.create_dao()
                continue
           if tip=='2':
               s.create_database()
               continue
           if tip=='3':
               s.create_sql()
               continue
           if tip=='4':
              s.setDB()
              continue
           if tip=='5':
              s.close()
              break

   def create_database(self):
        self.cls()
        self.explain_xlsx()
        file_name = input('请输入待读取的xlsx文件名 (要写 .xlsx 后缀, 直接回车则返回):')
        if file_name is None or len(file_name) < 1:
            return
        script = self.myf.create_database(file_name)
        self.mydb.create_database(script)

   def create_sql(self):
        self.cls()
        self.explain_xlsx()
        file_name = input('请输入待读取的xlsx文件名 (要写 .xlsx 后缀, 直接回车则返回)：')
        if file_name is None or len(file_name) < 1:
            return
        self.myf.create_sql(file_name)

   def close(s):
       s.cls()
       s.mydb.close()
       s.myf.close()    
       print('bye!')

   def create_entity(s):
       s.cls()
       res=s.mydb.create_dict()
       print('----------------表格清单--------------\n')
       for x in res.keys():
           print(' '+x)
       tip=input('\n如果撤销生成代码则直接回车, 否则输入pojo文件夹所在项目目录（如：com.gz）:')
       if tip != None and len(tip.strip()) >= 1:
          s.myf.create_entity(res, tip)         
       
   def create_dao(s):
       s.cls()
       res=s.mydb.create_dict()
       print('----------------表格清单--------------\n')
       for x in res.keys():
           print(' '+x)
       tip=input('\n如果撤销生成代码则直接回车, 否则输入pojo文件夹所在项目目录（如：com.gz）:')
       if tip != None and len(tip.strip()) >= 1:
          s.myf.create_dao(res, tip)

   def explain_xlsx(self):
        print('本程序可读取的excel表格有如下要求：')
        print('1. 前两列必须为： name(属性名)， type(属性类型) ， 后面的列不做要求')
        print('2. 真正数据从第二行开始，第一行可填写列名')
        print('3. 整个表格的有效区域必须从第一行第一列的单元格开始')
 
   def setdb_name(s):
       s.cls()
       data=input('\n\n\t请输入新的数据库名称：')
       if data.strip()!='':
          s.mydb.db_name=data.strip() 
       else:
          input('\n\t数据库名称不能为空')

   def setuser(s):
        s.cls()
        user_name=input('\n\n\t请输入数据库用户名：')
        password=input('\n\n\t请输入数据库密码')
        if user_name.strip() !='' and password.strip()!='':
           s.mydb.user_name=user_name
           s.mydb.password=password
        else:
           input('\n\n\t用户名或密码不能为空')

   def seturl(s):
        s.cls()
        data=input('\n\n\t请输入数据源路径：')
        if data.strip()!='':
           s.mydb.mysql_url=data
        else:
           input('\n\n\t数据源路径不能为空')

if __name__=='__main__':
   con=EJS()
   con.main()
