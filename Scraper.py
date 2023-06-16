import requests
from bs4 import BeautifulSoup
import csv
import yaml
import re
import time
import pandas as pd

url= input("Entrer l'url des commentaires que vous souhaitez analyser : ")

def scrape_amazon_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    reviews = soup.select('.review .review-text')
    stars = soup.select('.review .review-rating')

    review_data = []

    for review, star in zip(reviews, stars):
        review_text = review.get_text().strip()
        star_rating = star.get_text().strip()

        review_data.append({'review': review_text, 'stars': star_rating})

    return review_data

#with open('config.yml', 'r') as file:
    #config = yaml.safe_load(file)

reviews_data = []

page_number = 1
while True:
    page_url = url #+ f'&pageNumber={page_number}'
    try:
        reviews = scrape_amazon_reviews(page_url)
        if not reviews:
            break
        reviews_data.extend(reviews)
        page_number += 1
    except requests.exceptions.HTTPError as e:
        print(f"Une erreur s'est produite lors de l'accès à {page_url}: {e}")
        time.sleep(5)

        # Attendre un moment entre les requêtes pour éviter d'être bloqué
    time.sleep(2)

output_file = 'reviews.csv'

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['Review', 'Stars']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for review in reviews_data:
        writer.writerow({'Review': review['review'], 'Stars': review['stars']})
        
        
df = pd.read_csv('reviews.csv')
df['Stars'] = df['Stars'].str.extract('(\d)')
df.to_csv('reviews.csv', index=False)

print(df)
        
        