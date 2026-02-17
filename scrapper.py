#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime
import os
import logging
from bs4 import BeautifulSoup
import time

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)

class SkyrockDataScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'fr-FR,fr;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.data_file = 'data.json'
        
    def load_current_data(self):
        """Charge les données actuelles"""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logging.warning("Fichier data.json non trouvé, création d'un nouveau")
            return None
        except json.JSONDecodeError:
            logging.error("Erreur de décodage JSON")
            return None
    
    def save_data(self, data):
        """Sauvegarde les données"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        logging.info(f"✅ Données sauvegardées dans {self.data_file}")
    
    def scrape_acpm(self):
        """
        Scrape les données ACPM (à adapter selon la structure réelle du site)
        Note: Cette fonction doit être adaptée à la structure HTML de l'ACPM
        """
        try:
            url = "https://www.acpm.fr/Classements/Radios"
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # À ADAPTER : Logique d'extraction basée sur la structure réelle du site
            # Exemple hypothétique :
            streaming_data = {
                'main': 4840000,  # Valeur par défaut
                'klassiks': 1110000,
                'french': 508000,
                'trend': 12.3
            }
            
            # Recherche des données Skyrock dans le tableau
            # (Cette partie doit être personnalisée selon le site réel)
            
            return streaming_data
            
        except requests.RequestException as e:
            logging.error(f"Erreur lors du scraping ACPM: {e}")
            return None
    
    def scrape_mediametrie(self):
        """
        Scrape les données Médiamétrie
        Note: Médiamétrie protège ses données, cette fonction est illustrative
        """
        try:
            # Les données Médiamétrie sont difficiles à scraper automatiquement
            # On maintient les dernières valeurs connues
            return {
                'daily': 3160000,
                'trend': 220,
                'share': 5.3,
                'shareTrend': 0.4
            }
        except Exception as e:
            logging.error(f"Erreur Médiamétrie: {e}")
            return None
    
    def update_data(self):
        """Met à jour toutes les données"""
        logging.info("🚀 Début de la mise à jour des données...")
        
        # Charger les données actuelles
        current_data = self.load_current_data()
        if not current_data:
            current_data = {
                'lastUpdate': datetime.now().strftime('%Y-%m-%d'),
                'streaming': {},
                'digital': {},
                'audience': {},
                'idf': {},
                'shows': {},
                'sources': []
            }
        
        # Mettre à jour avec les nouvelles données
        new_data = current_data.copy()
        new_data['lastUpdate'] = datetime.now().strftime('%Y-%m-%d')
        
        # Scraping ACPM
        acpm_data = self.scrape_acpm()
        if acpm_data:
            new_data['streaming'].update(acpm_data)
            new_data['digital']['stations'][0]['listeners'] = acpm_data.get('main', 4840000)
            new_data['sources'][0]['period'] = datetime.now().strftime('%B %Y').upper()
        
        # Sauvegarde
        self.save_data(new_data)
        logging.info("✅ Mise à jour terminée")
        
        return new_data

def main():
    scraper = SkyrockDataScraper()
    scraper.update_data()

if __name__ == "__main__":
    main()