"""
Générateur de dashboards interactifs pour visualiser les ventes
Utilise matplotlib et plotly pour créer des graphiques
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import os


# Configurer le style matplotlib
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


def create_sales_overview_chart(df, kpis, save_path='../dashboards/sales_overview.png'):
    """
    Crée un graphique de vue d'ensemble avec les KPI principaux
    """
    print("Création du graphique de vue d'ensemble...")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle('Vue d\'ensemble des ventes', fontsize=20, fontweight='bold', y=0.98)
    
    # 1. KPI principaux en texte
    ax = axes[0, 0]
    ax.axis('off')
    
    kpi_text = f"""
    📊 KPI PRINCIPAUX
    
    Chiffre d'affaires:    ${kpis['chiffre_affaires']:,.0f}
    Profit total:          ${kpis['profit_total']:,.0f}
    Marge moyenne:         {kpis['marge_moyenne']:.1f}%
    
    Nombre de ventes:      {kpis['nombre_ventes']:,}
    Panier moyen:          ${kpis['panier_moyen']:.2f}
    
    Nombre de clients:     {kpis['nombre_clients']:,}
    CA par client:         ${kpis['ca_par_client']:.2f}
    """
    
    ax.text(0.1, 0.5, kpi_text, fontsize=14, verticalalignment='center',
            family='monospace', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.3))
    
    # 2. Ventes par catégorie
    df_delivered = df[df['status'] == 'Livrée']
    category_sales = df_delivered.groupby('category')['total_price'].sum().sort_values(ascending=True)
    
    ax = axes[0, 1]
    category_sales.plot(kind='barh', ax=ax, color='steelblue')
    ax.set_title('Chiffre d\'affaires par catégorie', fontsize=14, fontweight='bold')
    ax.set_xlabel('Chiffre d\'affaires ($)')
    ax.set_ylabel('')
    
    # 3. Ventes par région
    region_sales = df_delivered.groupby('region')['total_price'].sum().sort_values(ascending=True)
    
    ax = axes[1, 0]
    colors = plt.cm.Set3(range(len(region_sales)))
    region_sales.plot(kind='barh', ax=ax, color=colors)
    ax.set_title('Chiffre d\'affaires par région', fontsize=14, fontweight='bold')
    ax.set_xlabel('Chiffre d\'affaires ($)')
    ax.set_ylabel('')
    
    # 4. Ventes par canal
    channel_sales = df_delivered.groupby('channel')['total_price'].sum()
    
    ax = axes[1, 1]
    colors_pie = plt.cm.Pastel1(range(len(channel_sales)))
    wedges, texts, autotexts = ax.pie(channel_sales, labels=channel_sales.index, autopct='%1.1f%%',
                                        colors=colors_pie, startangle=90)
    ax.set_title('Répartition par canal de vente', fontsize=14, fontweight='bold')
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Graphique sauvegardé: {save_path}")


def create_time_series_chart(df, save_path='../dashboards/time_series.png'):
    """
    Graphique d'évolution temporelle des ventes
    """
    print("Création du graphique d'évolution temporelle...")
    
    df_delivered = df[df['status'] == 'Livrée'].copy()
    df_delivered['date'] = pd.to_datetime(df_delivered['date'])
    df_delivered['year_month'] = df_delivered['date'].dt.to_period('M').astype(str)
    
    monthly_data = df_delivered.groupby('year_month').agg({
        'total_price': 'sum',
        'profit': 'sum',
        'order_id': 'count'
    }).reset_index()
    
    fig, axes = plt.subplots(2, 1, figsize=(16, 10))
    fig.suptitle('Évolution temporelle des ventes', fontsize=18, fontweight='bold')
    
    # CA et profit
    ax = axes[0]
    ax.plot(monthly_data['year_month'], monthly_data['total_price'], 
            marker='o', linewidth=2, label='Chiffre d\'affaires', color='steelblue')
    ax.fill_between(range(len(monthly_data)), monthly_data['total_price'], alpha=0.3, color='steelblue')
    
    ax2 = ax.twinx()
    ax2.plot(monthly_data['year_month'], monthly_data['profit'], 
             marker='s', linewidth=2, label='Profit', color='green')
    
    ax.set_title('Chiffre d\'affaires et profit mensuel', fontsize=14, fontweight='bold')
    ax.set_xlabel('Mois')
    ax.set_ylabel('Chiffre d\'affaires ($)', color='steelblue')
    ax2.set_ylabel('Profit ($)', color='green')
    ax.tick_params(axis='x', rotation=45)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    # Nombre de commandes
    ax = axes[1]
    ax.bar(monthly_data['year_month'], monthly_data['order_id'], color='coral', alpha=0.7)
    ax.set_title('Nombre de commandes mensuelles', fontsize=14, fontweight='bold')
    ax.set_xlabel('Mois')
    ax.set_ylabel('Nombre de commandes')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Graphique sauvegardé: {save_path}")


def create_product_performance_chart(df, top_n=10, save_path='../dashboards/product_performance.png'):
    """
    Graphique de performance des produits
    """
    print("Création du graphique de performance produits...")
    
    df_delivered = df[df['status'] == 'Livrée']
    
    product_data = df_delivered.groupby('product').agg({
        'total_price': 'sum',
        'quantity': 'sum',
        'profit': 'sum',
        'margin_percent': 'mean'
    }).sort_values('total_price', ascending=False).head(top_n)
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    fig.suptitle(f'Top {top_n} produits - Performance', fontsize=18, fontweight='bold')
    
    # CA par produit
    ax = axes[0, 0]
    product_data['total_price'].plot(kind='barh', ax=ax, color='steelblue')
    ax.set_title('Chiffre d\'affaires', fontsize=12, fontweight='bold')
    ax.set_xlabel('CA ($)')
    
    # Quantité vendue
    ax = axes[0, 1]
    product_data['quantity'].plot(kind='barh', ax=ax, color='coral')
    ax.set_title('Quantités vendues', fontsize=12, fontweight='bold')
    ax.set_xlabel('Unités')
    
    # Profit
    ax = axes[1, 0]
    product_data['profit'].plot(kind='barh', ax=ax, color='green')
    ax.set_title('Profit généré', fontsize=12, fontweight='bold')
    ax.set_xlabel('Profit ($)')
    
    # Marge
    ax = axes[1, 1]
    product_data['margin_percent'].plot(kind='barh', ax=ax, color='purple')
    ax.set_title('Marge moyenne (%)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Marge (%)')
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Graphique sauvegardé: {save_path}")


def create_interactive_dashboard(df, save_path='../dashboards/interactive_dashboard.html'):
    """
    Crée un dashboard interactif avec Plotly
    """
    print("Création du dashboard interactif...")
    
    df_delivered = df[df['status'] == 'Livrée'].copy()
    df_delivered['date'] = pd.to_datetime(df_delivered['date'])
    
    # Créer une grille de sous-graphiques
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('CA par catégorie', 'Évolution mensuelle', 
                        'Top 10 produits', 'Répartition par région'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "bar"}, {"type": "pie"}]]
    )
    
    # 1. CA par catégorie
    cat_sales = df_delivered.groupby('category')['total_price'].sum().sort_values(ascending=False)
    fig.add_trace(
        go.Bar(x=cat_sales.index, y=cat_sales.values, name='Catégorie',
               marker_color='steelblue'),
        row=1, col=1
    )
    
    # 2. Évolution mensuelle
    df_delivered['year_month'] = df_delivered['date'].dt.to_period('M').astype(str)
    monthly = df_delivered.groupby('year_month')['total_price'].sum()
    fig.add_trace(
        go.Scatter(x=monthly.index, y=monthly.values, mode='lines+markers',
                   name='CA mensuel', line=dict(color='green', width=3)),
        row=1, col=2
    )
    
    # 3. Top 10 produits
    top_products = df_delivered.groupby('product')['total_price'].sum().nlargest(10)
    fig.add_trace(
        go.Bar(x=top_products.values, y=top_products.index, orientation='h',
               name='Produits', marker_color='coral'),
        row=2, col=1
    )
    
    # 4. Répartition par région
    region_sales = df_delivered.groupby('region')['total_price'].sum()
    fig.add_trace(
        go.Pie(labels=region_sales.index, values=region_sales.values, name='Région'),
        row=2, col=2
    )
    
    # Mise à jour du layout
    fig.update_layout(
        title_text="Dashboard interactif des ventes",
        title_font_size=24,
        height=800,
        showlegend=False
    )
    
    # Sauvegarder
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    fig.write_html(save_path)
    
    print(f"✓ Dashboard interactif sauvegardé: {save_path}")


def generate_all_dashboards(df, kpis):
    """
    Génère tous les dashboards
    """
    print("\n" + "=" * 70)
    print("GÉNÉRATION DES DASHBOARDS")
    print("=" * 70)
    
    create_sales_overview_chart(df, kpis)
    create_time_series_chart(df)
    create_product_performance_chart(df)
    create_interactive_dashboard(df)
    
    print("\n" + "=" * 70)
    print("✓ TOUS LES DASHBOARDS GÉNÉRÉS")
    print("=" * 70)


# Test
if __name__ == "__main__":
    from sales_analyzer import load_sales_data, calculate_kpis
    
    df = load_sales_data()
    if df is not None:
        kpis = calculate_kpis(df)
        generate_all_dashboards(df, kpis)
