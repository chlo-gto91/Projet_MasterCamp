from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
import unidecode
import string
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from colorspacious import cspace_converter

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

liste_com_df=pd.read_csv("reviews.csv")
liste_com_df=pd.DataFrame(liste_com_df)
print(liste_com_df)
polarity = []
for com in liste_com_df['Review']:
    phrases_separees = segmenter_phrases(com)

    for phrase in phrases_separees:
        # Permet de simplifier le message pour annalyse
        texte_modifie = phrase.replace("'", " ")
        phrase_sans_ponctuation = enlever_ponctuation(texte_modifie)
        texte_sans_accents = unidecode.unidecode(phrase_sans_ponctuation)
        phrase = texte_sans_accents.lower()
        phrase = enleverpetitmot(phrase)

        polarity.append(TextBlob(phrase, pos_tagger=PatternTagger(), analyzer=PatternAnalyzer()).sentiment[0])

cmaps = {}


import matplotlib.pyplot as plt

# Données d'exemple
labels = ['Très insatisfait', 'Insatisfait', 'Moyen', 'Satisfait', 'Très satisfait']
stars=list(liste_com_df['Stars'])
proportion=[stars.count(1),stars.count(2),stars.count(3),stars.count(4),stars.count(5)]
# Création du camembert

plt.pie(proportion, labels=labels, autopct='%1.1f%%', startangle=90)

# Ajout d'un titre
plt.title('Répartition des évaluations')

# Affichage du camembert
plt.show()


plt.plot(polarity, label="Courbe d'avis")
moyenne = sum(polarity) / len(polarity)
plt.axhline(moyenne, color='red', linestyle='--', label='Moyenne')
plt.xlabel('Nombre de commentaires ')
plt.ylabel('Niveau de positivité ')
plt.title('Emotion générale des commentaires')
plt.legend()
plt.show()

