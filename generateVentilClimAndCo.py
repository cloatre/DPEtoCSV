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

    ######################################################################################################################
    #remplissage du bloc orange: ECS/CHAUFFAGE/VENTILATION/CLIM

    ######################################################################################################################

    entete_fichier_resultat.extend(['Energie' , 'Système',	'Emetteurs', 'Energie2' , 'Système2',	'Emetteurs2',	'ECS', 'Ventilation', 'Climatisation'])

    #ici on force le cas ou il y a deux chauffages, par defaut le second sera vide
    nbchauffage=0
    for chauffage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/detail_chauffage/systeme_collection/systeme"):
        #pour chaque mur on ajoute les collones d'entete
        ligne_fichier_resultat.append(chauffage.findtext("energie???"))
        ligne_fichier_resultat.append(chauffage.findtext("Designation_systeme_court"))
        ligne_fichier_resultat.append(chauffage.findtext("Designation_emetteur_court"))
        nbchauffage=nbchauffage+1
    if nbchauffage<2:
        #on remplie de case vides
        ligne_fichier_resultat.append(chauffage.findtext("Null???"))
        ligne_fichier_resultat.append(chauffage.findtext("Null???"))
        ligne_fichier_resultat.append(chauffage.findtext("Null???"))

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
    nomFichierOutputGlobal = datetime.datetime.today().strftime('%Y-%m-%d') + '/' + "globalFichierMerge_VentilClimAndCoUniquementge .csv"
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
enteteEcrite=0

print 'mur=' + str(nbMurMax)
print 'menuiserie=' + str(nbMenuiserieMax)
print 'plancher=' + str(nbPlancherMax)

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
