import pandas as pd

# Créer une liste avec les humeurs positives
humeurs_positives = ["heureux", "enthousiaste", "épanoui", "optimiste", "serein"]

# Créer une liste avec les humeurs négatives
humeurs_negatives = ["triste", "déprimé", "anxieux", "frustré", "irrité"]

# Créer un DataFrame à partir des listes d'humeurs
df = pd.DataFrame({
    "Humeur": humeurs_positives + humeurs_negatives,
    "Sentiment": ["Positive"] * len(humeurs_positives) + ["Negative"] * len(humeurs_negatives)
})

print(df)