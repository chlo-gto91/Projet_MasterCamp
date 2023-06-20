from textblob import TextBlob
from textblob_fr import PatternTagger, PatternAnalyzer
import matplotlib.pyplot as plt
import pandas as pd
<<<<<<< HEAD
import numpy as np
import unidecode
import string
=======
import unidecode
import string
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from colorspacious import cspace_converter
>>>>>>> c6611eb63f6090f8b117a04306e20328603edac3

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

<<<<<<< HEAD
plt.plot(polarity)

# Couleurs pour les valeurs positives et négatives
positive_color = 'green'
negative_color = 'red'

# Création d'un tableau d'indices
indices = np.arange(len(polarity))

# Tracé du graphe en utilisant des couleurs différentes en fonction de la polarité
plt.scatter(indices, polarity, c=np.where(polarity >= 0, positive_color, negative_color))

# Affichage du graphe
plt.show()




=======
cmaps = {}

plt.plot(polarity, label="Courbe avis")
moyenne = sum(polarity) / len(polarity)
plt.axhline(moyenne, color='red', linestyle='--', label='Moyenne')
plt.xlabel('Nombre de commentaire ')
plt.ylabel('Niveau positivité ')
plt.title('Emotion générale des commentaires')

plt.legend()
plt.show()

>>>>>>> c6611eb63f6090f8b117a04306e20328603edac3
