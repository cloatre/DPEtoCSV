# coding: utf-8

from lxml import etree

tree = etree.parse("T783L_resultat_01_01_01_000.xml")
ligne_fichier_resultat=[]

#remplissage du bloc vert
#Codification DPE|Titulaire du marché|Date de visite|Date du DPE|Etiquette énergétique|Consommation énergétique (kWhep/m².an)|Chauffage (kWh ep)|"ECS (kWh ep)"|Etiquette GES|Emission GES (kg eq CO2/m².an)|Quantité d'énergie d'orignine renouvelable  (kWhep/m2.an)|
entete_fichier_resultat=['Codification DPE','Titulaire du marché','Date de visite','Date du DPE','Etiquette énergétique','Consommation énergétique (kWhep/m².an)','Chauffage (kWh ep)','"ECS (kWh ep)"','Etiquette GES','Emission GES (kg eq CO2/m².an)','Quantité d\'énergie d\'orignine renouvelable  (kWhep/m2.an)']
print(entete_fichier_resultat)
import csv
import csv
with open('some.csv', 'wb') as f:
    writer = csv.writer(f, dialect='excel')
    ligne=''
    for i in entete_fichier_resultat:
        ligne+=i + "|"
    writer.writerow([ligne, ])

#for item in entete_fichier_resultat:
    #item.encode('utf-8')
print(entete_fichier_resultat)
for Generalites_DPE in tree.xpath("/Projet/Generalites_DPE"):
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Reference_etude"))
    ligne_fichier_resultat.append("INNAX")
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Date_visite"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Date_etude"))

for Resume_DPE in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Resume_DPE"):
    ligne_fichier_resultat.append(Resume_DPE.findtext("Lettre_energie"))
    ligne_fichier_resultat.append(Resume_DPE.findtext("Valeur_energie"))
    ligne_fichier_resultat.append("Chauffage(kWh?")
    ligne_fichier_resultat.append("ECS(kWh?")
    ligne_fichier_resultat.append(Resume_DPE.findtext("Lettre_ges"))
    ligne_fichier_resultat.append(Resume_DPE.findtext("Valeur_ges"))
    ligne_fichier_resultat.append(Resume_DPE.findtext("energie renouvellable?"))

print(ligne_fichier_resultat)


print("######################################DEBUG")
entete_fichier_resultat.extend(['ESI programme','ESI Bâtiment','Adresse','Code postal','Ville','Nbre de logements','Surface habitable','Année de construction'])
print(entete_fichier_resultat)
#remplissage du bloc jaune
#ESI programme|ESI Bâtiment|Adresse|Code postal|Ville|Nbre de logements|Surface habitable|Année de construction|
for Generalites_DPE in tree.xpath("/Projet/Generalites_DPE"):
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Reference_etude"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Reference_etude"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Adresse"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Code_postal"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Localite"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("nombre?"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("surface habitable?"))
    ligne_fichier_resultat.append(Generalites_DPE.findtext("Annee_construction"))

print(ligne_fichier_resultat)


#remplissage du bloc orange: MUR
#potentielle liste de 1 à N murs

print("###########DEBUG")
for mur in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_murs"):
    #detail_mur=mur.get("detail_murs")
    print mur
    print mur.getchildren()
    print len(mur.getchildren())
    #help(mur)

exit()

somme_surface_totale=0.0
for mur in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_murs/Mur"):
    #pour chaque mur on ajoute les collones d'entete
    entete_fichier_resultat.extend([ str("Type "+mur.findtext("Id")), 'Superficie(m2)', 'isolation'])
    ligne_fichier_resultat.append(mur.findtext("Descriptif_court"))
    surface_totale=mur.findtext("Surface_totale")
    ligne_fichier_resultat.append(surface_totale)
    ligne_fichier_resultat.append(mur.findtext("Surface_isolee"))
    #remplacement des virgules pour passer des .
    surface_totale= surface_totale.replace(',', '.')
    somme_surface_totale+=float(surface_totale)


entete_fichier_resultat.extend([ 'Total surface mur'])
ligne_fichier_resultat.append(str(somme_surface_totale))



#remplissage du bloc orange: MENUISERIES
#potentielle liste de 1 à N fenetres
#Batiment__Zone__Logement__Etat__Enveloppe__detail_vitr__Vitrage__Id

somme_surface_totale_vitrage=0.0
for vitrage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage"):
    #pour chaque mur on ajoute les collones d'entete
    entete_fichier_resultat.extend([ str("Type "+vitrage.findtext("Id")), 'Superficie(m2)', 'Lame d\'air'])
    ligne_fichier_resultat.append(vitrage.findtext("Descriptif_court"))
    surface_totale=mur.findtext("Surface_totale")
    ligne_fichier_resultat.append(surface_totale)
    ligne_fichier_resultat.append(vitrage.findtext("lame dair"))
    #remplacement des virgules pour passer des .
    surface_totale= surface_totale.replace(',', '.')
    somme_surface_totale_vitrage+=float(surface_totale)

entete_fichier_resultat.extend([ 'Total surface vitrée'])
ligne_fichier_resultat.append(str(somme_surface_totale_vitrage))

#remplissage du bloc orange: Toiture
#pas trouve dans l'XML???
entete_fichier_resultat.extend([ 'Type 1', 'Superficie(m2)', 'Lame d\'air'])
ligne_fichier_resultat.extend([' ', ' ', ' '])

print("####################")
print entete_fichier_resultat
print("####################")
print ligne_fichier_resultat




#remplissage du bloc orange: PLANCHER BAS
#potentielle liste de 1 à N planchers
#Batiment__Zone__Logement__Etat__detail_chauffage__Io
entete_fichier_resultat.extend(['Energie' , 'Système',	'Emetteurs',	'ECS', 'Ventilation'])

for chauffage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/detail_chauffage/systeme_collection/systeme"):
    #pour chaque mur on ajoute les collones d'entete
    ligne_fichier_resultat.append(chauffage.findtext("energie???"))
    ligne_fichier_resultat.append(chauffage.findtext("Designation_systeme_court"))
    ligne_fichier_resultat.append(chauffage.findtext("Designation_emetteur_court"))
for ECS in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/detail_ECS/systeme_collection/systeme"):
    ligne_fichier_resultat.append(ECS.findtext("Designation_court"))

#ajout de la ventilation
for ventilation in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_ventilation"):
    ligne_fichier_resultat.append(ventilation.findtext("Designation_court"))


#remplissage du bloc orange: Préconisation de travaux 1
#???
entete_fichier_resultat.extend(['Préco de travaux: Type' , 'Caractéristique des travaux d\'amélioration',	'Quantité',	'ECS', 'Ventilation', 'Etiquette énergétique après travaux', 'Consommation énergétique après travaux(kWhep/m².an)'])
ligne_fichier_resultat.extend([' ?? ', '??', '??', '??'])

with open('resultat_loic_total.csv', 'wb') as f:
    writer = csv.writer(f, dialect='excel')
    ligne = ''
    for i in entete_fichier_resultat:
        ligne+=i + " |"
    writer.writerow([ligne, ])
    ligne = ''
    for i in ligne_fichier_resultat:
        print i
        if i != None:
            ligne+=i + " |"
        else:
            ligne += "  |"
    #ligne pour supprimer les eventuels retour charriot issus de l'xml
    ligne=ligne.replace('\n',' ')
    ligne=ligne.encode('UTF-8')
    writer.writerow([ligne, ])