class ModelMetaclass(type):
    def __new__(cls,class_name,class_parents,class_attrs):
        maping = {}
        for k,v in class_attrs.items():
            if isinstance(v,tuple):
                maping[k] = v
        for k in maping.keys():
            class_attrs.pop(k)
        class_attrs['__mappings__'] = maping
        class_attrs['__table__'] = class_name
        return type.__new__(cls,class_name,class_parents,class_attrs)
 # __mappings__ = {
    #     "uid": ('uid', "int unsigned")
    #     "name": ('username', "varchar(30)")
    #     "email": ('email', "varchar(30)")
    #     "password": ('password', "varchar(30)")
    # }
    # __table__ = "User"
class Model(object, metaclass=ModelMetaclass):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

    def save(self):
        fields = []
        args = []
        for k, v in self.__mappings__.items():
            fields.append(v[0])
            args.append(getattr(self, k, None))

        args_temp = list()
        for temp in args:
            # 判断入如果是数字类型
            if isinstance(temp, int):
                args_temp.append(str(temp))
            elif isinstance(temp, str):
                args_temp.append("""'%s'""" % temp)
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(args_temp))
        print('SQL: %s' % sql)

class User(Model):
    uid = ('uid', "int unsigned")
    name = ('username', "varchar(30)")
    email = ('email', "varchar(30)")
    password = ('password', "varchar(30)")

u = User(uid=12345, name='Michael', email='test@orm.org', password='my-pwd')

u.save()