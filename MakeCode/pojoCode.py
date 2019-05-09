

class PojoCode:

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
    def make (cls, table_name, fields, path='com'):
        if fields is None or len(fields) < 1:
            return None
        class_name = 'Tb'+table_name.capitalize()
        class_imp = '/* create by gz */'
        class_imp += cls.t('package %s.pojo;' % path)
        class_imp += cls.t('import java.io.Serializable;', 0, 1)
        class_def = cls.t('public class %s implements Serializable {' % class_name, 0, 1)
        class_end = cls.t('}')

        class_body = cls.t('public %s() {}' % class_name, 1, 1)
        class_body += cls.t('@Override', 1)
        class_body += cls.t('public String toString(){', 1)

        s1 = ''
        for x in fields :
            s1 += '%s=" + %s + ",' % (x['name'], x['name'])
        s1 = s1[:-1]

        class_body += cls.t('return "%s [ %s ]";' % (class_name, s1), 2)
        class_body += cls.t('}', 1)

        class_var = ''
        for x in fields:
            class_var += cls.t('private %s %s;' %(x['type'], x['name']), 1, 1)
            class_body += cls.t('public %s get%s() {' % (x['type'],x['name'].capitalize()), 1)
            class_body += cls.t('return %s;' % x['name'], 2)
            class_body += cls.t('}', 1, 1)
            class_body += cls.t('public void set%s( %s %s) {' % (x['name'].capitalize(), x['type'], x['name']), 1)
            class_body += cls.t('this.%s = %s;' % ( x['name'], x['name']), 2)
            class_body += cls.t('}', 1, 1)

        return class_imp+class_def+class_var+class_body+class_end

if __name__ == '__main__':
    s=PojoCode.make('tb1',[{'name':'f1','type':'String'}])
    print(s)
