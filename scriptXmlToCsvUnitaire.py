# coding: utf-8

from lxml import etree
import os
from lxml import etree


#
#Cette fonction va scanner un répertoire contenant des XML a aggreger dans un seul CSV
#Ca va rechercher le nombre de fenetre/Mur/Plancher et mettre à jour le max si besoin
def calculTailleColonneMax(nameofPath):
    entries = os.listdir(nameofPath)
    global nbMurMax
    global nbMenuiserieMax
    global nbPlancherMax



    nbMur=0
    nbMenuiserie=0
    nbPlancher=0
    for entry in entries:
        #RAZ à chaque fichier des compteurs
        nbMur = 0
        nbMenuiserie = 0
        nbPlancher = 0
        print(entry)
        tree = etree.parse(str("fichier_xml/" + entry))
        for mur in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_murs/Mur"):
            nbMur=nbMur+1

        for vitrage in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_vitr/Vitrage"):
            #pour le vitrage c'est plus compliqué, il faut regrouper par type de vitrage
            mapFenetreSurface = {}
            if vitrage.findtext("Code") in mapFenetreSurface:
                item = mapFenetreSurface.get(vitrage.findtext("Code"))
                # update valeur
            else:
                # on ajoute la case
                mapFenetreSurface[vitrage.findtext("Code")] = vitrage.findtext("Surface_totale").replace(',', '.')
                nbMenuiserie = nbMenuiserie + 1

            for code, surface in mapFenetreSurface.items():
                nbMenuiserie = nbMenuiserie


        for plancher in tree.xpath("/Projet/Batiment/Zone/Logement/Etat/Enveloppe/detail_planchers/Plancher"):
            nbPlancher=nbPlancher+1

        #maintenant on compare les resultats avec les anciens MAX
        if nbMur > nbMurMax:
            nbMurMax=nbMur
        if nbMenuiserie>nbMenuiserieMax:
            nbMenuiserieMax=nbMenuiserie
        if nbPlancher>nbPlancherMax:
            nbPlancherMax=nbPlancher

        #generateOneCsvLineFromOneXML(entry)

#
#Cette fonction parse un XML et génère une liste avec les parametres du CSV
#
def generateOneCsvLineFromOneXML(nameOfFile):
    global enteteEcrite


    nom_fichier="T783L_resultat_01_01_01_000.xml"
    tree = etree.parse("fichier_xml/"+nameOfFile)
    ligne_fichier_resultat=[nameOfFile]

    #remplissage du bloc vert
    #Codification DPE|Titulaire du marché|Date de visite|Date du DPE|Etiquette énergétique|Consommation énergétique (kWhep/m².an)|Chauffage (kWh ep)|"ECS (kWh ep)"|Etiquette GES|Emission GES (kg eq CO2/m².an)|Quantité d'énergie d'orignine renouvelable  (kWhep/m2.an)|
    entete_fichier_resultat=['NomFichier', 'Codification DPE','Titulaire du marché',
                             'Date de visite','Date du DPE','Etiquette énergétique',
                             'Consommation énergétique (kWhep/m².an)','Chauffage (kWh ep)',
                             '"ECS (kWh ep)"','Etiquette GES','Emission GES (kg eq CO2/m².an)','Quantité d\'énergie d\'orignine renouvelable  (kWhep/m2.an)',
                             'shab', 'Nbr_logement']
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

    for Logement in tree.xpath("/Projet/Batiment/Zone/Logement"):
        ligne_fichier_resultat.append(Logement.findtext("Shab"))
        ligne_fichier_resultat.append(Logement.findtext("Nbr_logement"))

    print(ligne_fichier_resultat)
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

    ######################################################################################################################
    #remplissage du bloc orange: MUR
    #potentielle liste de 1 à N murs
    ######################################################################################################################

    somme_surface_totale=0.0
    nbMur=0
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
        nbMur = nbMur +1


    #on complete la ligne avec des blancs pour se recaler avec les autres fichiers
    for i in range(nbMur, nbMurMax):
        entete_fichier_resultat.extend([' ', ' ', ' '])
        ligne_fichier_resultat.extend([' ', ' ', ' '])


    entete_fichier_resultat.extend([ 'Total surface mur'])
    ligne_fichier_resultat.append(str(somme_surface_totale))

    ######################################################################################################################
    #FIN                                                remplissage du bloc orange: MUR
    ######################################################################################################################


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

    for code, surface in mapFenetreSurface.items():
        print  code
        print str(surface)
        print mapFenetreCodeDescriptif[code]
        print mapFenetreCodeDesignation[code]
        entete_fichier_resultat.extend([ str("Type "+code), 'Superficie(m2)', 'description'])
        ligne_fichier_resultat.append(mapFenetreCodeDesignation[code])
        ligne_fichier_resultat.append(str(surface))
        ligne_fichier_resultat.append(mapFenetreCodeDescriptif[code])
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




    ######################################################################################################################
    #remplissage du bloc orange: PLANCHER BAS
    #potentielle liste de 1 à N planchers
    ######################################################################################################################

    somme_surface_totale=0.0
    nbPlancher=0
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
        nbPlancher=nbPlancher+1


    #on complete la ligne avec des blancs pour se recaler avec les autres fichiers
    for i in range(nbPlancher, nbPlancherMax):
        entete_fichier_resultat.extend([' ', ' ', ' '])
        ligne_fichier_resultat.extend([' ', ' ', ' '])

    entete_fichier_resultat.extend([ 'Total surface plancher'])
    ligne_fichier_resultat.append(str(somme_surface_totale))

    ######################################################################################################################
    #FIN                                remplissage du bloc orange: PLANCHER BAS
    ######################################################################################################################


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

    nomFichierOutputPSV=nameOfFile+"_OUTPUT.psv"
    with open(nomFichierOutputPSV, 'wb') as f:
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

    nomFichierOutput=nameOfFile+"_OUTPUT.csv"
    with open(nomFichierOutput, 'wb') as f:
        writer = csv.writer(f, dialect='excel')
        ligne = ''
        for i in entete_fichier_resultat:
            ligne+=i + " ;"
        writer.writerow([ligne, ])
        ligne = ''
        for i in ligne_fichier_resultat:
            print i
            if i != None:
                ligne+=i + " ;"
            else:
                ligne += "  ;"
        #ligne pour supprimer les eventuels retour charriot issus de l'xml
        ligne=ligne.replace('\n',' ')
        ligne=ligne.encode('UTF-8')
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
    nomFichierOutputGlobal = "globalFichierMerge.csv"
    if enteteEcrite<1:
        with open(nomFichierOutputGlobal, 'wb') as fileMerged:
            # on ecrit tout
            enteteEcrite = 1
            writerGlobal = csv.writer(fileMerged, dialect='excel')
            ligne = ''
            for i in entete_fichier_resultat:
                ligne += i + " ;"
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
                ligne += i + " ;"
            writerGlobal.writerow([ligne, ])

            #dans ce cas on n'ecrit pas l'entete
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




#################DEBUT du MAIN
#On bouche pour appeler la fonction
print("###########DEBUG")
import os
from lxml import etree

nbMurMax=0
nbMenuiserieMax=0
nbPlancherMax=0
enteteEcrite=0

calculTailleColonneMax('fichier_xml')

print 'mur=' + str(nbMurMax)
print 'menuiserie=' + str(nbMenuiserieMax)
print 'plancher=' + str(nbPlancherMax)

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