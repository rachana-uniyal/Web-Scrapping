from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

urls = []
product_links = []


def get_urls(drugs):
	for drug in drugs:
		temp_urls = drug.find_all('a')

		for temp in temp_urls:
			urls.append(temp.get('href'))


def get_pages(urls):
	for url in urls:
		data = requests.get(url).text
		page = BeautifulSoup(data, 'lxml')
		product_list = page.find_all('li', class_='product-item')
		

		
		for product in product_list:
			product_page = product.find_all('a')

			for page in product_page:
				product_links.append(page.get('href'))


def get_product_details(product_links):


	df = pd.DataFrame(columns=['Name','Category','Composition','Mfr','Country','MRP','Best_Price'])
	
	for link in product_links:

		Name = []
		Category = []
		Composition = []
		Mfr = []
		Country = []
		MRP = []
		Best_Price = []

		data = requests.get(link).text
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



home_page = requests.get('https://www.netmeds.com/prescriptions').text
soup = BeautifulSoup(home_page , 'lxml')
drugs = soup.find_all('ul', class_='alpha-drug-list')	
get_urls(drugs)

get_pages(urls)

get_product_details(product_links)


