
class DaoCode:


    @classmethod
    def t(cls,string, n=0, n2=0):
        s1 = ''
        s2 = ''
        for x in range(n):
            s1 += '\t'
        for x in range(n2):
            s2 += '\n'
        return '\n' + s1 + string + s2

    @classmethod
    def make (cls, table_name, fileds, id_name, id_type, path):
        if fileds is None or len(fileds) < 0:
            return None
        class_name = table_name.capitalize() + 'Dao'
        pojo_name = 'Tb'+table_name.capitalize()

        class_imp = cls.t('/*create by gz*/')
        class_imp += cls.t('package %s.dao;' % path)
        class_imp += cls.t('import java.util.List;')
        class_imp += cls.t('import org.apache.ibatis.annotations.Insert;')
        class_imp += cls.t('import org.apache.ibatis.annotations.Select;')
        class_imp += cls.t('import org.apache.ibatis.annotations.Delete;')
        class_imp += cls.t('import org.apache.ibatis.annotations.Update;')
        class_imp += cls.t('import %s.%s;' % (path + '.pojo', pojo_name))
        class_imp += cls.t('import org.springframework.stereotype.Repository;', 0, 1)
        
        class_def = cls.t('@Repository("%s")' % (table_name + 'Dao'))
        class_def += cls.t('public interface %s {' % (class_name))

        class_end = cls.t('}')

        class_body = cls.t(('@Select("select * from %s ")' % table_name), 1)
        class_body += cls.t('public List<%s> selects() throws Exception;' % pojo_name, 1, 1)
        class_body += cls.t('@Select("select * from %s where %s=#{%s}")' % (table_name, id_name, id_name), 1)
        class_body += cls.t('public %s selectById(%s %s) throws Exception;' % (pojo_name, id_type, id_name), 1, 1)
        class_body += cls.t('@Delete("delete from %s where %s=#{%s}")' % (table_name, id_name, id_name), 1)
        class_body += cls.t('public Boolean delete(%s %s) throws Exception;' % (id_type, id_name), 1, 1)

        t_str1 = ''
        t_str2 = ''
        for y in fileds:
            t_str1 += y['name'] + ','
            t_str2 += '#{%s},' % (y['name'])
        t_str1 = t_str1[:-1]
        t_str2 = t_str2[:-1]

        class_body += cls.t('@Insert("insert into %s(%s) values(%s)")' % (table_name, t_str1, t_str2), 1)
        class_body += cls.t('public Boolean insert(%s %s) throws Exception;' % (pojo_name,table_name), 1, 1)

        t_str3 = ''
        for y in fileds:
            t_str3 += (' %s=#{%s},'%(y['name'],y['name']))
        t_str3=t_str3[:-1]

        class_body += cls.t('@Update("update %s set %s where %s=#{%s}")' % (table_name, t_str3, id_name, id_name), 1)
        class_body += cls.t('public Boolean update(%s %s) throws Exception;' % (pojo_name, table_name), 1, 1)

        return class_imp+class_def+class_body+class_end

if __name__ == '__main__' :
    b = DaoCode()
    print(DaoCode.make('table',[{'name':'f1','type':'String'}],'f1','String', 'com.gz'))
