# coding=utf-8

from lxml import etree
import os
from lxml import etree
import datetime

#
#Cette fonction parse un XML et génère une liste avec les parametres du CSV
#
def generateOneCsvLineFromOneXML(nameOfFile):
    global enteteEcrite


    #nom_fichier="T783L_resultat_01_01_01_000.xml"
    tree = etree.parse("fichier_xml/"+nameOfFile)
    ligne_fichier_resultat=[nameOfFile]

    #remplissage du bloc vert
    #Codification DPE|Titulaire du marché|Date de visite|Date du DPE|Etiquette énergétique|Consommation énergétique (kWhep/m².an)|Chauffage (kWh ep)|"ECS (kWh ep)"|Etiquette GES|Emission GES (kg eq CO2/m².an)|Quantité d'énergie d'orignine renouvelable  (kWhep/m2.an)|
    entete_fichier_resultat=['NomFichier', 'Codification DPE','Titulaire du marché',
                             'Date de visite','Date du DPE','Designation','Etiquette énergétique',
                             'Consommation énergétique (kWhep/m².an)','Chauffage (kWh ep)',
                             '"ECS (kWh ep)"','Etiquette GES','Emission GES (kg eq CO2/m².an)','Quantité d\'énergie d\'orignine renouvelable  (kWhep/m2.an)',
                             'shab', 'Nbr_logement']
    #print(entete_fichier_resultat)
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
    #print(entete_fichier_resultat)
    for Generalites_DPE in tree.xpath("/Projet/Generalites_DPE"):
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Reference_etude"))
        ligne_fichier_resultat.append("INNAX")
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Date_visite"))
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Date_etude"))

    for Resume_DP in tree.xpath("/Projet/Batiment/Zone/Logement"):
        ligne_fichier_resultat.append(Resume_DP.findtext("Designation"))

    for Resume_DPE in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Resume_DPE"):
        ligne_fichier_resultat.append(Resume_DPE.findtext("Lettre_energie"))
        ligne_fichier_resultat.append(Resume_DPE.findtext("Valeur_energie"))

    for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/Chauffage"):
        ligne_fichier_resultat.append(item.findtext("Total_EP"))
        #ligne_fichier_resultat.append("Chauffage(kWh?")
    for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/ECS"):
        ligne_fichier_resultat.append(item.findtext("Total_EP"))
        #ligne_fichier_resultat.append("ECS(kWh?")
    for Resume_DPE in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Resume_DPE"):
        ligne_fichier_resultat.append(Resume_DPE.findtext("Lettre_ges"))
        ligne_fichier_resultat.append(Resume_DPE.findtext("Valeur_ges"))
    sommeENR = 0.0
    for item in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Conso/ENR_Collection/ENR"):
        if item.findtext("Total_EP"):
            sommeENR+= float(item.findtext("Total_EP").replace(',', '.'))
    ligne_fichier_resultat.append(str(sommeENR))
        #print item.findtext("Total_EP")
        #ligne_fichier_resultat.append(Resume_DPE.findtext("energie renouvellable?"))

    for Logement in tree.xpath("/Projet/Batiment/Zone/Logement"):
        ligne_fichier_resultat.append(Logement.findtext("Shab"))
        ligne_fichier_resultat.append(Logement.findtext("Nbr_logement"))

    #print(ligne_fichier_resultat)
    entete_fichier_resultat.extend(['ESI programme','ESI Bâtiment','Adresse','Code postal','Ville','Nbre de logements','Surface habitable','Année de construction'])
    #print(entete_fichier_resultat)
    #remplissage du bloc jaune
    #ESI programme|ESI Bâtiment|Adresse|Code postal|Ville|Nbre de logements|Surface habitable|Année de construction|
    for Generalites_DPE in tree.xpath("/Projet/Generalites_DPE"):
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Reference_etude"))
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Reference_etude"))
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Adresse"))
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Code_postal"))
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Localite"))
    for Logement in tree.xpath("/Projet/Batiment/Zone/Logement"):
        ligne_fichier_resultat.append(Logement.findtext("Nbr_logement"))
#        ligne_fichier_resultat.append(Generalites_DPE.findtext("nombre?"))
    for Logement in tree.xpath("/Projet/Batiment/Zone/Logement"):
        ligne_fichier_resultat.append(Logement.findtext("Shab"))
        #ligne_fichier_resultat.append(Generalites_DPE.findtext("surface habitable?"))
    for Generalites_DPE in tree.xpath("/Projet/Generalites_DPE"):
        ligne_fichier_resultat.append(Generalites_DPE.findtext("Annee_construction"))

    print(ligne_fichier_resultat)

    nomFichierOutputPSV=datetime.datetime.today().strftime('%Y-%m-%d') + '/' + nameOfFile+"_OUTPUT.psv"
    with open(nomFichierOutputPSV, 'wb') as f:
        writer = csv.writer(f, dialect='excel')
        ligne = ''
        for i in entete_fichier_resultat:
            if isinstance(i, unicode):
                #print i
                test = i.encode("utf-8")
                ligne += test + " |"
            else:
                ligne+=i + " |"
        writer.writerow([ligne, ])
        ligne = ''
        for i in ligne_fichier_resultat:
            #print i
            if i != None:
                if isinstance(i, unicode):
                    #print i
                    test = i.encode("utf-8")
                    ligne += test + " |"
                else:
                    ligne += i + " |"
               #          ligne+=i + " |"
            else:
                ligne += "  |"
        #ligne pour supprimer les eventuels retour charriot issus de l'xml
        ligne=ligne.replace('\n',' ')
        #ligne=ligne.encode("utf-8")
        writer.writerow([ligne, ])

    nomFichierOutput=datetime.datetime.today().strftime('%Y-%m-%d') + '/' + nameOfFile+"_OUTPUT.csv"
    with open(nomFichierOutput, 'wb') as f:
        writer = csv.writer(f, dialect='excel')
        ligne = ''
        for i in entete_fichier_resultat:
            if isinstance(i, unicode):
                #print i
                test = i.encode("utf-8")
                ligne += test + " ;"
            else:
                ligne+=i + " ;"
            #ligne+=i + " ;"
        writer.writerow([ligne, ])
        ligne = ''
        for i in ligne_fichier_resultat:
            #print i
            if i != None:
                if isinstance(i, unicode):
                    #print i
                    test = i.encode("utf-8")
                    ligne += test + " ;"
                else:
                    ligne += i + " ;"
                # ligne+=i + " ;"
            else:
                ligne += "  ;"
        #ligne pour supprimer les eventuels retour charriot issus de l'xml
        ligne=ligne.replace('\n',' ')
        #ligne=ligne.encode('UTF-8')
        writer.writerow([ligne, ])



    #ICI on ecrit le fichier mergé, la premiere occurence on ecrit l'entete
    nomFichierOutputGlobal = datetime.datetime.today().strftime('%Y-%m-%d') + '/' + "globalFichierMerge_GeneraliteDPEUniquement.csv"
    if enteteEcrite<1:
        with open(nomFichierOutputGlobal, 'wb') as fileMerged:
            # on ecrit tout
            enteteEcrite = 1
            writerGlobal = csv.writer(fileMerged, dialect='excel')
            ligne = ''
            for i in entete_fichier_resultat:
                if isinstance(i, unicode):
                    #print i
                    test = i.encode("utf-8")
                    ligne += test + " ;"
                else:
                    ligne += i + " ;"
                #ligne += i + " ;"
            writerGlobal.writerow([ligne, ])
            ligne = ''
            for i in ligne_fichier_resultat:
                #print i
                if i != None:
                    ligne += i + " ;"
                else:
                    ligne += "  ;"
            # ligne pour supprimer les eventuels retour charriot issus de l'xml
            ligne = ligne.replace('\n', ' ')
            ligne = ligne.encode('UTF-8')
            writerGlobal.writerow([ligne, ])
    else:
        #on a deja ecrit le premier, on  reouvre le fichier en append
        with open(nomFichierOutputGlobal, 'a+') as fileMerged:
            writerGlobal = csv.writer(fileMerged, dialect='excel')

            ligne = ''
            for i in entete_fichier_resultat:
                if isinstance(i, unicode):
                    #print i
                    test = i.encode("utf-8")
                    ligne += test + " ;"
                else:
                    ligne += i + " ;"
                #ligne += i + " ;"
            writerGlobal.writerow([ligne, ])

            #dans ce cas on n'ecrit pas l'entete
            ligne = ''
            for i in ligne_fichier_resultat:
                #print i
                if i != None:
                    if isinstance(i, unicode):
                        #print i
                        test = i.encode("utf-8")
                        ligne += test + " ;"
                    else:
                        ligne += i + " ;"
                    # ligne+=i + " ;"
                else:
                    ligne += "  ;"
            # ligne pour supprimer les eventuels retour charriot issus de l'xml
            ligne = ligne.replace('\n', ' ')
            #ligne = ligne.encode('UTF-8')
            writerGlobal.writerow([ligne, ])




#################DEBUT du MAIN
#On bouche pour appeler la fonction
print("###########DEBUG")
import os
from lxml import etree

nbMurMax=0
nbMenuiserieMax=0
nbPlancherMax=0
nbPlafondMax=0
enteteEcrite=0

print 'mur=' + str(nbMurMax)
print 'menuiserie=' + str(nbMenuiserieMax)
print 'plancher=' + str(nbPlancherMax)
print 'plafond= '+ str(nbPlafondMax)

#ici on crée le dossier qui va recevoir les fichiers générés
if os.path.isdir(datetime.datetime.today().strftime('%Y-%m-%d') ):
    print "dossier existe deja"
else:
    os.mkdir(datetime.datetime.today().strftime('%Y-%m-%d') , 0755)

# ici on ouvre le fichier global de resultat
# on initialise un booleen pour n'ecrire qu'une entete de colonne

entries = os.listdir('fichier_xml')
for entry in entries:
    print(entry)
    generateOneCsvLineFromOneXML(entry)
    #exit(0)


exit(0)
for mur in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_murs"):
    #detail_mur=mur.get("detail_murs")
    print mur
    print mur.getchildren()
    print len(mur.getchildren())
    #help(mur)
    generateOneCsvLineFromOneXML("test.xml")