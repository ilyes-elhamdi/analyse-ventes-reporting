"""
Génération de données de ventes synthétiques pour l'analyse
Crée un dataset réaliste avec produits, clients, dates, montants, etc.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_sales_data(n_records=10000, start_date='2023-01-01', end_date='2024-12-31'):
    """
    Génère un dataset de ventes synthétiques mais réalistes
    """
    print(f"Génération de {n_records} enregistrements de ventes...")
    
    # Définir les produits avec leurs catégories et prix
    products = {
        'Laptop': {'category': 'Électronique', 'price': 899, 'cost': 600},
        'Smartphone': {'category': 'Électronique', 'price': 699, 'cost': 450},
        'Tablet': {'category': 'Électronique', 'price': 499, 'cost': 320},
        'Headphones': {'category': 'Accessoires', 'price': 149, 'cost': 80},
        'Mouse': {'category': 'Accessoires', 'price': 29, 'cost': 15},
        'Keyboard': {'category': 'Accessoires', 'price': 79, 'cost': 40},
        'Monitor': {'category': 'Électronique', 'price': 349, 'cost': 220},
        'Webcam': {'category': 'Accessoires', 'price': 89, 'cost': 50},
        'SSD 1TB': {'category': 'Stockage', 'price': 119, 'cost': 70},
        'External HDD': {'category': 'Stockage', 'price': 79, 'cost': 45},
        'USB Cable': {'category': 'Accessoires', 'price': 12, 'cost': 5},
        'Charger': {'category': 'Accessoires', 'price': 35, 'cost': 18},
    }
    
    # Régions de vente
    regions = ['Nord', 'Sud', 'Est', 'Ouest', 'Centre']
    
    # Canaux de vente
    channels = ['Online', 'Magasin', 'Revendeur', 'Direct']
    
    # Statuts de commande
    statuses = ['Livrée', 'En cours', 'Annulée']
    status_weights = [0.85, 0.10, 0.05]  # 85% livrées, 10% en cours, 5% annulées
    
    # Générer les dates
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    date_range = (end - start).days
    
    # Créer les listes de données
    data = []
    
    for i in range(n_records):
        # Date aléatoire avec plus de ventes récentes (distribution exponentielle)
        days_ago = int(np.random.exponential(date_range / 4))
        days_ago = min(days_ago, date_range)
        date = end - timedelta(days=days_ago)
        
        # Produit aléatoire (certains plus populaires que d'autres)
        product_name = random.choices(
            list(products.keys()),
            weights=[2, 3, 1.5, 2.5, 3, 2, 1, 1.5, 2, 1.5, 4, 2.5],
            k=1
        )[0]
        
        product = products[product_name]
        
        # Quantité (la plupart sont de petites quantités)
        quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
        
        # Prix avec petite variation (+/- 10%)
        price_variation = np.random.uniform(0.9, 1.1)
        unit_price = round(product['price'] * price_variation, 2)
        total_price = round(unit_price * quantity, 2)
        
        # Coût (pour calculer la marge)
        unit_cost = round(product['cost'] * price_variation, 2)
        total_cost = round(unit_cost * quantity, 2)
        profit = round(total_price - total_cost, 2)
        margin = round((profit / total_price) * 100, 2) if total_price > 0 else 0
        
        # Région (certaines régions vendent plus)
        region = random.choices(regions, weights=[0.25, 0.20, 0.22, 0.18, 0.15], k=1)[0]
        
        # Canal (Online est le plus populaire)
        channel = random.choices(channels, weights=[0.45, 0.30, 0.15, 0.10], k=1)[0]
        
        # Statut
        status = random.choices(statuses, weights=status_weights, k=1)[0]
        
        # ID client (environ 2000 clients différents)
        customer_id = f'C{random.randint(1000, 2999)}'
        
        # ID commande
        order_id = f'ORD-{date.year}{date.month:02d}{i+1:05d}'
        
        # Ajouter l'enregistrement
        data.append({
            'order_id': order_id,
            'date': date.strftime('%Y-%m-%d'),
            'customer_id': customer_id,
            'product': product_name,
            'category': product['category'],
            'quantity': quantity,
            'unit_price': unit_price,
            'total_price': total_price,
            'unit_cost': unit_cost,
            'total_cost': total_cost,
            'profit': profit,
            'margin_percent': margin,
            'region': region,
            'channel': channel,
            'status': status,
            'year': date.year,
            'month': date.month,
            'quarter': f'Q{(date.month-1)//3 + 1}',
            'weekday': date.strftime('%A')
        })
    
    # Créer le DataFrame
    df = pd.DataFrame(data)
    
    print(f"✓ Dataset généré: {len(df)} enregistrements")
    print(f"  - Période: {df['date'].min()} à {df['date'].max()}")
    print(f"  - Produits: {df['product'].nunique()}")
    print(f"  - Clients: {df['customer_id'].nunique()}")
    print(f"  - Ventes totales: ${df['total_price'].sum():,.2f}")
    
    return df


def save_data(df, output_path='../data/sales_data.csv'):
    """
    Sauvegarde le dataset dans un fichier CSV
    """
    print(f"\nSauvegarde des données: {output_path}")
    df.to_csv(output_path, index=False)
    print("✓ Données sauvegardées")


def get_data_summary(df):
    """
    Affiche un résumé statistique des données
    """
    print("\n" + "=" * 70)
    print("RÉSUMÉ DES DONNÉES")
    print("=" * 70)
    
    print(f"\n📊 Statistiques générales:")
    print(f"  - Nombre d'enregistrements: {len(df):,}")
    print(f"  - Nombre de clients uniques: {df['customer_id'].nunique():,}")
    print(f"  - Nombre de produits: {df['product'].nunique()}")
    print(f"  - Période: {df['date'].min()} → {df['date'].max()}")
    
    print(f"\n💰 Métriques financières:")
    print(f"  - Chiffre d'affaires total: ${df['total_price'].sum():,.2f}")
    print(f"  - Coût total: ${df['total_cost'].sum():,.2f}")
    print(f"  - Profit total: ${df['profit'].sum():,.2f}")
    print(f"  - Marge moyenne: {df['margin_percent'].mean():.2f}%")
    
    print(f"\n📈 Top 5 produits (par ventes):")
    top_products = df.groupby('product')['total_price'].sum().sort_values(ascending=False).head(5)
    for product, sales in top_products.items():
        print(f"  - {product}: ${sales:,.2f}")
    
    print(f"\n🌍 Répartition par région:")
    region_sales = df.groupby('region')['total_price'].sum().sort_values(ascending=False)
    for region, sales in region_sales.items():
        percent = (sales / df['total_price'].sum()) * 100
        print(f"  - {region}: ${sales:,.2f} ({percent:.1f}%)")
    
    print("\n" + "=" * 70)


# Exécution si appelé directement
if __name__ == "__main__":
    print("=" * 70)
    print("GÉNÉRATION DU DATASET DE VENTES")
    print("=" * 70)
    
    # Générer les données
    df = generate_sales_data(n_records=10000)
    
    # Afficher le résumé
    get_data_summary(df)
    
    # Sauvegarder
    save_data(df)
    
    print("\n✓ Dataset prêt pour l'analyse!")
