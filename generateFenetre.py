# coding=utf-8

from lxml import etree
import os
from lxml import etree
import datetime

#


#Cette fonction va scanner un répertoire contenant des XML a aggreger dans un seul CSV
#Ca va rechercher le nombre de fenetre/Mur/Plancher et mettre à jour le max si besoin
def calculTailleColonneMax(nameofPath):
    entries = os.listdir(nameofPath)
    global nbMurMax
    global nbMenuiserieMax
    global nbPlancherMax
    global nbPlafondMax


    nbMur=0
    nbMenuiserie=0
    nbPlancher=0
    nbPlafond=0
    for entry in entries:
        #RAZ à chaque fichier des compteurs
        nbMur = 0
        nbMenuiserie = 0
        nbPlancher = 0
        nbPlafond=0
        mapFenetreSurface = {}
        print(entry)
        #entry="4928L-B_resultat_01_01_01_000.xml"
        tree = etree.parse(str("fichier_xml/" + entry))
        for vitrage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage"):
            #pour le vitrage c'est plus compliqué, il faut regrouper par type de vitrage

            #print vitrage.findtext("Descriptif_court")

            #modification, regroupement par description_courte car on peut avoir une commune pour 2 type de fenetres
            if vitrage.findtext("Descriptif_court") in mapFenetreSurface:
                item = mapFenetreSurface.get(vitrage.findtext("Code"))
                # update valeur
            else:
                # on ajoute la case
                if vitrage.findtext("Surface_totale"):
                    mapFenetreSurface[vitrage.findtext("Descriptif_court")] = vitrage.findtext("Surface_totale").replace(',', '.')
                else:
                    mapFenetreSurface[vitrage.findtext("Descriptif_court")] = '0.0'

                nbMenuiserie = nbMenuiserie + 1
                #print "connait pas "
                #print(len(mapFenetreSurface))
                #print mapFenetreSurface

            for code, surface in mapFenetreSurface.items():
                nbMenuiserie = nbMenuiserie


        if nbMenuiserie>nbMenuiserieMax:
            nbMenuiserieMax=nbMenuiserie



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
    #remplissage du bloc orange: MENUISERIES
    #potentielle liste de 1 à N fenetres
    ######################################################################################################################

    #dans mapFenetreSurface, on a le code et la somme des surface (F02, 10.35m2) par exemple
    #dans mapFenetreCodeDescriptif, on a le code et le descriptif detaillé
    #dans mapFenetreCodeDesignation, on a le code et la designation
    mapFenetreSurface={}
    mapFenetreCodeDescriptif={}
    mapFenetreCodeDesignation={}
    somme_surface_totale_vitrage=0.0
    nbMenuiserie=0
    #### DEBUG pour faire somme par taille de fenetre
    for vitrage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage"):
        #pour chaque fenetre on ajoute les colones d'entete
        #correction pour le cas ou il n'y a pas de surface
        #cas normal ou il y a la surface
        if vitrage.findtext("Surface_totale"):
            ligne=vitrage.findtext("Id") + "   " + vitrage.findtext("Code") + "   " + vitrage.findtext("Designation")+ "   " + vitrage.findtext("Surface_totale") + "   "+ vitrage.findtext("Descriptif")

            ####
            # On considere que si la balise Surface_totale existe il doit y avoir 1 à 4 balises d'orientation
            # Nord/Sud/Est/Ouest
            ####
            sommeOrientation=0.0
            for orientation in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage/Sud"):
                sommeOrientation += float(orientation.findtext("Surface").replace(',', '.'))
            for orientation in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage/Nord"):
                sommeOrientation += float(orientation.findtext("Surface").replace(',', '.'))
            for orientation in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage/Est"):
                sommeOrientation += float(orientation.findtext("Surface").replace(',', '.'))
            for orientation in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage/Ouest"):
                sommeOrientation += float(orientation.findtext("Surface").replace(',', '.'))

            ligne=ligne.replace('\n',' ')
            ligne=ligne.encode('UTF-8')
            #print ligne

            #on ajoute la surface de la fenetre a la somme globale (peu importe le type de fenetre
            somme_surface_totale_vitrage += float(sommeOrientation)
            if vitrage.findtext("Descriptif_court")  in mapFenetreSurface:
                item=mapFenetreSurface.get(vitrage.findtext("Descriptif_court"))
                sommeSurface= float(item) + float(sommeOrientation)
                mapFenetreSurface[vitrage.findtext("Descriptif_court")] =sommeSurface
                #update valeur
            else:
                #on ajoute la case
                mapFenetreSurface[vitrage.findtext("Descriptif_court")]=vitrage.findtext("Surface_totale").replace(',', '.')
                mapFenetreCodeDescriptif[vitrage.findtext("Descriptif_court")]=vitrage.findtext("Descriptif").replace('\n',' ')
                mapFenetreCodeDesignation[vitrage.findtext("Descriptif_court")]=vitrage.findtext("Designation").replace('\n',' ')
        else:
            #dans ce cas, on n'a pas de surface dans la balise xml
            ligne = vitrage.findtext("Id") + "   " + vitrage.findtext("Code") + "   " + vitrage.findtext("Designation") + "   " + "0.0" + "   " + vitrage.findtext("Descriptif")
            ligne = ligne.replace('\n', ' ')
            ligne = ligne.encode('UTF-8')
            print ligne

            # on ajoute la surface de la fenetre a la somme globale (peu importe le type de fenetre
            somme_surface_totale_vitrage += float(0)
            if vitrage.findtext("Descriptif_court") in mapFenetreSurface:
                item = mapFenetreSurface.get(vitrage.findtext("Descriptif_court"))
                sommeSurface = float(item) + float(0)
                mapFenetreSurface[vitrage.findtext("Descriptif_court")] = sommeSurface
                # update valeur
            else:
                # on ajoute la case
                mapFenetreSurface[vitrage.findtext("Descriptif_court")] = 0
                mapFenetreCodeDescriptif[vitrage.findtext("Descriptif_court")] = vitrage.findtext("Descriptif").replace('\n', ' ')
                mapFenetreCodeDesignation[vitrage.findtext("Descriptif_court")] = vitrage.findtext("Designation").replace('\n', ' ')

    for descriptif_court, surface in mapFenetreSurface.items():
        print  descriptif_court
        print str(surface)
        print mapFenetreCodeDescriptif[descriptif_court]
        print mapFenetreCodeDesignation[descriptif_court]
        #entete_fichier_resultat.extend([ str("Type "+descriptif_court),'description', 'Superficie(m2)' ])
        entete_fichier_resultat.extend(["Type " + descriptif_court, 'description', 'Superficie(m2)'])
        ligne_fichier_resultat.append(mapFenetreCodeDesignation[descriptif_court])
        ligne_fichier_resultat.append(mapFenetreCodeDescriptif[descriptif_court])
        ligne_fichier_resultat.append(str(surface))
        nbMenuiserie=nbMenuiserie+1

    #on complete la ligne avec des blancs pour se recaler avec les autres fichiers
    for i in range(nbMenuiserie, nbMenuiserieMax):
        entete_fichier_resultat.extend([' ', ' ', ' '])
        ligne_fichier_resultat.extend([' ', ' ', ' '])

    entete_fichier_resultat.extend([ 'Total surface vitrée'])
    ligne_fichier_resultat.append(str(somme_surface_totale_vitrage))


    ######################################################################################################################
    #FIN                                remplissage du bloc orange: MENUISERIES
    ######################################################################################################################

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
    nomFichierOutputGlobal = datetime.datetime.today().strftime('%Y-%m-%d') + '/' + "globalFichierMerge_FenetreUniquement.csv"
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

calculTailleColonneMax('fichier_xml')

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