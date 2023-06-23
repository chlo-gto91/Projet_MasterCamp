import pandas as pd
import re
import unidecode
import Levenshtein
import string
from nltk.stem import SnowballStemmer
from collections import Counter
import numpy as np
from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

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
        if mot_test==mot:
            return True
        else:
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
        elif detecter_emotion_ecart_mot(com_mot[i],negatif_df.values[:,0]):
            if com_mot[i] != 'pas' and com_mot[i] != 'jamais' and com_mot[i] != 'rien':
                if com_mot[i] not in sujet_aborde:
                    if verif_neg(com_mot, i):
                        dic[com_mot[i]] = ["P", i]
                    else :
                        dic[com_mot[i]] = ["N", i]
    return dic

###### Recherche emotion ########

# regarder si le mot dans la liste à 2 lettres d'erreur considèrer comme identitique
def detecter_sujet_ecart_mot(mot,df):

    for mot_test in df:
        if mot_test==mot:
            distance = Levenshtein.distance(mot_test,mot)
            if distance <= 1:  # La distance maximale autorisée
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
                        if len(emo)==0:
                            emo = com_mot[i]
                        else :
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

def enlever_doublons(sujets_counts):
    notin=[]
    conteur=[]
    index=[]
    for val in range(len(sujets_counts)):
        if val not in notin:
            conteur.append(sujets_counts[val])
            index.append(sujets_counts.index[val])
            for i in range (val+1,len(sujets_counts)):
                if i not in notin:
                    distance = Levenshtein.distance(sujets_counts.index[val], sujets_counts.index[i])
                    if distance <= 1:  # La distance maximale autorisée
                        ind = val - len(notin)
                        notin.append(i)
                        conteur[ind] = conteur[ind] + sujets_counts[i]


    con=np.array(conteur)

    s=pd.Series(con , index=index)
    return s

def mot_majeur(liste,x):
    sujets_counts = liste.value_counts()
    s=enlever_doublons(sujets_counts)
    # Obtenez le sujet qui apparaît le plus fréquemment (le premier élément de la série sujets_counts)
    sujet_plus_frequent = s.index[0:x]

    return sujet_plus_frequent

def emotion_majeur(sujet_frequent,data):
    dic={}
    for sujet in sujet_frequent:
        df_sujet = data.loc[data['Sujet'] == sujet]
        mot_frequent = mot_majeur(df_sujet['Emotion'],2)
        dic[sujet]=mot_frequent
    return dic

def trouver_info(data):
    data_pos = split_sujet(data)
    x = int(len(data_pos) * 0.05)
    sujet_frequent_pos = mot_majeur(data_pos['Sujet'],3)
    dic=emotion_majeur(sujet_frequent_pos, data)

    return dic

#####################################
##### PROGRAMME PRINCIPALE ##########
####################################


# Nos données : sujet et emotion
positif_df = pd.read_csv("positif_df.csv")
positif_df=pd.DataFrame(positif_df)
negatif_df = pd.read_csv("negatif_df.csv")
negatif_df=pd.DataFrame(negatif_df)
sujet_aborde = ["site", "haleine","dent","internet", "personnel", "livraison", "marque", "delai", "esthetique",
                    "collection", "materiel", "prix", "etablissement", "matiere", "taille", "politesse", "cashback",
                    "produit", "commande", "service", "client", "vetement", "qualite", "regler", "renvoi", "image", 
                    "roman", "histoire", "tissus", "pads", "utilite", "achat", "design","couleurs","brosse", "utilisation", 
                    "solide", "solidite", "appareil", "clips", "article", "coutures", "toile", "plastique", "housse", "nettoyage", "poil"]

adverbe=["peu", "pas","mais","sans","dans","pour","plus","vous","elle"]
liste_com_df=pd.read_csv("reviews2.csv")
liste_com_df=pd.DataFrame(liste_com_df)
print(liste_com_df)
#Dataframe qui contindra emotion et sujet pour tous les commentaires analysé
dfinal= pd.DataFrame({
        "Emotion": [],
        "Sujet": [],
        "P/N": [] # changer derniere colonne par coef ou ajouter colonne avec
    })
polarity = []
for com in liste_com_df['Review']:
    phrases_separees = segmenter_phrases(com)

    #initialisation du dataframes pour chaque com
    df = pd.DataFrame({
            "Emotion": [],
            "Sujet": [],
            "P/N": []
        })

    for phrase in phrases_separees:

        polarity.append(TextBlob(phrase, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0])

        #Permet de simplifier le message pour annalyse
        texte_modifie = phrase.replace("'", " ")
        phrase_sans_ponctuation = enlever_ponctuation(texte_modifie)
        texte_sans_accents = unidecode.unidecode(phrase_sans_ponctuation)
        phrase = texte_sans_accents.lower()
        phrase = enleverpetitmot(phrase )

        polarity.append(TextBlob(phrase, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0])

        #print(phrase)

        #Analyse de la phrase
        dic=chercheemotion(phrase,positif_df,negatif_df,sujet_aborde)
        df=trouve_sujet(dic, phrase, df,positif_df, negatif_df,sujet_aborde,adverbe) # trouver le sujet

    #print(df) # resultat pour un commentaire

    #assembler dans un data frame final
    dfinal=pd.concat([dfinal,df])

# mettre proprement dataframe final avec les indexs 
dfinal=dfinal.reset_index()
dfinal = dfinal.drop('index', axis=1)

#print(dfinal) # résultat de tous les commentaires

#séparer le dataframe entre P et N 

data_pos = dfinal.loc[dfinal['P/N'] == 'P']
data_neg = dfinal.loc[dfinal['P/N'] == 'N']


dic_pos=trouver_info(data_pos)
dic_neg=trouver_info(data_neg)

print("Positif : ",dic_pos)
print("Negatif : ",dic_neg)

#MESSAGE ENTREPRISE 
print("\nBienvenu dans l'analyse des avis que vos clients ont donné sur votre entreprise et vos produits ! ")
mes_pos = "\nNous avons recueilli plusieurs avis positifs sur votre site web : les plus récurrents montrent une satisfaction liée aux points suivants :"
print(mes_pos)
sujet_pos = dic_pos.keys()
for cle in sujet_pos:
    print(cle)

mes_neg = "\nAttention, des points négatifs ont été relevés dans certains avis publiés ! Une méthode d'action peut être alors mise en place pour améliorer votre service ou vos produits. les plus récurrents montrent une insatisfaction ou mécontentement liée aux points suivants :"
print(mes_neg)
sujet_neg = dic_neg.keys()
for cle in sujet_neg:
    print(cle)

labels = ['Très insatisfait', 'Insatisfait', 'Moyen', 'Satisfait', 'Très satisfait']
stars = list(liste_com_df['Stars'])
proportion = [stars.count(1), stars.count(2), stars.count(3), stars.count(4), stars.count(5)]

# Vérifier les comptes de chaque catégorie et les filtrer
filtered_labels = []
filtered_proportion = []
for i in range(len(labels)):
    if proportion[i] > 0:
        filtered_labels.append(labels[i])
        filtered_proportion.append(proportion[i])

# Créer le graphique circulaire avec les données filtrées
plt.pie(filtered_proportion, labels=filtered_labels, autopct='%1.1f%%', startangle=90)
plt.title('Répartition des évaluations')
plt.show()

plt.plot(polarity, label="Courbe d'avis")
plt.xlabel('Nombre de commentaires ')
plt.ylabel('Niveau de positivité ')
plt.title('Emotion générale des commentaires')
plt.legend()
plt.show()


#%% Partie analyse des dates
date_df = liste_com_df['Date']
date_df = date_df.str.extract(r'le (\d+ \w+ \d{4})')
# Renommer les colonnes
date_df.columns = ['Date']

# Afficher le df avec toutes les dates
print(date_df)

date_df['Date'] = date_df['Date'].astype(str)


date_df['year'] = ''
date_df['month'] = ''

# Extraire le mois et l'année à partir de la colonne "Date"
for index, row in date_df.iterrows():
    date_parts = row['Date'].split(' ')
    if len(date_parts) >= 2:
        row['year'] = date_parts[-1]
        row['month'] = date_parts[-2]

date_df = date_df.drop(date_df.columns[0], axis=1)
print(date_df)


month_order = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
date_df['month'] = pd.Categorical(date_df['month'], categories=month_order, ordered=True)

# Créer les graphique avec l'échelle des mois triée
# Fréquence des avis en fonction des mois 
plt.figure(figsize=(12, 6))
sns.countplot(data=date_df, x='month', hue='year')
plt.xlabel('Mois')
plt.ylabel('Fréquence')
plt.title('Fréquence des dates')
plt.legend(title='Année', loc='upper right')

# Fréquence des avis en fonction des années
plt.show()
plt.figure(figsize=(12, 6))
sns.countplot(data=date_df, x='year', hue='month')
plt.xlabel('Année')
plt.ylabel('Fréquence')
plt.title('Fréquence des dates')
plt.legend(title='Mois', loc='upper right')

plt.show()

# Fréquence des avis en fonction des années
plt.figure(figsize=(12, 6))
sns.countplot(data=date_df, x='year')
plt.xlabel('Année')
plt.ylabel('Fréquence')
plt.title('Fréquence des dates par année')

plt.show()


