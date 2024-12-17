# APOD-Wallpaper

## Basic Info

Il s'agit d'une refonte d'un [script original en python](https://github.com/charly98cma/apod-wallpaper) de [Charly98cma](https://github.com/Charly98cma) utilisant l'API NASA *Astronomy Picture Of the Day* ([APOD](https://apod.nasa.gov/apod/astropix.html)) pour définir l'APOD comme image de fond d'écran à chaque fois que vous exécutez le script.

Et, comme nous sommes tous assez paresseux, *systemd* lancera le script au démarrage, après avoir eu une connexion internet, il suffit de suivre les instructions ci-dessous.

## Makefile

### installer le service

``` bash
make install
```

### désinstaller le service

``` bash
make uninstall
```

### élement par élément

#### Dépendances

Vous avez besoin de [Python 3.11 minimum](https://www.python.org/), [pip](https://pypi.org/project/pip/), le programme [feh](https://feh.finalrewind.org/) (feh est installé avec apt-get dans le makefile).

``` bash
make init
```

#### Exécution du script

Pour exécuter le script manuellement, et changer le fond d'écran, il suffit de lancer la commande suivante :

``` bash
make run
```

Maintenant, pour exécuter le script après le démarrage du système, vous devez suivre quelques étapes simples :

1. Lancez `make config`, pour définir les paramètres appropriés sur *apodwallpaper.service* (chemin absolu du script Python, au cas où vous vous poseriez la question).
2. Maintenant, pour activer le service *systemd*, lancez la commande make `make setup`, qui fait et exécute ce qui suit (nécessite les permissions **sudo**) :
   1. Place le fichier de service dans */etc/systemd/user* (nécessite **sudo**)
   2. Attribuez la permission appropriée au fichier de service en exécutant `sudo chmod 644 /etc/systemd/user/apodwallpaper.service`. (nécessite **sudo**)
   3. Rechargez le démon systemd en exécutant `systemctl --user daemon-reload`
   4. Activez le service en exécutant `systemctl --user enable apodwallpaper.service`.

Et c'est tout, à partir de maintenant, après le démarrage du système, le script sera exécuté, et le fond d'écran changera.

## Références

J'utilise la **api_key** par défaut pour les requêtes APOD, car les contraintes d'utilisation sont basées sur l'IP de l'utilisateur, ce qui n'est pas un problème pour ce projet, puisque chaque utilisateur ne téléchargera l'image qu'une fois par jour. ([Github](https://github.com/nasa/apod-api))

Mais si vous souhaitez utiliser votre propre clé, vous pouvez en demander une sur le site [NASA Open APIs](https://api.nasa.gov/).
