#Imports
import requests
import pandas as pd
import collections
import sys

#Definir para o usuário
#Url get Results
#urlcx = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/jY7LDoIwFEQ_qYOlFJaFJuVlICoI3RASjWli0YVx4ddbjQtdiN5Z3eRM5hBNOqKn8WoO48WcpvH4-HUwBF6JFAp5lWcMoqgobWTrIWQO6B2QKJH6vATghwtkMk4lj5ZAFvzXx5cT-NXfEv2JqDpxSCXjCNQF7AXMKT6BGYfeSfK3ibwVzqJcsQ0tgDUnjTWTsea235GzbTqY2t4BwEYURQ!!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'
urlcx = sys.argv[1]

#urlcx = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbwMPI0sDBxNXAOMwrzCjA0sjIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wNnUwNHfxcnSwBgIDUyhCvA5EawAjxsKckMjDDI9FQE-F4ca/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K8DBC0QPVN93KQ10G1/res/id=historicoHTML/c=cacheLevelPage/=/'

#Field Names lst_fld (Numeric Fields) lst_state (Field State)
lst_fld = sys.argv[2]
lst_state = sys.argv[3]
qtd_fld = sys.argv[4]
qtd_bolas = sys.argv[5]
fld_br = 0

try:
    fld_br = int(sys.argv[6])
except:
    fld_br = 0


#valores lotofacil
#lst_fld = 'Bola'
#lst_state = 'Cidade'
#qtd_fld = 15
#qtd_bolas = 25
#fld_br = 1
#print(str(fld_br + ' fldbr')


#Execute Get and convert to Data Frame
r = requests.get(urlcx)

df = pd.read_html(r.text)
df = df[0].copy()

df
#Result Vars
r_num    = [0]  * int(qtd_bolas) #Number of Sorted
r_comb   = [] #Combinations
r_par    = [] #Number of Pair
r_impar  = [] #Number of Odd
r_primos = [] #Number of Prime
r_state  = [] #Number of States

#Var Check States
chk_state = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
             'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
             'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']

nr_pop = []
nr_pares = []
nr_impares = []
nr_primos = []

#Check Odd Numbers
def isprimo(num):
    if num < 2: #0/1 not odd
        return False
    elif num == 2: #2 only pair odd
        return True
    elif num % 2 == 0: #Not 2 and pair not odd
        return False
    else: #last check
        for i in range (3, num // 2, 2):
            if num % i == 0:
                return False
        else:
            return True

#Inicializando Variáveis comparativas
i = 1 
while i <= int(qtd_bolas):
    nr_pop.append(i)
    if ((i % 2) == 0):
        nr_pares.append(i)
    if ((i % 2 ) > 0):
        nr_impares.append(i)
    if (isprimo(i) == True):
        nr_primos.append(i)
    i += 1

#cria lst_campos
lst_campos = []
i = 1
while i <= int(qtd_fld):
    lst_campos.append(lst_fld+str(i))
    i += 1


#Começa a Checagem
for index, row in df.iterrows():
    vlr = 0
    v_pares = 0
    v_impares = 0
    v_primos = 0
    for campo in lst_campos:
        if row[campo] in nr_pares:
            v_pares   += 1
        if row[campo] in nr_impares:
            v_impares += 1
        if row[campo] in nr_primos:
            v_primos  +=1
        r_num[row[campo]-1] += 1
    r_comb.append( str(v_pares) + ' Pares/Pair - ' + str(v_impares) + ' Impares/Odds  - ' + str(v_primos) + ' Primos/Primes' )

#Transformar para ordernar
freq_nr = []
i = 1
for i in range (len(r_num)):
    l1 = []
    l1 = [i+1, r_num[i]]
    freq_nr.append(l1)

#Order
freq_nr.sort(key=lambda tup: tup[1])    

freq_nr[0] #+sorted
freq_nr[-1] #-sorted


i = 1
txt_bls = '''Jogo Perfeito'''
while i <= int(qtd_fld):
    txt_bls += ('''\n'''+str(lst_fld)+str(i) +": " +str(freq_nr[i-1][0]))
    i += 1

counter = collections.Counter(r_comb)
resultado = pd.DataFrame(counter.items(), columns=['Combinação', 'Frequencia'])
resultado['p_freq'] = resultado['Frequencia']/resultado['Frequencia'].sum()
resultado = resultado.sort_values(by='p_freq')


#Estados
#Criando lista de estados + vencedores
if int(fld_br) == 1:
    r_state=[]
    for index, row in df.iterrows():
        tmpTx = row[lst_state]
        tmpTx = str(tmpTx).split()
        for i in range(len(tmpTx)):
            if len(tmpTx[i]) == 2:
                for inx in range (len(chk_state)):
                    tmp=chk_state[inx]
                    if tmpTx[i] == tmp:
                        r_state.append(tmp)
    
    cntstate = collections.Counter(r_state)
    rststate = pd.DataFrame(cntstate.items(), columns=['Estado', 'Frequencia'])
    rststate['p_freq'] = rststate['Frequencia']/rststate['Frequencia'].sum()
    rststate = rststate.sort_values(by='p_freq')
    txtstate = 'O Estado que mais ganhou sorteios: ' + str(rststate['Estado'].values[-1]) + ' frequencia de: '+ str(int(((rststate['p_freq'].values[-1]*100)*100))/100) + '%'

#Imprimir
print('Resultados da consulta')
#Texto bolas ganhadoras
print(txt_bls)
#Numeros/Combinação
print('''
O Número mais frequente: {}
O Número menos frequente: {}
A Combinação de Pares, Impares e Primos mais frequente: {} frequencia de: {}%
'''.format(freq_nr[-1][0], freq_nr[0][0], resultado['Combinação'].values[-1], int(((resultado['p_freq'].values[-1]*100)*100))/100) )
#Estado/%Ganhos

if int(fld_br) == 1:
    print(txtstate)