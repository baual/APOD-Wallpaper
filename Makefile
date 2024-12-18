#!make
lieu = ${HOME}/.APOD

init:
	pip3 install -r requirements.txt
	sudo apt-get install feh -y
#copie les fichiers utiles
	mkdir $(lieu)
	cp ${PWD}/apodwallpaper.* $(lieu)

config:
#modifie le fichier qui va servir au service
	sed -i 's|ExecStart=.*|ExecStart=python3 $(lieu)/apodwallpaper.py|g' $(lieu)/apodwallpaper.service

.ONESHELL:
setup:
	sudo cp ~/.APOD/apodwallpaper.service /etc/systemd/user/
	sudo chmod 644 /etc/systemd/user/apodwallpaper.service
	systemctl --user daemon-reload
	systemctl --user enable apodwallpaper.service

run:
	python3 $(lieu)/apodwallpaper.py

install: init config setup

uninstall:
#je n'enlève que le service, les fichiers peuvent etre supprimés à la et les dépendances de Python et feh
#utilisés par d'autres

#enleve toute notion de service
	systemctl stop apodwallpaper.service
	systemctl disable apodwallpaper.service
	sudo rm /etc/systemd/system/apodwallpaper.service
	sudo rm /etc/systemd/system/apodwallpaper.service # and symlinks that might be related
#	sudo rm /usr/lib/systemd/system/apodwallpaper.service 
#	sudo rm /usr/lib/systemd/system/apodwallpaper.service # and symlinks that might be related
	systemctl daemon-reload
	systemctl reset-failed

.PHONY: 
	init, config, setup, run, uninstall
