import urllib.request as request
import urllib.parse as UrlParse


# Ouvrir une URL
response = request.urlopen('https://www.tresfacile.net/')
 
# Lire le contenu de la réponse
content = response.read()
 
# Afficher le contenu
print(content) # affiche le conenu html de la pge demandée


#exemple suivre les redirections
import urllib.request
 
# Configuration de l'opener pour suivre les redirections
opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler())
 
# Exemple d'ouverture d'une URL avec redirection
response = opener.open('http://www.tresfacile.net')
final_url = response.url
print(final_url)


#recupérer un fichier
import urllib.request
 
url = 'https://www.tresfacile.net/wp-content/uploads/2022/08/miniature-les-briques-de-bases-en-langage-python.png'
filename = './Tests/fichier.png'
 
urllib.request.urlretrieve(url, filename)
#print('Le fichier a été téléchargé avec succès.')
