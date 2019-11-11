import ply.lex as lex
import ply.yacc as yacc
import sys

#ejemplo del lenguaje
#retiro -t 'visa' -n 1234 5432 4567 5432 -c 4567 -cant 50 -comp 'digital'
#consulta -t 'visa' -n 1234 5432 4567 5432 -c 4567 -op 'saldo'

reserved = {
    'retiro' : 'RETIRO',    'consulta': 'CONSULTA',
    'digital':'DIGITAL',
    'impreso': 'IMPRESO',
    't': 'TIPO',
    'n': 'NUMTARJETA',
    'c': 'CLAVEP',
    'cant': 'CANTIDAD',
    'op': 'OPCION',
    'comp': 'COMPROBANTE'
}

tokens = [
   # 'OPCION',
    'GUION',
   # 'PARAMETRO',
    'APOST',
    'CADENA',
    'CLAVE',
    'ENTERO'
    #'VALOR'

   
]

tokens += reserved.values()


t_GUION=r'\-'
t_APOST=r'\''
t_ignore= r' '

'''
def t_OPCION(t):
    r'retiro | consulta'
    
    return t
'''

''''
def t_PARAMETRO(t):
    r't | c | cant | op |comp'
    return t
'''

def t_CADENA(t):
    r'[a-zA-Z_][\w_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t

def t_ENTERO(t):
    r'\d+'
    t.value=int(t.value)
    return t

def t_CLAVE(t):
    r'\d\d\d\d'
    '''
    print(len(t.value))
    size=len(str(t.value))
    if size>4:
        t_ENTERO(t)
    elif size == 4: 
        print("a")
        t.value=int(t.value)
        return t
    '''
    return t




def t_error(t):
    print ("Illegal character '%s'" % t.value[0])
    

# Build the lexer
lex.lex()

# Get the input
data = input("Bienvenidos al ATM UTEPITO ingrese su solicitud \n")

lex.input(data)

# Tokenize
while 1 :
        tok = lex.token()
        if not tok :
                break
        print (tok)
