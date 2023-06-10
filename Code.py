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
def detecter_mot(mot):
    sujet_aborde = ["site", "internet", "personnel", "livraison", "marque", "delai", "esthetique",
                    "collection", "materiel", "prix", "etablissement", "matiere", "taille", "politesse", "cashback",
                    "produit", "commande", "service", "client", "vetement","qualite"]

    for mot_test in sujet_aborde:
        distance = Levenshtein.distance(mot_test,mot)
        if distance <= 2:  # La distance maximale autorisée
            return True

    return False

#si même phrase d'un sujet avant alors même sujet pour cette émotion
def verif_avant(com,df):
    avant=df.iloc[-1]
    if avant["Sujet"] in com:
        return avant["Sujet"]
    return "GENERAL"

# associe à chaque emotion le sujet
def trouve_sujet(dic,com,df):

    com_mot = com.split()

    for key in dic.keys():
        pos = dic[key][1]
        debut = pos - 4

        if debut < 0:
            debut = 0

        fin = pos + 4

        if fin > len(com_mot):
            fin = len(com_mot)

        emo = ""
        for i in range(debut, fin):
            if detecter_mot(com_mot[i]) :
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
        if len(word)>3 or word=="pas":
            phrase_simple=phrase_simple+" "+word
    return phrase_simple

# Fonction qui sera remplacer par celle de momo et matthieu quand elle marchera
def it(i):
    if i==1:
        return {"incroyable": ["P", 3]}
        #return {"meilleur": ["N", 3]}
    if i==2:
        return {"adorables": ["P", 4], "grande": ["P", 6]}
        #return {"bien": ["P", 2],"rapide":["P",6]}
    if i==3:
        return {"variées": ["P", 3]}
        #return {"long": ["N", 1], "dramatique": ["P", 4]}
    if i==4:
        return {"rapide":["P",1],"excellent":["P", 5]}
    if i==5:
        return {"stylés":["P",8],"abordable":["P",10]}

# Programme principal
com = "Shein est une marque en ligne incroyable ! Leur vetements à la mode sont adorables et de grande qualité. Leurs collections sont variées et suivent les dernières tendances. La livraison est rapide et leur service client est excellent. Je recommande vivement Shein pour tous ceux qui recherchent des vêtement stylés à des prix abordables !"
#com="La qualité n'est pas la meilleure, mais c'est normal à ce prix, on ne peut pas tout avoir. Les livraisons sont bien suivies et de plus en plus rapide. Cashback un peu long, mais rien de dramatique."
phrases_separees = segmenter_phrases(com)

df = pd.DataFrame({
        "Emotion": [],
        "Sujet": [],
        "P/N": []
    })

i=1
for phrase in phrases_separees:

    #Permet de simplifier le message pour annalyse
    phrase = enleverpetitmot(phrase)
    texte_sans_accents = unidecode.unidecode(phrase)
    phrase=texte_sans_accents.lower()
    print(phrase)

    dic=it(i) # fonction momo matthieu
    df=trouve_sujet(dic, phrase, df) # trouver le sujet

    i+=1 # à enelever plus tard
print(df) # resultat pour un commentaire























