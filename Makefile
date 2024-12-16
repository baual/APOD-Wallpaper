#!make
init:
	pip3 install -r requirements.txt
	sudo apt-get install feh -y
	mkdir ~/.APOD/
	cp ${PWD}/apodwallpaper.py ~/.APOD

config:
	sed -i 's|ExecStart=.*|ExecStart=python ~/.APOD/apodwallpaper.py|g' apodwallpaper.service

.ONESHELL:
setup:
	sudo cp apodwallpaper.service /etc/systemd/user/
	sudo chmod 644 /etc/systemd/user/apodwallpaper.service
	systemctl --user daemon-reload
	systemctl --user enable apodwallpaper.service

run:
	python3 ~/.APOD/apodwallpaper.py

all: init config setup run

.PHONY: 
	init, config, setup, run
