# Quand démarrer un service dépendant de l'interface X sous linux

## question à Gemini 2.0

'quand démarrer service dépendant de interface X sous linus en utilisant un fichier .service'

## Réponse de Gemini

Pour démarrer un service dépendant d'une interface spécifique (appelons-la interface X) sous Linux en utilisant un fichier .service systemd, vous devez configurer correctement les dépendances et les conditions de démarrage dans votre fichier de service. Voici les étapes à suivre et les options à considérer :

1. Identifier l'interface et son nom systemd:

Nom de l'interface réseau: Assurez-vous de connaître le nom exact de l'interface réseau (par exemple, eth0, wlan0, enp0s3). Vous pouvez utiliser la commande ip a ou ifconfig pour lister les interfaces disponibles.
Nom de l'unité systemd pour l'interface: Systemd crée des unités pour les interfaces réseau. Le nom de l'unité est généralement basé sur le nom de l'interface. Vous pouvez utiliser 'systemctl list-units --type=device' pour voir les unités d'appareil. Le nom sera souvent quelque chose comme 'sys-subsystem-net-devices-eth0.device'.
2. Créer ou modifier le fichier .service:

Le fichier .service doit contenir les directives nécessaires pour gérer la dépendance. Voici un exemple de structure et les options les plus importantes :

'''Ini, TOML
[Unit]
Description=Mon service dépendant de l'interface X
After=network-online.target
Wants=network-online.target
Before=multi-user.target
Requires=sys-subsystem-net-devices-X.device
After=sys-subsystem-net-devices-X.device

[Service]
Type=simple
ExecStart=/chemin/vers/mon/script

[Install]
WantedBy=multi-user.target
'''
[Unit]
Description=Mon service dépendant de l'interface X
After=network-online.target
Wants=network-online.target
Before=multi-user.target
Requires=sys-subsystem-net-devices-X.device
After=sys-subsystem-net-devices-X.device

[Service]
Type=simple
ExecStart=/chemin/vers/mon/script

[Install]
WantedBy=multi-user.target
'''
Explication des directives importantes:

After=network-online.target et Wants=network-online.target: Ces directives assurent que le service démarre après que le réseau est configuré (au moins partiellement). Wants indique une dépendance faible (si network-online.target échoue, le service essaiera quand même de démarrer). After crée une dépendance forte (le service ne démarrera pas tant que network-online.target n'est pas atteint).
'Requires=sys-subsystem-net-devices-X.device' et 'After=sys-subsystem-net-devices-X.device': C'est la clé pour la dépendance à l'interface. Requires crée une dépendance forte à l'unité d'appareil de l'interface X. Le service ne démarrera pas si l'interface n'est pas active. After assure que le service démarre après que l'interface est active. Remplacez X par le nom réel de votre interface (par exemple, eth0).
'Before=multi-user.target': Indique que le service doit démarrer avant d'atteindre l'état multi-utilisateur.
'Type=simple': Type de service le plus courant.
'ExecStart=/chemin/vers/mon/script': Commande à exécuter pour démarrer le service.
'WantedBy=multi-user.target': Permet d'activer le service au démarrage du système.
3. Placer le fichier .service au bon endroit:

Placez le fichier .service dans /etc/systemd/system/.
4. Recharger systemd et activer le service:
'''bash
sudo systemctl daemon-reload
sudo systemctl enable mon_service.service  # Remplacez mon_service par le nom de votre service
sudo systemctl start mon_service.service
'''
5. Vérifier le statut du service:
'''bash
sudo systemctl status mon_service.service
'''
Points importants et alternatives:

'network.target' vs. 'network-online.target': 'network.target' indique que la configuration réseau de base est terminée, tandis que 'network-online.target' indique que le système est connecté au réseau. 'network-online.target' est généralement plus approprié pour les services qui nécessitent une connectivité réseau.
Utiliser des conditions plus spécifiques: Si vous avez besoin de conditions plus complexes, vous pouvez utiliser les directives Condition* dans la section [Unit]. Par exemple, 'ConditionInterfaceHasCarrier=X' vérifie si l'interface X a un signal porteur (est connectée physiquement).
Débogage: En cas de problème, consultez les journaux systemd avec 'journalctl -u mon_service.service'.
Exemple concret:

Supposons que vous ayez une interface nommée eth1 et un script '/usr/local/bin/mon_script.sh'. Votre fichier 'mon_service.service' pourrait ressembler à ceci :
'''Ini, TOML
[Unit]
Description=Mon service dépendant de l'interface eth1
After=network-online.target
Wants=network-online.target
Before=multi-user.target
Requires=sys-subsystem-net-devices-eth1.device
After=sys-subsystem-net-devices-eth1.device

[Service]
Type=simple
ExecStart=/usr/local/bin/mon_script.sh

[Install]
WantedBy=multi-user.target
'''
