"""
Script d'analyse des ventes avec calcul des KPI
Analyse les tendances, performances par produit, région, etc.
"""

import pandas as pd
import numpy as np
from datetime import datetime


def load_sales_data(file_path='../data/sales_data.csv'):
    """
    Charge le fichier de données de ventes
    """
    print(f"Chargement des données: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        df['date'] = pd.to_datetime(df['date'])
        print(f"✓ Données chargées: {len(df)} enregistrements")
        return df
    except Exception as e:
        print(f"✗ Erreur de chargement: {e}")
        return None


def calculate_kpis(df):
    """
    Calcule les KPI (Key Performance Indicators) principaux
    """
    print("\nCalcul des KPI...")
    
    # Filtrer seulement les commandes livrées pour les vrais KPI
    df_delivered = df[df['status'] == 'Livrée']
    
    kpis = {
        'chiffre_affaires': df_delivered['total_price'].sum(),
        'profit_total': df_delivered['profit'].sum(),
        'marge_moyenne': df_delivered['margin_percent'].mean(),
        'nombre_ventes': len(df_delivered),
        'panier_moyen': df_delivered['total_price'].mean(),
        'nombre_clients': df_delivered['customer_id'].nunique(),
        'ca_par_client': df_delivered['total_price'].sum() / df_delivered['customer_id'].nunique(),
        'taux_annulation': (len(df[df['status'] == 'Annulée']) / len(df)) * 100,
    }
    
    print("✓ KPI calculés")
    return kpis


def analyze_by_category(df):
    """
    Analyse des ventes par catégorie de produits
    """
    # Filtrer les ventes livrées
    df_delivered = df[df['status'] == 'Livrée']
    
    category_analysis = df_delivered.groupby('category').agg({
        'total_price': ['sum', 'mean', 'count'],
        'profit': 'sum',
        'margin_percent': 'mean',
        'quantity': 'sum'
    }).round(2)
    
    category_analysis.columns = ['CA_total', 'CA_moyen', 'Nb_ventes', 'Profit_total', 'Marge_%', 'Quantité_totale']
    category_analysis = category_analysis.sort_values('CA_total', ascending=False)
    
    return category_analysis


def analyze_by_region(df):
    """
    Analyse des ventes par région
    """
    df_delivered = df[df['status'] == 'Livrée']
    
    region_analysis = df_delivered.groupby('region').agg({
        'total_price': ['sum', 'mean'],
        'profit': 'sum',
        'order_id': 'count',
        'customer_id': 'nunique'
    }).round(2)
    
    region_analysis.columns = ['CA_total', 'CA_moyen', 'Profit', 'Nb_commandes', 'Nb_clients']
    region_analysis = region_analysis.sort_values('CA_total', ascending=False)
    
    return region_analysis


def analyze_by_channel(df):
    """
    Analyse des ventes par canal de vente
    """
    df_delivered = df[df['status'] == 'Livrée']
    
    channel_analysis = df_delivered.groupby('channel').agg({
        'total_price': ['sum', 'mean'],
        'profit': 'sum',
        'margin_percent': 'mean',
        'order_id': 'count'
    }).round(2)
    
    channel_analysis.columns = ['CA_total', 'CA_moyen', 'Profit', 'Marge_%', 'Nb_ventes']
    channel_analysis = channel_analysis.sort_values('CA_total', ascending=False)
    
    return channel_analysis


def analyze_by_product(df, top_n=10):
    """
    Analyse des produits les plus performants
    """
    df_delivered = df[df['status'] == 'Livrée']
    
    product_analysis = df_delivered.groupby('product').agg({
        'total_price': 'sum',
        'profit': 'sum',
        'margin_percent': 'mean',
        'quantity': 'sum',
        'order_id': 'count'
    }).round(2)
    
    product_analysis.columns = ['CA_total', 'Profit', 'Marge_%', 'Quantité_vendue', 'Nb_commandes']
    product_analysis = product_analysis.sort_values('CA_total', ascending=False).head(top_n)
    
    return product_analysis


def analyze_time_trends(df):
    """
    Analyse des tendances temporelles (mensuelle)
    """
    df_delivered = df[df['status'] == 'Livrée']
    
    # Créer une colonne année-mois
    df_delivered['year_month'] = df_delivered['date'].dt.to_period('M')
    
    monthly_trends = df_delivered.groupby('year_month').agg({
        'total_price': 'sum',
        'profit': 'sum',
        'order_id': 'count',
        'customer_id': 'nunique'
    }).round(2)
    
    monthly_trends.columns = ['CA', 'Profit', 'Nb_commandes', 'Nb_clients']
    
    return monthly_trends


def analyze_customer_segments(df):
    """
    Segmentation des clients (RFM simplifié)
    R = Recency (récence), F = Frequency (fréquence), M = Monetary (montant)
    """
    df_delivered = df[df['status'] == 'Livrée'].copy()
    
    # Assurer que la colonne date est au bon format
    df_delivered['date'] = pd.to_datetime(df_delivered['date'])
    
    # Calculer les métriques par client
    customer_metrics = df_delivered.groupby('customer_id').agg({
        'date': 'max',  # Date dernière commande
        'order_id': 'count',  # Nombre de commandes
        'total_price': 'sum'  # CA total
    }).round(2)
    
    customer_metrics.columns = ['derniere_commande', 'nb_commandes', 'ca_total']
    
    # Calculer la récence (jours depuis dernière commande)
    max_date = df_delivered['date'].max()
    customer_metrics['recence_jours'] = (max_date - customer_metrics['derniere_commande']).dt.days
    
    # Segmenter les clients
    # VIP: >5 commandes OU >$2000 CA
    # Réguliers: 3-5 commandes
    # Occasionnels: 1-2 commandes
    def segment_customer(row):
        if row['nb_commandes'] > 5 or row['ca_total'] > 2000:
            return 'VIP'
        elif row['nb_commandes'] >= 3:
            return 'Régulier'
        else:
            return 'Occasionnel'
    
    customer_metrics['segment'] = customer_metrics.apply(segment_customer, axis=1)
    
    # Résumé par segment
    segment_summary = customer_metrics.groupby('segment').agg({
        'ca_total': ['sum', 'mean'],
        'nb_commandes': ['sum', 'mean'],
        'recence_jours': 'mean'
    }).round(2)
    
    return customer_metrics, segment_summary


def generate_analysis_report(df):
    """
    Génère un rapport d'analyse complet
    """
    print("\n" + "=" * 70)
    print("RAPPORT D'ANALYSE DES VENTES")
    print("=" * 70)
    
    # KPI globaux
    kpis = calculate_kpis(df)
    print("\n📊 KPI GLOBAUX:")
    print(f"  • Chiffre d'affaires: ${kpis['chiffre_affaires']:,.2f}")
    print(f"  • Profit total: ${kpis['profit_total']:,.2f}")
    print(f"  • Marge moyenne: {kpis['marge_moyenne']:.2f}%")
    print(f"  • Nombre de ventes: {kpis['nombre_ventes']:,}")
    print(f"  • Panier moyen: ${kpis['panier_moyen']:.2f}")
    print(f"  • Nombre de clients: {kpis['nombre_clients']:,}")
    print(f"  • CA par client: ${kpis['ca_par_client']:.2f}")
    print(f"  • Taux d'annulation: {kpis['taux_annulation']:.2f}%")
    
    # Analyse par catégorie
    print("\n📦 TOP 3 CATÉGORIES:")
    cat_analysis = analyze_by_category(df)
    for cat, row in cat_analysis.head(3).iterrows():
        print(f"  • {cat}: ${row['CA_total']:,.2f} (Marge: {row['Marge_%']:.2f}%)")
    
    # Analyse par région
    print("\n🌍 TOP 3 RÉGIONS:")
    region_analysis = analyze_by_region(df)
    for region, row in region_analysis.head(3).iterrows():
        print(f"  • {region}: ${row['CA_total']:,.2f} ({row['Nb_clients']} clients)")
    
    # Analyse par canal
    print("\n💻 PERFORMANCE PAR CANAL:")
    channel_analysis = analyze_by_channel(df)
    for channel, row in channel_analysis.iterrows():
        print(f"  • {channel}: ${row['CA_total']:,.2f} (Marge: {row['Marge_%']:.2f}%)")
    
    # Top produits
    print("\n🏆 TOP 5 PRODUITS:")
    product_analysis = analyze_by_product(df, top_n=5)
    for product, row in product_analysis.iterrows():
        print(f"  • {product}: ${row['CA_total']:,.2f} ({row['Quantité_vendue']} unités)")
    
    # Segments clients
    customer_metrics, segment_summary = analyze_customer_segments(df)
    print("\n👥 SEGMENTS CLIENTS:")
    segment_counts = customer_metrics['segment'].value_counts()
    for segment in segment_summary.index:
        ca_sum = segment_summary.loc[segment, ('ca_total', 'sum')]
        nb_clients = segment_counts.get(segment, 0)
        print(f"  • {segment}: ${ca_sum:,.2f} ({nb_clients} clients)")
    
    print("\n" + "=" * 70)
    
    return {
        'kpis': kpis,
        'category': cat_analysis,
        'region': region_analysis,
        'channel': channel_analysis,
        'product': product_analysis
    }


# Exécution si appelé directement
if __name__ == "__main__":
    df = load_sales_data()
    
    if df is not None:
        report = generate_analysis_report(df)
