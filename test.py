# coding: utf-8

from lxml import etree

tree = etree.parse("2760L - 4 à 16_resultat_01_01_01_000.xml")
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

with open('resultat_loic_partie_vert.csv', 'wb') as f:
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



entete_fichier_resultat=[]
ligne_fichier_resultat=[]
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

with open('resultat_loic_partie_jaune.csv', 'wb') as f:
    writer = csv.writer(f, dialect='excel')
    ligne = ''
    for i in entete_fichier_resultat:
        print i
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

######################################################################################################################
#remplissage du bloc orange: MUR
#potentielle liste de 1 à N murs
######################################################################################################################
entete_fichier_resultat=[]
ligne_fichier_resultat=[]

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

######################################################################################################################
#FIN remplissage du bloc orange: MUR
######################################################################################################################

with open('resultat_loic_partie_orange_mur.csv', 'wb') as f:
    writer = csv.writer(f, dialect='excel')
    ligne = ''
    for i in entete_fichier_resultat:
        print i
        ligne+=i + " |"
    writer.writerow([ligne, ])
    ligne = ''
    for i in ligne_fichier_resultat:
        print i
        if i != None:
            ligne+=i + " |"
        else:
            ligne += "  |"
    print("######################################DEBUG")
    #ligne pour supprimer les eventuels retour charriot issus de l'xml
    print ligne
    ligne=ligne.replace('\n',' ')
    ligne=ligne.encode('UTF-8')
    writer.writerow([ligne, ])

######################################################################################################################
#remplissage du bloc orange: MENUISERIES
#potentielle liste de 1 à N fenetres
######################################################################################################################
entete_fichier_resultat=[]
ligne_fichier_resultat=[]

#dans mapFenetreSurface, on a le code et la somme des surface (F02, 10.35m2) par exemple
#dans mapFenetreCodeDescriptif, on a le code et le descriptif detaillé
#dans mapFenetreCodeDesignation, on a le code et la designation
mapFenetreSurface={}
mapFenetreCodeDescriptif={}
mapFenetreCodeDesignation={}
somme_surface_totale_vitrage=0.0
#### DEBUG pour faire somme par taille de fenetre
for vitrage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage"):
    #pour chaque mur on ajoute les collones d'entete
    ligne=vitrage.findtext("Id") + "   " + vitrage.findtext("Code") + "   " + vitrage.findtext("Designation")+ "   " + vitrage.findtext("Surface_totale") + "   "+ vitrage.findtext("Descriptif")
    ligne=ligne.replace('\n',' ')
    ligne=ligne.encode('UTF-8')
    print ligne
    #on ajoute la surface de la fenetre a la somme globale (peu importe le type de fenetre
    somme_surface_totale_vitrage += float(vitrage.findtext("Surface_totale").replace(',', '.'))
    if vitrage.findtext("Code")  in mapFenetreSurface:
        item=mapFenetreSurface.get(vitrage.findtext("Code"))
        sommeSurface= float(item) + float(vitrage.findtext("Surface_totale").replace(',', '.'))
        mapFenetreSurface[vitrage.findtext("Code")] =sommeSurface
        #update valeur
    else:
        #on ajoute la case
        mapFenetreSurface[vitrage.findtext("Code")]=vitrage.findtext("Surface_totale").replace(',', '.')
        mapFenetreCodeDescriptif[vitrage.findtext("Code")]=vitrage.findtext("Descriptif").replace('\n',' ')
        mapFenetreCodeDesignation[vitrage.findtext("Code")]=vitrage.findtext("Designation").replace('\n',' ')


entete_fichier_resultat = []
ligne_fichier_resultat = []
for code, surface in mapFenetreSurface.items():
    print  code
    print str(surface)
    print mapFenetreCodeDescriptif[code]
    print mapFenetreCodeDesignation[code]
    entete_fichier_resultat.extend([ str("Type "+code), 'Superficie(m2)', 'description'])
    ligne_fichier_resultat.append(mapFenetreCodeDesignation[code])
    ligne_fichier_resultat.append(str(surface))
    ligne_fichier_resultat.append(mapFenetreCodeDescriptif[code])

entete_fichier_resultat.extend([ 'Total surface vitrée'])
ligne_fichier_resultat.append(str(somme_surface_totale_vitrage))


######################################################################################################################
#FIN                                remplissage du bloc orange: MENUISERIES
######################################################################################################################

#faire une map, avec map_fenetre<Code, surface>
print entete_fichier_resultat
print ligne_fichier_resultat

####

somme_surface_totale_vitrage=0.0
for vitrage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage"):
    #pour chaque mur on ajoute les collones d'entete
    entete_fichier_resultat.extend([ str("Type "+vitrage.findtext("Id")), 'Superficie(m2)', 'Lame d\'air'])
    ligne_fichier_resultat.append(vitrage.findtext("Descriptif_court"))
    surface_totale=vitrage.findtext("Surface_totale")
    ligne_fichier_resultat.append(surface_totale)
    ligne_fichier_resultat.append(vitrage.findtext("lame dair"))
    #remplacement des virgules pour passer des .
    surface_totale= surface_totale.replace(',', '.')
    somme_surface_totale_vitrage+=float(surface_totale)

entete_fichier_resultat.extend([ 'Total surface vitrée'])
ligne_fichier_resultat.append(str(somme_surface_totale_vitrage))



######################################################################################################################
#remplissage du bloc orange: TOITURE
#potentielle liste de 1 à N fenetres
######################################################################################################################

#remplissage du bloc orange: Toiture
#pas trouve dans l'XML???
entete_fichier_resultat.extend([ 'Type 1', 'Superficie(m2)', 'Lame d\'air'])
ligne_fichier_resultat.extend([' ', ' ', ' '])



######################################################################################################################
#FIN                            remplissage du bloc orange: TOITURE
######################################################################################################################
print("####################")
print entete_fichier_resultat
print("####################")
print ligne_fichier_resultat


with open('resultat_loic_partie_orange_menuiserie_toiture.csv', 'wb') as f:
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



######################################################################################################################
#remplissage du bloc orange: PLANCHER BAS
#potentielle liste de 1 à N planchers
######################################################################################################################

entete_fichier_resultat=[]
ligne_fichier_resultat=[]

somme_surface_totale=0.0
for plancher in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_planchers/Plancher"):
    #pour chaque mur on ajoute les collones d'entete
    entete_fichier_resultat.extend([ str("Type "+plancher.findtext("Id")), 'Superficie(m2)', 'isolation'])
    ligne_fichier_resultat.append(plancher.findtext("Descriptif_court"))
    surface_totale=plancher.findtext("Surface_totale")
    ligne_fichier_resultat.append(surface_totale)
    ligne_fichier_resultat.append(plancher.findtext("Surface_isolee"))
    #remplacement des virgules pour passer des .
    surface_totale= surface_totale.replace(',', '.')
    somme_surface_totale+=float(surface_totale)


entete_fichier_resultat.extend([ 'Total surface plancher'])
ligne_fichier_resultat.append(str(somme_surface_totale))

######################################################################################################################
#FIN                                remplissage du bloc orange: PLANCHER BAS
######################################################################################################################


with open('resultat_loic_partie_orange_plancher.csv', 'wb') as f:
    writer = csv.writer(f, dialect='excel')
    ligne = ''
    for i in entete_fichier_resultat:
        print i
        ligne+=i + " |"
    writer.writerow([ligne, ])
    ligne = ''
    for i in ligne_fichier_resultat:
        print i
        if i != None:
            ligne+=i + " |"
        else:
            ligne += "  |"
    print("######################################DEBUG")
    #ligne pour supprimer les eventuels retour charriot issus de l'xml
    print ligne
    ligne=ligne.replace('\n',' ')
    ligne=ligne.encode('UTF-8')
    writer.writerow([ligne, ])
###ENDOF PLANCHER


######################################################################################################################
#remplissage du bloc orange: ECS/CHAUFFAGE/VENTILATION/CLIM

######################################################################################################################

entete_fichier_resultat=['Energie' , 'Système',	'Emetteurs',	'ECS', 'Ventilation', 'Climatisation']
ligne_fichier_resultat=[]

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

#ajout de la climatisation
for clim in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/detail_CLIM"):
    ligne_fichier_resultat.append(clim.findtext("Designation_court"))

######################################################################################################################
#FIN                                remplissage du bloc orange: ECS/CHAUFFAGE/VENTILATION/CLIM
######################################################################################################################


######################################################################################################################
#remplissage du bloc bleu: RESULTAT/PRECO
######################################################################################################################

entete_fichier_resultat.extend(['chauffage Total_EF' , 'chauffage Total_EP',	'ECS Total_EF' , 'ECS Total_EP','ENR Designation' , 'ENR energie','ENR Total_EP' , 'ENR Total_General'])
entete_fichier_resultat.extend(['Reco designation' , 'reco descriptif'])

#ajout de la chauffage Batiment__Zone__Logement__Etat__Conso__
for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/Chauffage"):
    ligne_fichier_resultat.append(item.findtext("Total_EF"))
    ligne_fichier_resultat.append(item.findtext("Total_EP"))
#ajout de la ECS
for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/ECS"):
    ligne_fichier_resultat.append(item.findtext("Total_EF"))
    ligne_fichier_resultat.append(item.findtext("Total_EP"))
#ajout de la ENR
for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/ENR_Collection/ENR"):
    ligne_fichier_resultat.append(item.findtext("Designation"))
    ligne_fichier_resultat.append(item.findtext("energie"))
    ligne_fichier_resultat.append(item.findtext("Total_EP"))
for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/ENR_Collection"):
    ligne_fichier_resultat.append(item.findtext("Total_general"))
for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/Reco"):
    ligne_fichier_resultat.append(item.findtext("Designation"))
    ligne_fichier_resultat.append(item.findtext("Descriptif"))
######################################################################################################################
#FIN                        remplissage du bloc bleu: RESULTAT/PRECO
######################################################################################################################

######################################################################################################################
#remplissage du bloc bleu: RESULTAT/LETTRE/VALEUR
######################################################################################################################
entete_fichier_resultat.extend(['Type_dpe' , 'Lettre_energie', 'Valeur_energie', 'Lettre_ges', 'Valeur_ges'])

#ajout de la chauffage
for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Resume_DPE"):
    ligne_fichier_resultat.append(item.findtext("Type_dpe"))
    ligne_fichier_resultat.append(item.findtext("Lettre_energie"))
    ligne_fichier_resultat.append(item.findtext("Valeur_energie"))
    ligne_fichier_resultat.append(item.findtext("Lettre_ges"))
    ligne_fichier_resultat.append(item.findtext("Valeur_ges"))
######################################################################################################################
#FIN                                remplissage du bloc bleu: RESULTAT/LETTRE/VALEUR
######################################################################################################################


with open('resultat_loic_partie_chauffage_ECS.csv', 'wb') as f:
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