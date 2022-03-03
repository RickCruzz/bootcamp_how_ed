#%%
import selenium
import sys 
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#%%
cep = sys.argv[1]
if cep:
    #Acesso ao site da How
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #driver.get('https://howedu.com.br')

    # %%
    #Preenchimento Formulário
    driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
    elem_cep = driver.find_element_by_name('endereco')
    elem_mod = driver.find_element_by_name('tipoCEP')

    #%%
    #elem_mod.value('ALL')
    elem_cep.clear()
    elem_cep.send_keys(cep)
    elem_mod.click()
    driver.find_element_by_xpath('//*[@id="formulario"]/div[2]/div/div[2]/select/option[1]').click()

    # %%
    #Pesquisar
    driver.find_element_by_id('btn_pesquisar').click()
    # %%

    logradouro = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr[1]/td[1]').text
    bairro = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr[1]/td[2]').text
    localidade = driver.find_element_by_xpath('//*[@id="resultado-DNEC"]/tbody/tr[1]/td[3]').text

    # %%
    print(""" Para o CEP: {}
    Endereco: {}
    Bairro: {}
    Localidade: {}
    CEP: {}
    """.format(cep, logradouro, bairro, localidade, cep))
    
# %%
