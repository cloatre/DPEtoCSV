import os
from lxml import etree

entries = os.listdir('fichier_xml')
for entry in entries:
    print(entry)

#parcours de tous les fichiers XML, ie tous les batiments
#afin de rechercher les pires cas en nombre de colonne
nb_mur_max=0
nb_menuiserie_max=0
nb_toiture_max=0
nb_plancher_bas_max=0

for fichier in listeFichierXML:
    tree = etree.parse(fichier)
    for mur in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_murs/Mur"):
        nb_mur= mur.
    nb_mur = 0
    nb_menuiserie = 0
    nb_toiture = 0
    nb_plancher_bas = 0
