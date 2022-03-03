#%%
#imports
from multiprocessing import Condition
from pydoc import describe
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

#%%
url = 'https://www.vivareal.com.br/venda/alagoas/maceio/apartamento_residencial/?pagina={}'


#%%
i=1
ret = requests.get(url.format(i))
soup = bs(ret.text)

#%%
#Quantidade da pesquisa/Iniciar Data Frame
qtd_houses = float(soup.find('strong',{'class' : 'results-summary__count'}).text.replace('.',''))

df = pd.DataFrame( columns=['Descricao', 'Endereco', 'Area', 'Quartos', 'WC', 'Vagas',
                            'Valor', 'Condominio', 'Link'])

i = 0
# %%
while qtd_houses > df.shape[0]:
    i +=1
    print(f"valor i: {i} \t\t qtd_imoveis: {df.shape[0]}" )
    ret  = requests.get(url.format(i))
    soup = bs(ret.text)
    houses = soup.find_all('a',{'class':'property-card__content-link js-card-title'})
    for house in houses:
        try:
            descri  = house.find('span',{'class': 'property-card__title'}).text.strip()
        except:
            descri  = None
        try:
            endr    = house.find('span',{'class'  : 'property-card__address'}).text.strip()
        except:
            endr    = None
        try:
            area    = house.find('span',{'class'  : 'js-property-card-detail-area'}).text.strip()
        except:
            area    = None
        try:
            quartos = house.find('li',{'class'  : 'property-card__detail-room'}).span.text.strip()
        except:
            quartos = None
        try:
            wc      = house.find('li',{'class'  : 'property-card__detail-bathroom'}).span.text.strip()
        except:
            wc      = None
        try:
            vagas   = house.find('li',{'class'  : 'property-card__detail-garage'}).span.text.strip()
        except:
            vagas   = None
        try:
            valor   = house.find('div',{'class': 'property-card__price'}).p.text.strip()
        except:
            valor   = None
        try:
            condo   = house.find('strong',{'class': 'js-condo-price'}).text.strip()
        except:
            condo   = None
        try:
            direc   = 'https://www.vivareal.com.br' + house['href']
        except:
            direc   = None
        
        df.loc[df.shape[0]] = [descri, endr, area, quartos, wc, vagas, valor, condo, direc]


# %%
df.to_csv('banco_de_imoveis.csv', sep=';', index=False)

# %%
