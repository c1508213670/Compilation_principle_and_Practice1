#coding=utf-8
import ply.lex as lex

# List of token names.   This is always required
tokens = (
    'NUMBER',#识别分子式后的数量
    'SYMBOL',#识别原子
)

# Regular expression rules for simple tokens
t_SYMBOL = (#正则表达式识别化学元素
    r"C[laroudsemf]?|Os?|N[eaibdpos]?|S[icernbmg]?|P[drmtboau]?|"
    r"H[eofgas]?|A[lrsgutcm]|B[eraik]?|Dy|E[urs]|F[erm]?|G[aed]|"
    r"I[nr]?|Kr?|L[iaur]|M[gnodt]|R[buhenaf]|T[icebmalh]|"
    r"U|V|W|Xe|Yb?|Z[nr]")

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Error handling rule
def t_error(t):
    print("Illegal character",end=" " )
    print(t.value[0])
    t.lexer.skip(1)

## Build the lexer
lexer = lex.lex()

