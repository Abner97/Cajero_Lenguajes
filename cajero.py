import ply.lex as lex
import ply.yacc as yacc
import sys
from random import seed
from random import random
import subprocess as sp

#ejemplo del lenguaje
#retiro -t 'visa a' -n 1234 5432 4567 5432 -c 4567 -cant 50 -comp 'digital'
#consulta -t 'visa' -n 1234 5432 4567 5432 -c 4567 -op 'saldo'
cont = 0
seed(1)
reserved = {
    'retiro' : 'RETIRO',
    'consulta': 'CONSULTA',
    'digital':'DIGITAL',
    'impreso': 'IMPRESO',
    'visa':'VISA',
    'mastercard':'MSCARD',
    'americanexpress':'AMERICANEXP',
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

def p_cajero(p):#p[0]
    '''
    cajero : expression
           
    '''
    print(run(p[1])) 


def p_expression(p):#p[1]
    '''
    expression : transaction body
    '''
    p[0]=(p[1],p[2])

def p_transaction(p):#p[0]
    '''
    transaction : RETIRO
                | CONSULTA
    '''
    p[0]=p[1]

def p_body(p):#p[1]
    '''
    body : parameter value body
         | parameter value empty
    '''
    p[0]=(p[1],p[2],p[3])

def p_parameter(p):#p[1][0]
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
                | APOST VISA APOST
                | APOST MSCARD APOST
                | APOST AMERICANEXP APOST
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


def retiro(numero,tarjeta,monto,comprobante):
    tmp = sp.call('clear',shell=True)
    global cont
    print("Usted está retirando $",monto)
    cont = cont + 1
    if comprobante=="digital":

        print("Tarjeta: ",tarjeta," ","#",numero,"\n")
        print("Monto a retirado: $",monto,"\n")
        print("Transaccion #",cont)
    elif comprobante =="impreso":
        print("Retire su comprobante")

def consulta(tarjeta,numero,opcion):
    tmp = sp.call('clear',shell=True)
    value = random()
    scaled_value = 0 + (value * (10000 - 0))
    
    if opcion == "saldo":
        print("usted tiene un saldo de $",scaled_value)
    elif opcion == None or opcion!='saldo':
        print("Error porfavor introduzca una opcion valida")
    
        


def run(p):
    
    if p[0]=='retiro':
        retiro(tarjeta=p[1][1],numero=p[1][2][1],monto=p[1][2][2][2][1],comprobante=p[1][2][2][2][2][1])

    elif p[0]=='consulta':
        consulta(tarjeta=p[1][1],numero=p[1][2][1],opcion=p[1][2][2][2][1])


            
#tarjeta p[1][1]
#numero p[1][2][1]
#clave p[1][2][2][1]
#canridad p[1][2][2][2][1]
#comprobante p[1][2][2][2][2][1]
while True:
    try:
        s = input('')
        dataPurged=s.replace(" ", "")
    except EOFError:
        break
    parser.parse(dataPurged)