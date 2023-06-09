import pandas as pd


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

#%% PARTIE ANALYSE SUJET

sujet_abordé = ["site internet","personnel", "livraison", "délai", "esthétique", "materiel","prix","établissement","matière","taille","politesse","produit","commande","service clients"]
   

# Retour attendu machine learning :
dic={"content":["P",2],"desastre":["N",2]}
