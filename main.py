__author__ = 'Simone'

from Person import  *
from postgresql import *
import sys

def main():
    p1 = Person('simone','de cristofaro',29)
    p2 = Person('chiara','fiaschetti',28)
    persons=[p1.toTuple(),p2.toTuple()]
    print(persons)
    writePersonOnDb(persons)

main()