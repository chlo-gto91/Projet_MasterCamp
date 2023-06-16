import pandas as pd
import re
import unidecode
import Levenshtein
import string
from nltk.stem import SnowballStemmer
from collections import Counter

#####################################
##### PARTIE IMPORTER COMMENTAIRE####
####################################

# a mettre ici


#####################################
##### PARTIE ANALYSE PHRASE #########
####################################

#### initialisation commentaire ####

# separer le commentaire complet par chaque phrase
def segmenter_phrases(commentaire):
    marqueurs = ['.', '!', '?']  # Liste des marqueurs de ponctuation
    phrases = []
    phrase = ""
    for caractere in commentaire:
        phrase += caractere
        if caractere in marqueurs:
            phrases.append(phrase.strip())  # Ajouter la phrase à la liste
            phrase = ""
    if phrase:
        phrases.append(phrase.strip())  # Ajouter la dernière phrase si elle existe
    return phrases

#Permet de simplifier les phrases
def enleverpetitmot(phrase):
    words=phrase.split()
    phrase_simple=""
    for word in words:
        if len(word)>3 or word=="pas" or word=="peu" or word=="bon":
            phrase_simple=phrase_simple+" "+word
    return phrase_simple

#enlève point et virgule
def enlever_ponctuation(phrase):
    ponctuation = string.punctuation
    phrase_sans_ponctuation = "".join(caractere for caractere in phrase if caractere not in ponctuation)
    return phrase_sans_ponctuation

#### Recherche sujet ####

#Verifier si vrai negatif et vrai positif
def verif_neg(com_mot,pos):
    debut = pos - 2

    if debut < 0:
        debut = 0

    fin = pos + 1

    if fin > len(com_mot):
        fin = len(com_mot)

    for i in range(debut,fin):
        if com_mot[i]=='pas'or com_mot[i]=='jamais'or com_mot[i]=='rien':
            return True
    return False

#verifier si c'est le même mot suivant orthographe
def detecter_emotion_ecart_mot(mot,df):

    for mot_test in df:
        distance = Levenshtein.distance(mot_test,mot)
        if distance <= 1:  # La distance maximale autorisée
            return True

    return False

#cherche emotion par rapport au dataframe et au commentaire
def chercheemotion(com, positif_df, negatif_df,sujet_aborde):
    dic = {}
    com_mot = com.split()
    for i in range(len(com_mot)):
        if detecter_emotion_ecart_mot(com_mot[i],positif_df.values[:,0]):
            if com_mot[i] != 'pas' and com_mot[i] != 'jamais' and com_mot[i] != 'rien':
                if com_mot[i] not in sujet_aborde:
                    if verif_neg(com_mot, i):
                        dic[com_mot[i]] = ["N", i]
                    else :
                        dic[com_mot[i]] = ["P", i]
        if detecter_emotion_ecart_mot(com_mot[i],negatif_df.values[:,0]):
            if com_mot[i] != 'pas' and com_mot[i] != 'jamais' and com_mot[i] != 'rien':
                if com_mot[i] not in sujet_aborde:
                    if verif_neg(com_mot, i):
                        dic[com_mot[i]] = ["P", i]
                    else :
                        dic[com_mot[i]] = ["N", i]
    print(dic)
    return dic

###### Recherche emotion ########

# regarder si le mot dans la liste à 2 lettres d'erreur considèrer comme identitique
def detecter_sujet_ecart_mot(mot,df):

    for mot_test in df:
        distance = Levenshtein.distance(mot_test,mot)
        if distance <= 2:  # La distance maximale autorisée
            return True

    return False

#si même phrase d'un sujet avant alors même sujet pour cette émotion
def verif_avant(com,df):
    if len(df)!=0:
        avant=df.iloc[-1]
        if avant["Sujet"] in com:
            return avant["Sujet"]
        return "GENERAL"
    else :
        return "GENERAL"

# associe à chaque emotion le sujet
def trouve_sujet(dic,com,df,positif_df, negatif_df,sujet_aborde,adverbe):

    com_mot = com.split()
    for key in dic.keys():
        pos = dic[key][1]
        debut = pos - 3

        if debut < 0:
            debut = 0

        fin = pos +2

        if fin > len(com_mot):
            fin = len(com_mot)

        emo = ""
        for i in range(debut, fin):
            if detecter_sujet_ecart_mot(com_mot[i],sujet_aborde):
                if com_mot[i] not in positif_df.values and com_mot[i] not in negatif_df.values :
                    if com_mot[i]!=key and com_mot[i] not in adverbe:
                        emo = emo + " " + com_mot[i]

        if len(emo)==0:

            emo=verif_avant(com, df) # si n'a pas trouver le sujet
            x=1
            while emo=="GENERAL" and pos+x<len(com_mot):
                j=pos+x
                if com_mot[j] not in positif_df.values and com_mot[j] not in negatif_df.values :
                    if com_mot[j]!=key and com_mot[j] not in adverbe:
                        emo=com_mot[j]
                x+=1
        new_row = pd.DataFrame({
            "Emotion": [key],
            "Sujet": [emo],
            "P/N": [dic[key][0]]
        })

        df = pd.concat([df, new_row], ignore_index=True)

    return df

#####################################
##### PARTIE REGRESSION ############
####################################

####    A FAIRE      ###########

#####################################
##### PARTIE ANALYSE COM ############
####################################
def split_sujet(df):
    rows_to_append = []

    for index, row in df.iterrows():
        sujet = row['Sujet']

        if len(sujet.split()) > 1:
            mots = sujet.split()
            emo = row['Emotion']

            for mot in mots:
                new_row = {'Emotion': emo, 'Sujet': mot,'P/N': row['P/N']}
                rows_to_append.append(new_row)
            df=df.drop(index)
    # Append the new rows to the DataFrame
    if rows_to_append:
        new_rows_df = pd.DataFrame(rows_to_append)
        df = pd.concat([df, new_rows_df], ignore_index=True)

    return df



def sujet_majeur(df):
    sujets_counts = df['Sujet'].value_counts()
    liste_mots_sans_espaces = [mot.strip() for mot in sujets_counts.index]
    print(liste_mots_sans_espaces)
    x=int(len(df)*0.2)
    # Obtenez le sujet qui apparaît le plus fréquemment (le premier élément de la série sujets_counts)
    sujet_plus_frequent = sujets_counts.index[0:x]

    # Affichez le sujet le plus fréquent
    print("Le sujet le plus fréquent est :", sujet_plus_frequent)


#####################################
##### PROGRAMME PRINCIPALE ##########
####################################

#Partie momentané en l'attente de boucle

#com = "Shein est une marque en ligne incroyable ! Leur vetements à la mode sont adorables et de grande qualité. Leurs collections sont variées et suivent les dernières tendances. La livraison est rapide et leur service client est excellent. Je recommande vivement Shein pour tous ceux qui recherchent des vêtement stylés à des prix abordables !"
#com="La qualité n'est pas la meilleure, mais c'est normal à ce prix, on ne peut pas tout avoir. Les livraisons sont bien suivies et de plus en plus rapide. Cashback un peu long, mais rien de dramatique."
#com="Surprise par tant de notes négatives. Cliente depuis des années d'Amazon il m'est arrivé d'avoir des problèmes sur une commande mais elle a toujours été réglée rapidement.Renvoi facile et remboursement dans la semaine.Seul bémol, leurs quelques envois effectués par UPS qui est une entreprise catastrophique. Si j'avais une remarque à faire à Amazon serait de ne jamais travailler avec ce transporteur qui gâche leur image."
#com="Mes deux chiens adorent quand je mets des friandises et qu ils s'amusent a les chercher. Très solide tapis, bonne qualité, assez grand pour 2 voir 3 chiens. Moi j'ai un Springer spaniel et un Shih Tzu. Je recommande ce tapis"
#com="Très joli tapis de fouille. Mon malinois de 1 an l'a adopté tout de suite.Jolies couleurs et items variés, ce qui permet au chien d'avoir plusieurs jeux à disposition.En revanche il est petit. Mesure 70*47 et non 70*50 comme décrit.Les photos d'illustration sont retouchées et donc trompeuses. Ce n'est pas une pratique recommandable. J'enlève donc 1 étoile pour la déception a l'arrivée du produit qu'on est en droit de penser plus grand."
com="Il y a longtemps que j'attendais un nouveau roman de Fred Vargas et celui-ci ne m'a pas déçu. On retrouve le commissaire Adamsberg.L'histoire comme d'habitude est prenante et la fin surprenante"


# Partie qui restera

# Nos données : sujet et emotion
positif_df = pd.read_csv("positif_df.csv")
positif_df=pd.DataFrame(positif_df)
negatif_df = pd.read_csv("negatif_df.csv")
negatif_df=pd.DataFrame(negatif_df)
sujet_aborde = ["site", "internet", "personnel", "livraison", "marque", "delai", "esthetique",
                    "collection", "materiel", "prix", "etablissement", "matiere", "taille", "politesse", "cashback",
                    "produit", "commande", "service", "client", "vetement", "qualite", "regler", "renvoi", "image", 
                    "roman", "histoire", "tissus", "pads", "utilite", "achat", "design","couleurs","brosse", "utilisation", 
                    "solide", "solidite", "appareil", "clips", "article", "coutures", "toile", "plastique", "housse", "nettoyage"]
adverbe=["peu", "pas","mais","sans","dans"]
liste_com_df=pd.read_csv("reviews.csv")
liste_com_df=pd.DataFrame(liste_com_df)
print(liste_com_df)
#Dataframe qui contindra emotion et sujet pour tous les commentaires analysé
dfinal= pd.DataFrame({
        "Emotion": [],
        "Sujet": [],
        "P/N": [] # changer derniere colonne par coef ou ajouter colonne avec
    })
for com in liste_com_df['Review']:
    phrases_separees = segmenter_phrases(com)

    #initialisation du dataframes pour chaque com
    df = pd.DataFrame({
            "Emotion": [],
            "Sujet": [],
            "P/N": []
        })

    for phrase in phrases_separees:

        #Permet de simplifier le message pour annalyse
        texte_modifie = phrase.replace("'", " ")
        phrase = enleverpetitmot(texte_modifie)
        texte_sans_accents = unidecode.unidecode(phrase)
        phrase_sans_ponctuation=enlever_ponctuation(texte_sans_accents)
        phrase=phrase_sans_ponctuation.lower()
        print(phrase)

        #Analyse de la phrase
        dic=chercheemotion(phrase,positif_df,negatif_df,sujet_aborde)
        df=trouve_sujet(dic, phrase, df,positif_df, negatif_df,sujet_aborde,adverbe) # trouver le sujet

    print(df) # resultat pour un commentaire

#------A DECOMMENTER UNE FOIS BOUCLE COM PAR COM FAIT ------

    #assembler dans un data frame final
    dfinal=pd.concat([dfinal,df])

#Fin de la boucle pour passer commentaire par commentaire


# mettre proprement dataframe final avec les indexs 
dfinal=dfinal.reset_index()
dfinal = dfinal.drop('index', axis=1)

#print(dfinal) # résultat de tous les commentaires

#séparer le dataframe entre P et N 

data_pos = dfinal.loc[dfinal['P/N'] == 'P']
data_neg = dfinal.loc[dfinal['P/N'] == 'N']

# Afficher les données filtrées
#print(data_pos)
#print(data_neg)
data_pos=split_sujet(data_pos)
print(data_pos)
sujet_majeur(data_pos)
data_neg=split_sujet(data_neg)
print(data_neg)
sujet_majeur(data_neg)




#--------------------------------APRES : POUR TROUVER LES SUJETS LES PLUS FREQUENTS POUR P ET N-----------------------------------------
"""

        
# Compter les occurrences de chaque sujet pour P et N
compt_emoP = data_pos['Sujet'].value_counts()
compt_emoN = data_neg['Sujet'].value_counts()

# Obtenir l'émotion la plus fréquente pour P et N
emo_freqP = compt_emoP.idxmax()
emo_freqN = compt_emoN.idxmax()

# Afficher l'émotion la plus fréquente dans les positifs puis négatifs
print("Le sujet positif le plus fréquent est :", emo_freqP)
print("Le sujet négatif le plus fréquent est :", emo_freqN)


#trouver les 10% des sujets les plus réccurents
texte_complet = ' '.join(emo_freqP['Sujet'])
sujets = texte_complet.split()
# Comptez la fréquence de chaque sujet
compteur_sujets = Counter(sujets)
total_sujets = len(sujets)

# Déterminez le seuil pour les 10 % des sujets les plus fréquents
seuil = int(total_sujets * 0.1)
sujets_freq = compteur_sujets.most_common()
sujets_pos_top10 = sujets_freq[:seuil]
print(sujets_pos_top10)


texte_complet = ' '.join(emo_freqN['Sujet'])
sujets = texte_complet.split()
compteur_sujets = Counter(sujets)
total_sujets = len(sujets)
seuil = int(total_sujets * 0.1)
sujets_freq = compteur_sujets.most_common()
sujets_neg_top10 = sujets_freq[:seuil]

print(sujets_neg_top10)

"""









