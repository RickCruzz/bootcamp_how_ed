#%%
import selenium
import time
import sys
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#%%
#ator = sys.argv[1]
ator = 'Nicolas Cage'
#%%
#criar Sessão
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(30)
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')
# %%
#loading table
tabela = driver.find_element_by_xpath('//*[@id="mw-content-text"]/div[1]/table[2]')
print('carregado e arquivo sera criado')
#%%
df = pd.read_html('<table>' + tabela.get_attribute('innerHTML') + '</table>')[0]

#%%
with open('print.png', 'wb') as f:
    f.write(driver.find_element_by_xpath('/html/body/div/div/div[1]/div[2]/main/div[2]/div[3]/div[1]/table[1]/tbody/tr[2]/td/div/div/div/a/img').screenshot_as_png)

# %%
arquivo = ator+'.csv'
df.to_csv(arquivo, sep=';', index=False)
#driver.close()
# %%
