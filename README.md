# But du projet : 
Répondre à une problématique d'analyse de marché sur le [site](https://books.toscrape.com/index.html) grâce à Python.

# Contexte du projet : 
Un client m'a contacté afin de créer un script qui permet d'extraire certaines informations sur les livres du site par catégorie.

# Statut du projet : 

| Fonction | Avancement |
| ------ | ------ |
| Récupération du code HTML de l'ensemble des pages| **Terminé**  |
| Parsing des données HTML avec *BeautifulSoup* | **Terminé** |
| Téléchargement d'images avec *requests* dans un dossier d'output spécifié| **Terminé** |
| Sauvegarde des informations de chaque article dans des fichiers *csv*  organisés par catégories dans un dossier d'output spécifié | **Terminé** |


# Environnement de développement : 				
`Python 3.9.5`

# Méthode utilisée : 
Scraping.

# Le script permet :

* De récupérer **le titre**,**l'image**, **le prix**, **le code universel produit**, **le nombre d'étoiles**, **la quantité en stock**, **la catégorie**, **l'url** et **la description** de chaque livre dans chaque catégorie du site. Ces informations sont extraites dans des fichiers csv (1 par catégorie), dans un dossier.
* De récupérer l'image de chaque livre du site et de la mettre dans un dossier.

# Instruction d’installation et d’utilisation : 
Le script doit être télécharger et lancer dans le dossier de destinations de tous les extracts. 
Le dossier contenant l'image de chaque livre et celui contenant les csv de chaque catégorie seront créés au même endroit que la ou le script sera lancé.

# Ce que j'ai appris : 
Le web scraping permet via un script, l'extraction du contenu d'un site Web. Certaines informations sont extraites puis étudiées dans un autre contexte, par exemple pour le référencement ou l'étude de la concurrence.