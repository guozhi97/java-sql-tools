#!/usr/bin/python3
#-*- coding:UTF-8 -*-

import pymysql

class MyDB:
   #module of database
   mysql_url = 'localhost'
   conn=None
   
   #default get all tables
   state=True
   self_table=[]
   
   def __init__(s,name='icms',u_name='root',pwd='root'):
         s.db_name=name
         s.user_name=u_name
         s.password=pwd
         try:
             s.conn=pymysql.connect(s.mysql_url,u_name,pwd,name)
         except Exception as e:
             print('connect mysql error :',e)

   def setdb_name(s,name):
      if name.strip() != '':
         s.db_name=name
     
   def setuser_name(s,name):
      if name.strip() != '':
         s.user_name = name

   def setpassword(s,pwd):
      if pwd.strip() != '':
         s.password = pwd

   def seturl(s,url):
       if url.strip() != '':
          s.mysql_url = url
 
   def reset_state(s):
       s.state=True

   def use_table(s,alist):
       s.self_table=list(alist)
       if s.self_table != []:
          s.state=False
       else:
          s.state=True

   def reconnect(s):
       try:
           s.conn=pymysql.connect(s.mysql_url,s.user_name,s.password,s.db_name)
       except Exception as e:
           print('reconnect mysql error:',e)
           return False
       else:
           return True

   def isconnect(self):
        if self.conn is None:
            return False
        else:
            return True

   def select(s,sql):
       res=None
       cur=None
       if s.conn==None:
          print('connect is unuseful')
          return res
       try:
           cur=s.conn.cursor()
           try:
              cur.execute(sql)
              res=cur.fetchall()
           finally:
              cur.close()
       except Exception as e: 
           print('select error :',e)
       return res


   def getall_tables(s):
       select='select table_name from information_schema.tables '
       where=("where table_schema='%s'"%(s.db_name)) 
       res=s.select(select+where)
       return res

   def getcolumns(s,tb_name):
       select='select column_name,data_type,column_key from information_schema.columns '
       where=("where table_schema='%s' and table_name='%s' "%(s.db_name,tb_name))
       res=s.select(select+where)
       return res

   def create_database(self, scripts):
       if scripts is None or len(scripts) < 1:
           return False
       if self.conn is None:
           print('connect is unuseful!')
           return False
       try:
           cursor = self.conn.cursor()
           try:
               for x in scripts:
                   cursor.execute(x)
               self.conn.commit()
           finally:
               cursor.close()
       except Exception as e:
           print('connect error')
           return False
       return True

   def create_dict(s):
       tables={}
       if s.state:
          tmp_tb=s.getall_tables()
          if tmp_tb is None or len(tmp_tb) <= 0:
             return None
          data=[]
          for x in s.getall_tables():
              data.append(x[0])
       else:
          data=s.self_table
       
       for y in data:
          data_table=[]
          tmp_columns=s.getcolumns(y)
          if len(tmp_columns)<1:
             continue
          for z in tmp_columns:
             data_columns={}
             data_columns['name']=z[0]
             data_columns['type']=z[1]
             if z[2]=='PRI':
                data_columns['key']=True
             else:
                data_columns['key']=False
             data_table.append(data_columns)
          tables[y]=data_table

       return tables
       

   def close(s):
       try:
          if s.conn != None:
             s.conn.close()
       except Exception as e:
           print('connect close error !')
           #print(e)
         
if __name__=='__main__':
   db=MyDB()
   #atuple=db.getall_tables()
   #atuple=db.getcolumns('test')
   a=db.create_dict()
   print(a)
   #db.getall()
   db.close()


       


