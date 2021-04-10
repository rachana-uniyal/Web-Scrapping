from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv


class Scrapper:

	def __init__(self, drugs):
		self.drugs = drugs
		self.urls = []
		self.productLinks = []


    # get urls of each drug category
	def getUrls(self):
		for drug in self.drugs:
			tempUrls = drug.find_all('a')

			for temp in tempUrls:
				self.urls.append(temp.get('href'))

	# accessing urls to get drug pages and then getting urls corresponding to each medicine
	def getPages(self):
		for url in self.urls:
			try:
				data = requests.get(url).text
				page = BeautifulSoup(data, 'lxml')
				productList = page.find_all('li', class_='product-item')
			except:
				continue

			
			for product in productList:
				productPage = product.find_all('a')

				for page in productPage:
					self.productLinks.append(page.get('href'))
			
	# extracting details of each medicine present in the website
	def getProductDetails(self):

		fields = [['Name','Category','Composition','Mfr','Country','MRP','Best_Price']]
		
		
		No_Of_Entries = 1
		entries = []

		# name of csv file 
		filename = "MedicineData.csv"
		csvfile = open(filename, 'a')


		# Setting Up The Columns name in CSV File

		# creating a csv writer object 
		csvwriter = csv.writer(csvfile) 
		# writing the data rows 
		csvwriter.writerows(fields)


		for link in self.productLinks:

			entry = []
			try:
				data = requests.get(link).text
				page = BeautifulSoup(data, 'lxml')
			except:
				continue

			try:
				dt = page.find('div', class_='product-detail')
				ess = page.find('div', class_='essentials')
			except:
				continue
			
			try:	
				name = dt.find('h1').text
				entry.append(name)
			except:
				entry.append('NA')

			try:
				category = (dt.find('span').text)
				entry.append(category)
			except:
				entry.append('NA')

			try:
				composition = dt.find('div', class_='drug-manu').text
				entry.append(composition.strip())
			except:
				entry.append('NA')

			try:
				mfr = ess.find('a').text
				entry.append(mfr)
			except:
				entry.append('NA')

			try:
				country = ess.find('span', class_='drug-manu ellipsis origin_text').text
				entry.append(country.split(':')[-1].strip())
			except:
				entry.append('NA')

			try:
				mrp = ess.find('span', class_='price').text
				mrp = mrp.split(' ')[-1]
				entry.append(mrp[1:])
			except:
				entry.append('NA')

			try:
				best_Price = ess.find('span', class_='final-price').text
				entry.append(best_Price.split()[-1])
			except:
				entry.append('NA')

			entries.append(entry)

			if No_Of_Entries % 100 == 0:

				# creating a csv writer object 
				csvwriter = csv.writer(csvfile) 
				        
				# writing the data rows 
				csvwriter.writerows(entries)

				entries = []

			print("No Of Entries : ",No_Of_Entries)
			No_Of_Entries = No_Of_Entries + 1


# get html page of link 'https://www.netmeds.com/prescriptions'
home_page = requests.get('https://www.netmeds.com/prescriptions').text
soup = BeautifulSoup(home_page , 'lxml')

# find drug categories
drugs = soup.find_all('ul', class_='alpha-drug-list')	


medicineScrapper = Scrapper(drugs)
medicineScrapper.getUrls()
medicineScrapper.getPages()
medicineScrapper.getProductDetails()

