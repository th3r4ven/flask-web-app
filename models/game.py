class Game:
    def __init__(self, title, category, console, id=None):
        self.__id = id
        self.__title = title
        self.__category = category
        self.__console = console

    @property
    def id(self):
        return self.__id

    @property
    def title(self):
        return self.__title

    @property
    def category(self):
        return self.__category

    @property
    def console(self):
        return self.__console



