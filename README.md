# filbleu
Ce petit script écrit en langage Python a pour but de télécharger l'attestation Fil Bleu du mois en cours et d'envoyer le fichier PDF par email.
Le site de Fil Bleu est quelque peu pénible car il faut aller sur la homepage puis s'identifier, cliquer sur un nouveau menu, aller sur les attestations et enfin télécharger l'attestation qui couvre la période voulue.

Il est nécessaire d'avoir un interpréteur python sur sa machine et quelques modules d'installés :
* mechanize
* ConfigParser
* smtplib

La plupart de ces modules sont installés de base avec votre distribution.
Ce script a été testé sous Ubuntu Server 10.04 et Mac OS X 10.11.2

Le script filbleu.py s'appuie sur un fichier config.ini qui contient différentes valeurs dont :
* votre login Fil Bleu
* votre mot de passe Fil Bleu
* l'adresse email d'expédition
* l'adresse email de réception

Un fichier config.ini est donné en exemple.

Enfin, je vous invite à mettre en place une crontab afin de recevoir le fichier PDF par email.
```
30 16 7 * * cd /home/hindy/bin/filbleu && /usr/bin/python filbleu.py
```
