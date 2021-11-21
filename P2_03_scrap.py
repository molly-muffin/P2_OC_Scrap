##############
# LIBRAIRIES #
##############

from bs4 import BeautifulSoup
import requests
import re
import sys
import os
import shutil
import time


#############
# VARIABLES #
#############

url    = 'https://books.toscrape.com/'
file_category = "_save_data.csv"
directory_category = "P2_02_save_data/"
directory_img = "P2_01_save_img/"

#############
# FONCTIONS #
#############

# Trouver les liens vers chaque catégorie
def get_categories(url):
	r = requests.get(url)
	categories = {}
	soup = BeautifulSoup(r.content, 'html.parser')
	ul_navlist = soup.find("ul", class_="nav-list")
	ul_categories = ul_navlist.find("ul")
	i = 1
	for li_category in ul_categories.find_all("li"):
		i = i + 1
		a_category = li_category.find("a")
		name = "%s%s%s" % (a_category.text.replace("\n","").strip(), "_", i)
		url  = a_category["href"]
		categories[name] = url
	return categories

# Trouver le nombres de page pour chaque catégorie
def get_total_pages_and_get_all(category, url):
	url_page = "%s/catalogue/category/books/%s/index.html" % (url, category.lower())
	r = requests.get(url_page)
	soup = BeautifulSoup(r.content, "html.parser")
	category_htmlcode = ""
	if soup.find("li",  class_="current") == None:
		r = requests.get('%s/catalogue/category/books/%s/index.html' % (url, category.lower()))
		category_htmlcode =  str(r.content)
		time.sleep(1)
	else:
		pages = int(str(soup.find("li",  class_="current")).replace('<li class="current">', "").replace("</li>", "").replace("\n", "").replace("Page 1 of", "").strip())
		for page in range(1, int(pages)+1):
			r = requests.get('%scatalogue/category/books/%s/page-%d.html' % (url, category.lower(), page))
			category_htmlcode =  str(category_htmlcode) + str(r.content)
			time.sleep(1)
	return category_htmlcode

# Trouver les liens de chaque livres pour une catégorie
def parse_articles_url_category(category_htmlcode):
	url_list = []
	soup = BeautifulSoup(category_htmlcode, 'html.parser')
	all_articles = soup.find_all("article")
	for article in all_articles:
		links = article.find("a")
		article_url = url + "catalogue/" + links["href"].replace("../","")
		url_list.append(article_url)
	return url_list

# Parser la page de chaque livre
def request_article_category(article_url):
	r = requests.get(article_url)
	return r.content 

# Trouver les informations pour chaque livre 
def parse_article(data):
	article_data = {}
	soup = BeautifulSoup(data, 'html.parser')

	title = (soup.find("h1").text)
	article_data["title"] = title

	img = soup.find("img")["src"].replace("../","")
	img_url = str(url) + str(img)
	article_data["img"] = img_url

	price = (soup.find("p", class_="price_color").text)
	article_data["prix"] = price

	upc = (soup.find("td").text)
	article_data["upc"] = upc

	category = (soup.find("ul", class_="breadcrumb").contents[5].find("a").text)
	article_data["category"] = category	

	try: 
		description = (soup.find(id="product_description").find_all_next()[1].text)
	except:
		description = ""
	article_data["description"] = description

	star = soup.find("p", class_="star-rating")["class"][1]
	article_data["etoile"] = star

	stock = (soup.find("p", class_="availability").text.replace("\n",""))
	if "In stock" in stock:
		article_data["stock"] = re.search('\d+', stock).group(0)
	else:
		article_data["stock"] = 0

	return article_data

# Stocker les informations receuillis dans un dictionnaire 
def save_data(article_data, category):
	f = open("%s%s%s" % (directory_category, category.split("_")[0], file_category), "a", encoding = "utf_8")
	article_data["description"] = article_data["description"].replace(' "','\"').replace('" ','\"').replace(' " ','\"') 
	data = '"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";"%s";\n' % (article_data["title"],article_data["img"],article_data["prix"],article_data["upc"],article_data["etoile"],article_data["stock"],article_data["category"],article_data["url"],article_data["description"])
	f.write(data)
	f.close()

# Créer un dossier pour y mettre les fichiers csv
def create_directories():
	os.makedirs(directory_category, exist_ok = True)
	os.makedirs(directory_img, exist_ok = True)

# Créer un fichier pour une catégorie 
def create_file(category):
	try:	
		f = open("%s%s%s" % (directory_category, category.split("_")[0], file_category), "w", encoding = "utf_8")
		data = "TITLE;IMG;PRIX;UPC;ETOILE;STOCK;CATEGORY;URL;DESCRIPTION\n"
		f.write(data)
		f.close()
	except PermissionError: 
		print("Erreur d'accès au fichier csv")

# Récupérer le nombre de page et le contenu de toutes mes pages
def get_all_pages():
	pages_htmlcode = ""
	r = requests.get(url)
	soup = BeautifulSoup(r.content, "html.parser")	
	pages = int(str(soup.find("li",  class_="current")).replace('<li class="current">', "").replace("</li>", "").replace("\n", "").replace("Page 1 of", "").strip())
	for page in range(1, int(pages)+1):
		print("Récupération des informations de la page n°%d sur %d.." % (page, pages))
		r = requests.get('%s/catalogue/page-%d.html' % (url, page))
		pages_htmlcode = str(pages_htmlcode) + str(r.content)
		time.sleep(1)
	return pages_htmlcode

# Importer les images des livres dans un dossier 
def import_img(url_img):
	r = requests.get(url_img["img"], stream = True)
	if r.status_code == 200:
		filename = "%s%s" %(directory_img, url_img["title"])
		filename = filename[:150] + str(".jpg")
		with open(filename, "wb") as f:
			r.raw.decode_content = True
			shutil.copyfileobj(r.raw, f)

########
# MAIN #
########

def main():
	print("Création des dossiers..")
	create_directories()
		
	print("Récupération des pages..")
	categories = get_categories(url)
	for category in categories:
		print("Récupération de %s.." % (category.split("_")[0]))
		category_htmlcode = get_total_pages_and_get_all(category, url)
		print("Récupération des liens de chaque livre..")
		links = parse_articles_url_category(category_htmlcode)
		create_file(category)	
		print("Récupération des articles..")
		i = 0
		links_number = (len(links))
		for article_url in links:
			i = i + 1
			print("Traitement article %d sur %d" % (i, links_number))
			data = request_article_category(article_url)
			article_data = parse_article(data)
			article_data["url"] = article_url
			save_data(article_data, category)
			time.sleep(1)

	print("Récupération des images..")
	all_pages_htmlcode = get_all_pages()

	soup = BeautifulSoup(all_pages_htmlcode, 'html.parser')
	img_number = (len(soup.find_all("article", class_= "product_pod")))
	i = 0
	for article in soup.find_all("article", class_= "product_pod"):
		i = i + 1
		print("Récupération de l'image n°%d sur %d" % (i, img_number))
		img = article.find("img")["src"]
		img = ("%s%s" % (url, img.replace("../", ""))) 
		title = article.find("img")["alt"]
		title_ok = ""
		for char in title:
			if char.isalnum():
				title_ok = title_ok + char
		url_img = {"img":img, "title":title_ok}		
		import_img(url_img)

main()