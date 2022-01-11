# -*- coding: utf-8 -*-
"""
Created on Sun Jan  2 17:03:48 2022

@author: unily
"""

import pandas as pd
from datetime import date
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Arrancando el webdriver:
options = Options()
options.add_argument("--lang=es")
from webdriver_manager.chrome import ChromeDriverManager
import plotly.express as px
from plotly.offline import plot

driver = webdriver.Chrome(ChromeDriverManager().install())

headers = {
    'authority': 'https://www.walmart.com.ni',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'sec-fetch-site': 'none',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9,es-MX;q=0.8,es;q=0.7'
}

'''
URL = 'https://www.walmart.com.ni/abarrotes'
page = requests.get(URL)
# specifying a desired format of "page" using the html parser    soup = BeautifulSoup(page.text, "html.parser")
soup = BeautifulSoup(page.text, "html.parser")
Ofertas_Activas = soup.find(
    class_="vtex-search-result-3-x-totalProducts--layout pv5 ph9 bn-ns bt-s b--muted-5 tc-s tl t-action--small").text
Ofertas_Activas = int(''.join(filter(str.isdigit, Ofertas_Activas)))
print(Ofertas_Activas)
'''

#Empty list
texto = []
#items_perpage = 21
#for pages in range(1, int((Ofertas_Activas / items_perpage) + 1)):
for pages in range(1,51): #50 parece ser el max de paginas por seccion
    URL = 'https://www.walmart.com.ni/abarrotes?order=OrderByTopSaleDESC&page='+format(pages)
    print(URL)
    # conducting a request of the stated URL above:
    driver.get(URL)
#Esperando que la información esté visible y ejecutando crawler:
    time.sleep(5)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)
        element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/div/div[5]/div/div/section/div[2]/div/div/div/div[4]/div/div[2]/div/div[6]/div/div/div/div[2]/div[24]'))
        WebDriverWait(driver, 30).until(element_present)
        results = [i.text for i in driver.find_elements_by_xpath('/html/body/div[2]/div/div[1]/div/div[5]/div/div/section/div[2]/div/div/div/div[4]/div/div[2]/div/div[6]/div/div/div/div[2]/div')]            
        print(results)
        texto.append(results)
        time.sleep(1)
    except:
        break
    pass
    
    
#Procesando data descargada
# Manipulacion de listas para crear dataframe
listas = [i for sublist in texto for i in sublist]            
data = pd.DataFrame(listas)
data = data[0].str.split('\n', expand=True).dropna(thresh=3).drop_duplicates([0])
#Creando variables
data['price'] = data[1].str.extract('(\d+)').astype('int')
data['name'] = data[0].str.lower()
data['weight_grams'] = data['name'].str.\
    extract(r'((\d+(?=gr))|(\d+(?=\sgr))|(\d+(?=grs))|(\d+(?=\sgrs))|(\d+(?=\sg))|(\d+(?=g)))')[0]

data['weight_lbs'] = data['name'].str.\
    extract(r'((\d+(?=lb))|(\d+(?=\slb))|(\d+(?=lbs))|(\d+(?=\slbs))|(\d+(?=\slb))|(\d+(?=lb)))')[0]
data['weight_ml'] = data['name'].str.\
    extract(r'((\d+(?=ml))|(\d+(?=\sml))|(\d+(?=mls))|(\d+(?=\smls))|(\d+(?=\sml))|(\d+(?=ml)))')[0]

data['weight'] = data['weight_grams'].astype(float)/1000
data['weight_lb_to_kg'] = data['weight_lbs'].astype(float)/2.20462
data['weight_ml_to_kg'] = data['weight_ml'].astype(float)/1000
data['weight'] = data['weight'].fillna(data['weight_ml_to_kg'])
data['weight'] = data['weight'].fillna(data['weight_lb_to_kg'])
data['weight'] = data['weight'].round(2)

data['name'] = data['name'].str.replace('\d+', '')
data['name'] = data['name'].str.replace('- gr', '')
data['name'] = data['name'].str.replace(' gr', '')
data['name'] = data['name'].str.replace('- ml', '')
data['name'] = data['name'].str.replace(' ml', '')
data['name'] = data['name'].str.replace('-', '')
data['name'] = data['name'].str.replace('lb', '')

data['country'] = 'nic'
data['date'] = date.today()

data = data[['name','weight','price','country','date']]

## GRAPHS
# Graph 1
fig1 = px.bar(data[0:15].sort_values('price'), x='price', y="name", 
             template="simple_white", text='price',
             title= 'Fig 1. Top Selling Grocery Items (sorted by unit price)')

fig1.update_layout(showlegend=True, legend_title_text='',
                xaxis_title="Price in Local Currency Units (nominal C$)", 
                yaxis_title="",
                font_family="Arial", title_font_family="Arial Black",
                yaxis_title_font_family ="Arial Black",
                xaxis_title_font_family ="Arial Black",
                title_font_color="black",
                title_font_size=19, legend_title_font_color="black",
                legend=dict(yanchor="top", y=0.89, xanchor="right", x=1),
                )
fig1.update_traces(textposition='inside')
fig1.add_annotation(
    text="Source: author.",
    xref="x domain", yref="y domain",x=0.01, y=-0.14,showarrow=False)

plot(fig1)

fig2 = px.bar(data[0:15].sort_values('weight'), x='weight', y="name", 
             template="simple_white", text='weight',
             title= 'Fig 2. Heaviest Grocery Items')

fig2.update_layout(showlegend=True, legend_title_text='',
                xaxis_title="Weight in Kilograms", 
                yaxis_title="",
                font_family="Arial", title_font_family="Arial Black",
                yaxis_title_font_family ="Arial Black",
                xaxis_title_font_family ="Arial Black",
                title_font_color="black",
                title_font_size=19, legend_title_font_color="black",
                legend=dict(yanchor="top", y=0.89, xanchor="right", x=1),
                )
fig2.update_traces(textposition='inside')
fig2.add_annotation(
    text="Source: author.",
    xref="x domain", yref="y domain",x=0.01, y=-0.14,showarrow=False)

plot(fig2)