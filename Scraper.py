from bs4 import BeautifulSoup
import requests
import re

med_data = requests.get('https://www.netmeds.com/prescriptions').text
soup = BeautifulSoup(med_data , 'lxml')
# prescriptions = soup.find('div', class_='prescriptions_products').text
# prescriptions = prescriptions.split()

# # print(prescriptions)

# categories = []
# for i in range(len(prescriptions)):
# 	if len(prescriptions[i]) > 1 and '(' not in prescriptions[i]:
# 		categories.append(prescriptions[i])
# # print(categories)

links = []
prescriptions = soup.find_all('ul', class_='alpha-drug-list')	

# print(prescriptions)
for prescription in prescriptions:
	link = prescription.find_all('a')

	for l in link:
		links.append(l.get('href'))
	   

print(links)

# links = []

# for link in soup.find_all('a',class_='alpha-drug-list' , attrs={'href': re.compile("^https://")}):
#     links.append(link.get('href'))

# print(links)


