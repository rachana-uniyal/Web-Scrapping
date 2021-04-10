from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd

Name = []
Category = []
Composition = []
Mfr = []
Country = []
MRP = []
Best_Price = []

df = pd.DataFrame(columns=['Name','Category','Composition','Mfr','Country','MRP','Best_Price'])

data = requests.get('https://www.netmeds.com/prescriptions/hexilak-gel-20gm').text
page = BeautifulSoup(data, 'lxml')
dt = page.find('div', class_='product-detail')
ess = page.find('div', class_='essentials')
	
name = dt.find('h1').text
Name.append(name)

category = (dt.find('span').text)
Category.append(category)

composition = dt.find('div', class_='drug-manu').text
Composition.append(composition.strip())

mfr = ess.find('a').text
Mfr.append(mfr)

country = ess.find('span', class_='drug-manu ellipsis origin_text').text
Country.append(country.split(':')[-1].strip())


mrp = ess.find('span', class_='price').text
mrp = mrp.split(' ')[-1]
MRP.append(mrp[1:])

best_Price = ess.find('span', class_='final-price').text
Best_Price.append(best_Price.split()[-1])

df=pd.DataFrame(Name,columns=['Name'])
df['Category'] = Category
df['Composition'] = Composition
df['Mfr'] = Mfr
df['Country'] = Country
df['MRP in Rs'] = MRP
df['Best_Price in Rs'] = Best_Price

df.to_csv('Medicins.csv')
