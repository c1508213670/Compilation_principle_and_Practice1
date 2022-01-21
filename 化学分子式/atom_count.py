#! /usr/bin/env python
#coding=utf-8
import ply.yacc as yacc
from calclex import tokens

# 识别分子式
# 分子式 : 更细分的分子式 + 分子
#       | 分子
def p_species_list(p):
    '''species_list :  species_list species
                    |  species             '''
    if(len(p)==3):
        p[0]=p[1]+p[2]
    else:
        p[0]=p[1]

# 识别分子
# 分子 : 原子 + 数量
#     | 原子
def p_species(p):
    '''species :  SYMBOL NUMBER
               |  SYMBOL       '''
    if(len(p)==3):p[0]=p[2]
    else:p[0]=1


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")


# Build the parser
parser = yacc.yacc()

def atom_count(ATOM):
    atomcount=parser.parse(ATOM)
    print("atomcount("+ATOM+")="+str(atomcount))
    return atomcount

atom_count("He")
atom_count("H2")
atom_count("H2SO4")
atom_count("CH3COOH")
atom_count("NaCl")
atom_count("C60H60")

