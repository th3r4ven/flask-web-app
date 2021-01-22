class User(object):

    def __init__(self, id, name, passwd):
        self.__id = id
        self.__name = name
        self.__passwd = passwd

    @property
    def name(self):
        return self.__name

    @property
    def id(self):
        return self.__id

    def do_login(self, name, passwd):
        return self.__name == name and self.__passwd == passwd