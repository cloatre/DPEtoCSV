# coding=utf-8

from lxml import etree
import os
from lxml import etree
import datetime

#

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
    entete_fichier_resultat=['NomFichier']
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


    ######################################################################################################################
    # remplissage du nouveau bloc: PLAFOND
    # potentielle liste de 1 à N plafonds
    ######################################################################################################################

    somme_surface_totale = 0.0
    nbPlafond = 0
    for plafond in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_plafond/Plafond"):
        # pour chaque mur on ajoute les collones d'entete
        # entete_fichier_resultat.extend([ str("Type "+mur.findtext("Id")), 'Superficie(m2)', 'isolation'])
        entete_fichier_resultat.extend([str("Type " + plafond.findtext("Id")), 'localisation', 'Superficie(m2)'])
        ligne_fichier_resultat.append(plafond.findtext("Descriptif_court"))
        ligne_fichier_resultat.append(plafond.findtext("Localisation"))
        #s'il y a une surface, cas normal
        if plafond.findtext("Surface_totale"):
            surface_totale = plafond.findtext("Surface_totale")
            ligne_fichier_resultat.append(surface_totale)
            # ligne_fichier_resultat.append(mur.findtext("Surface_isolee"))
            # remplacement des virgules pour passer des .
            surface_totale = surface_totale.replace(',', '.')
            somme_surface_totale += float(surface_totale)
        else:
            #dans ce cas, on n'a pas de surface dans la balise xml
            ligne = plafond.findtext("Id") + "   " + plafond.findtext("Code") + "   " + plafond.findtext("Designation") + "   " + "0.0" + "   " + plafond.findtext("Descriptif")
            ligne = ligne.replace('\n', ' ')
            ligne = ligne.encode('UTF-8')
            ligne_fichier_resultat.append('0.0')
        nbPlafond = nbPlafond + 1

    # on complete la ligne avec des blancs pour se recaler avec les autres fichiers
    for i in range(nbPlafond, nbPlafondMax):
        entete_fichier_resultat.extend([' ', ' ', ' '])
        ligne_fichier_resultat.extend([' ', ' ', ' '])

    entete_fichier_resultat.extend(['Total surface plafond'])
    ligne_fichier_resultat.append(str(somme_surface_totale))

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
            print i
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
            print i
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

    ########DEBUG
    print("DEBUG LCLLLLLLLLLLL")
    print entete_fichier_resultat
    print ligne_fichier_resultat
    for i in ligne_fichier_resultat:
        print i
        #print str(i).encode('UTF-8')

    #exit(0)

    #ICI on ecrit le fichier mergé, la premiere occurence on ecrit l'entete
    nomFichierOutputGlobal = datetime.datetime.today().strftime('%Y-%m-%d') + '/' + "globalFichierMerge_plafondUniquement.csv"
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
                print i
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
                print i
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