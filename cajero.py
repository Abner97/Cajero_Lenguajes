import ply.lex as lex
import ply.yacc as yacc
import sys

#ejemplo del lenguaje
#retiro -t 'visa a' -n 1234 5432 4567 5432 -c 4567 -cant 50 -comp 'digital'
#consulta -t 'visa' -n 1234 5432 4567 5432 -c 4567 -op 'saldo'

reserved = {
    'retiro' : 'RETIRO',
    'consulta': 'CONSULTA',
    'digital':'DIGITAL',
    'impreso': 'IMPRESO',
    't': 'TIPO',
    'c': 'CLAVEP',
    'n': 'NUMEROT',
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
    'ENTERO',
    'RESERVADA'
    #'VALOR'

   
]

tokens += reserved.values()


t_GUION=r'\-'
t_APOST=r'\''
t_ignore  = ' \t'
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
    r'[a-zA-Z_]+'
    
    if t.value in reserved:
        t_RESERVADA(t)
    
    return t

def t_RESERVADA(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get( t.value, 'RESERVADA' )
    return t

def t_ENTERO(t):
    r'\d+'
    t.value=int(t.value)
    return t




def t_error(t):
    print ("Caracter Illegal '%s'" % t.value[0])
    

# Build the lexer
lexer = lex.lex()

'''
#prueba de analizdor lexico
# Get the input
data = input("Bienvenidos al ATM UTEPITO ingrese su solicitud \n")
dataPurged=data.replace(" ", "")#elimina los espacios en blanco
lex.input(dataPurged)
#print(dataPurged)
# Tokenize
while 1 :
        tok = lex.token()
        if not tok :
                break
        print (tok)
'''
def p_cajero(p):
    '''
    cajero : expression
           
    '''
    print(p[1]) 

def p_expression(p):
    '''
    expression : transaction body
    '''
    p[0]=(p[1],p[2])

def p_transaction(p):
    '''
    transaction : RETIRO
                | CONSULTA

    '''
    p[0]=p[1]

def p_body(p):
    '''
    body : parameter value body
         | parameter value empty
    '''
    p[0]=(p[1],p[2],p[3])

def p_parameter(p):
    '''
    parameter : GUION TIPO
              | GUION CLAVEP
              | GUION NUMEROT
              | GUION CANTIDAD
              | GUION OPCION
              | GUION COMPROBANTE
    '''
    p[0]=(p[1],p[2])

def p_value(p):
    '''
    value : ENTERO
          | cadenaApost
          
    '''
    p[0]=p[1]

def p_cadenaApost(p):
    '''
    cadenaApost : APOST CADENA APOST
                | APOST DIGITAL APOST
                | APOST IMPRESO APOST
    '''
    p[0]=p[2]


def p_empty(p):
    '''
    empty :
    '''
    p[0]=None
def p_error(p):
    print ("Sintax error",p)

parser = yacc.yacc()


while True:
    try:
        s = input('')
        dataPurged=s.replace(" ", "")
    except EOFError:
        break
    parser.parse(dataPurged)