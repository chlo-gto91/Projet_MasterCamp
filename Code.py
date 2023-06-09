import pandas as pd

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

def trouve_sujet(dic,com,df):

    sujet_aborde = ["site", "internet","personnel", "livraison","livraisons", "marque","délai", "esthétique","collections", "materiel","prix","établissement","matière","taille","politesse","cashback","produit","commande","service", "client","vêtements","vêtement","qualité"]

    com = com.lower()

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
            if com_mot[i] in sujet_aborde:
                emo = emo + " " + com_mot[i]
        if len(emo)==0:
            emo="GÉNÉRAL"
        new_row = pd.DataFrame({
            "Emotion": [key],
            "Sujet": [emo],
            "P/N": [dic[key][0]]
        })

        df = pd.concat([df, new_row], ignore_index=True)

    return df

com = "Shein est une marque en ligne incroyable ! Leur vetements à la mode sont adorables et de grande qualité. Leurs collections sont variées et suivent les dernières tendances. La livraison est rapide et leur service client est excellent. Je recommande vivement Shein pour tous ceux qui recherchent des vêtement stylés à des prix abordables !"

phrases_separees = segmenter_phrases(com)

df = pd.DataFrame({
        "Emotion": [],
        "Sujet": [],
        "P/N": []
    })
def it(i):
    if i==1:
        return {"incroyable": ["P", 6]}
    if i==2:
        return {"adorables": ["P", 6], "qualité": ["P", 10]}
    if i==3:
        return {"variées": ["P", 3]}
    if i==4:
        return {"rapide":["P",3],"excellent":["P", 9]}
    if i==5:
        return {"stylé":["P",8],"abordable":["P",12]}

i=1
for phrase in phrases_separees:
    dic=it(i)
    df=trouve_sujet(dic, phrase, df)

    i+=1
print(df)























