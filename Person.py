__author__ = 'Simone'

class Person:


    def __init__(self,name,surname,age):
        self.__name=name
        self.__surname=surname
        self.__age=age

    def print(self):
        print("name = " + self.__name + "; surname = " + self.__surname + "; age = " + str(self.__age))

    def getName(self):
        return self.__name

    def getSurname(self):
        return self.__surname

    def getAge(self):
        return self.__age

    def toTuple(self):
        return (self.__name,self.__surname,self.__age)