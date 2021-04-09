from bs4 import BeautifulSoup
import requests
import re

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
		# print(product_list)

		
		for product in product_list:
			product_page = product.find_all('a')

			for page in product_page:
				product_links.append(page.get('href'))


def get_product_details(product_links):

	data = requests.get(product_links[0]).text
	page = BeautifulSoup(data, 'lxml')
	dt = page.find('div', class_='product-detail').text
	ess = page.find('div', class_='essentials').text
	print(dt)
	print('**********************')
	print(ess)
	# product_details = page.find('div', class_='product-detail')
	# print(product_details)

	# for link in product_links:
	# 	data = requests.get(link).text
	# 	page = BeautifulSoup(data, 'lxml')
	# 	product_details = page.find('div', class_='product-details')
	# 	print(product_details)



	        




home_page = requests.get('https://www.netmeds.com/prescriptions').text
soup = BeautifulSoup(home_page , 'lxml')
drugs = soup.find_all('ul', class_='alpha-drug-list')	
get_urls(drugs)

get_pages(urls)

get_product_details(product_links)


