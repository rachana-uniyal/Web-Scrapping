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





	        




home_page = requests.get('https://www.netmeds.com/prescriptions').text
soup = BeautifulSoup(home_page , 'lxml')
drugs = soup.find_all('ul', class_='alpha-drug-list')	
get_urls(drugs)

get_pages(urls)




