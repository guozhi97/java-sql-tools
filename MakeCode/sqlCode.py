
class SQLCode:

    @classmethod
    def make(cls,tables):
        if tables is None or len(tables) < 1:
            return None
        script = list()
        for x, y in tables.items():
            script += cls.do_table(x, y)
        return script

    @classmethod
    def do_table(cls, table_name, fields):
        if table_name is None or len(table_name) < 1:
            return None
        scripts = list()
        if_del = ' drop table if exists `%s` ' % table_name
        s1 = ' create table `%s` ( ' % table_name
        s2 = ''
        for x in fields:
            s2 += ' `%s` %s, ' % (x['name'].strip(), x['type'])
        s2 = s2.strip()[:-1]
        s3 = ')'
        scripts.append(if_del)
        scripts.append(s1 + s2 + s3)
        return scripts

