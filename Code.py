import pandas as pd
import re
import unidecode
import Levenshtein
"""
#%% PARTIE MOMO


humeurs_positives = ["heureux", "enthousiaste", "épanoui", "optimiste", "serein"]
humeurs_negatives = ["triste", "déprimé", "anxieux", "frustré", "irrité"]
inverseur_linguistique = ["pas"]
adverbe = ["très", "peu", "beaucoup"]

 


def pos_ou_neg(commentaire) : 

    mot = string(map(if mot in humeurs_negatives || humeurs_positives))
    if mot in humeurs_positives : 
        return "humeur positive"
    else :
        return "humeur négative"

def inverseur() : 
    if inverseur_linguistique in : 
        return "oui"
    else : 
        return "non"

bool_inv = inverseur()

 
# Créer un DataFrame à partir des listes d'humeurs
df = pd.DataFrame({
    "Humeur": humeurs_positives + humeurs_negatives,
    "Sentiment": ["Positive"] * len(humeurs_positives) + ["Negative"] * len(humeurs_negatives)
    "Inverseur": ["Oui"]
})

# Afficher le DataFrame
df
"""

#%% PARTIE ANALYSE SUJET

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

# regarder si le mot dans la liste à 2 lettres d'erreur considèrer comme identitique
def detecter_mot(mot,df):

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
def trouve_sujet(dic,com,df):

    com_mot = com.split()
    sujet_aborde = ["site", "internet", "personnel", "livraison", "marque", "delai", "esthetique",
                    "collection", "materiel", "prix", "etablissement", "matiere", "taille", "politesse", "cashback",
                    "produit", "commande", "service", "client", "vetement", "qualite", "regler", "renvoi", "image"]

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
            if detecter_mot(com_mot[i],sujet_aborde):
                emo = emo + " " + com_mot[i]

        if len(emo)==0:

            emo=verif_avant(com, df) # si n'a pas trouver le sujet

        new_row = pd.DataFrame({
            "Emotion": [key],
            "Sujet": [emo],
            "P/N": [dic[key][0]]
        })

        df = pd.concat([df, new_row], ignore_index=True)

    return df

#Permet de simplifier les phrases
def enleverpetitmot(phrase):
    words=phrase.split()
    phrase_simple=""
    for word in words:
        if len(word)>3 or word=="pas" or word=="peu" or word=="bon":
            phrase_simple=phrase_simple+" "+word
    return phrase_simple

# Fonction qui sera remplacer par celle de momo et matthieu quand elle marchera
def it(i):
    if i==1:
        #return {"incroyable": ["P", 3]} #1
        return {"meilleur": ["N", 3]} #2
        #return {"surprise":['P',0],"negatives": ["N", 3]} #3
    if i==2:
        #return {"adorables": ["P", 4], "grande": ["P", 6]} #1
        return {"bien": ["P", 2],"rapide":["P",6]} #2
        #return {"probleme": ["N", 7], "rapidement": ["P", 13]} #3
    if i==3:
        #return {"variées": ["P", 3]} #1
        return {"long": ["N", 1], "dramatique": ["P", 4]} #2
        #return {"facile": ["P", 1]} #3
    if i==4:
        return {"rapide":["P",1],"excellent":["P", 5]} #1
        #return {"catastrophique": ["N", 7]} #3
    if i==5:
        return {"stylés":["P",8],"abordable":["P",10]} #1
        #return {"gache": ["N", 9]} #3


def chercheemotion(com,positif_df,negatif_df):

    dic={}
    com_mot = com.split()
    for i in range (len(com_mot)):
        print(com_mot[i])
        if com_mot[i] in positif_df:
            dic[com_mot[i]]=["P",i]
        if com_mot[i] in negatif_df:
            dic[com_mot[i]]=["N",i]
    #print(dic)
    return dic



# Programme principal
#com = "Shein est une marque en ligne incroyable ! Leur vetements à la mode sont adorables et de grande qualité. Leurs collections sont variées et suivent les dernières tendances. La livraison est rapide et leur service client est excellent. Je recommande vivement Shein pour tous ceux qui recherchent des vêtement stylés à des prix abordables !"
com="La qualité n'est pas la meilleure, mais c'est normal à ce prix, on ne peut pas tout avoir. Les livraisons sont bien suivies et de plus en plus rapide. Cashback un peu long, mais rien de dramatique."
#com="Surprise par tant de notes négatives. Cliente depuis des années d'Amazon il m'est arrivé d'avoir des problèmes sur une commande mais elle a toujours été réglée rapidement.Renvoi facile et remboursement dans la semaine.Seul bémol, leurs quelques envois effectués par UPS qui est une entreprise catastrophique. Si j'avais une remarque à faire à Amazon serait de ne jamais travailler avec ce transporteur qui gâche leur image."
phrases_separees = segmenter_phrases(com)

df = pd.DataFrame({
        "Emotion": [],
        "Sujet": [],
        "P/N": []
    })

i=1
dfinal= pd.DataFrame({
        "Emotion": [],
        "Sujet": [],
        "P/N": [] # changer derniere colonne par coef ou ajouter colonne avec
    })

positif_df = pd.read_csv("positif_df.csv")
positif_df=pd.DataFrame(positif_df)
print(positif_df)
negatif_df = pd.read_csv("negatif_df.csv")
negatif_df=pd.DataFrame(negatif_df)
print(negatif_df)

# faire for pour parcourir tout les com du csv recuperer par url dans le site
for phrase in phrases_separees:

    #Permet de simplifier le message pour annalyse
    phrase = enleverpetitmot(phrase)
    texte_sans_accents = unidecode.unidecode(phrase)
    phrase=texte_sans_accents.lower()
    print(phrase)


    dic=chercheemotion(phrase,positif_df,negatif_df)
    #dic=it(i) # fonction momo matthieu
    df=trouve_sujet(dic, phrase, df) # trouver le sujet

    #assembler dans un data frame final
    #dfinal=pd.concat([dfinal,df])
    i+=1 # à enelever plus tard

print(df) # resultat pour un commentaire

#faire apres boucle pour regression

#dfinal=dfinal.reset_index()
#dfinal = dfinal.drop('index', axis=1)
#print(dfinal)



















