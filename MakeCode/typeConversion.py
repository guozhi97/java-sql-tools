
class TypeConversion:

    __dict_dir = 'MakeCode/jdbc_java_type.txt'
    __dict_data = dict()

    def __init__(self):
        data = None
        try:
            f = open(self.__dict_dir,'r')
            try:
                data = f.read()
            finally:
                f.close()
        except Exception as e:
            print("read " + self.__dict_dir + "file error!")
        if data is None:
            print('read '+self.__dict_dir+' error')
            return
        for x in data.split('\n'):
            arr = x.split('\t')
            if arr is None or len(arr) < 2:
                continue
            self.__dict_data[str(arr[0])] = arr[1]

    def debug(self):
        print(self.__dict_data)

    def get(self, type_name):
        if type_name is None or len(type_name) < 1:
            print("type is none or '' ")
            return 'String'
        type_name = str.strip(type_name)
        if type_name in self.__dict_data.keys():
            return self.__dict_data[str(type_name)]
        else:
            print("havan't this type :"+type_name)
            return 'String'

if __name__ == '__main__':
    t = TypeConversion()
    t.debug()
    print(t.get('int'))