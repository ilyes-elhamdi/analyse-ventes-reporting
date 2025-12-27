# 📊 Analyse des Ventes et Reporting Dynamique

Projet d'analyse de données de ventes avec génération automatique de rapports et dashboards interactifs.

## 📋 Description

Ce projet fournit une solution complète pour **analyser les données de ventes** et générer des **rapports visuels** et **dashboards interactifs**. Il combine analyse de données avec Pandas, visualisations avec Matplotlib/Seaborn, et dashboards interactifs avec Plotly.

### 🎯 Fonctionnalités principales :
- Génération de données de ventes synthétiques réalistes
- Calcul automatique des KPI (Chiffre d'affaires, profit, marge, etc.)
- Analyses multidimensionnelles (produits, régions, canaux, temps)
- Segmentation clients (VIP, Réguliers, Occasionnels)
- Dashboards statiques (PNG) et interactifs (HTML)

## 🛠️ Technologies utilisées

- **Pandas** : Manipulation et analyse de données
- **NumPy** : Calculs numériques
- **Matplotlib & Seaborn** : Visualisations statiques
- **Plotly** : Dashboards interactifs
- **OpenPyXL** : Export Excel

## 📁 Structure du projet

```
analyse-ventes-reporting/
│
├── src/
│   ├── data_generator.py      # Génération de données synthétiques
│   ├── sales_analyzer.py      # Analyse et calcul des KPI
│   └── dashboard_generator.py # Création des dashboards
│
├── data/
│   └── sales_data.csv         # Dataset de ventes (généré)
│
├── dashboards/                # Dashboards générés
│   ├── sales_overview.png
│   ├── time_series.png
│   ├── product_performance.png
│   └── interactive_dashboard.html
│
├── reports/                   # Rapports générés
├── requirements.txt
└── README.md
```

## 🚀 Installation

1. Cloner le repository :
```bash
git clone https://github.com/ilyes-elhamdi/analyse-ventes-reporting.git
cd analyse-ventes-reporting
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## 💻 Utilisation

### 1. Générer les données de ventes

```bash
cd src
python data_generator.py
```

Cela génère un fichier `data/sales_data.csv` avec 10,000 enregistrements de ventes.

### 2. Analyser les données

```bash
python sales_analyzer.py
```

Affiche un rapport complet avec tous les KPI et analyses.

### 3. Générer les dashboards

```bash
python dashboard_generator.py
```

Crée 4 dashboards :
- Vue d'ensemble (KPI + graphiques principaux)
- Évolution temporelle
- Performance produits
- Dashboard interactif (HTML)

### Utilisation dans le code

```python
# Générer des données
from data_generator import generate_sales_data
df = generate_sales_data(n_records=10000)

# Analyser
from sales_analyzer import calculate_kpis, generate_analysis_report
kpis = calculate_kpis(df)
report = generate_analysis_report(df)

# Créer des dashboards
from dashboard_generator import generate_all_dashboards
generate_all_dashboards(df, kpis)
```

## 📊 KPI calculés

### KPI principaux :
- **Chiffre d'affaires** : CA total des ventes livrées
- **Profit total** : Marge totale générée
- **Marge moyenne** : Pourcentage de marge moyen
- **Panier moyen** : Valeur moyenne par commande
- **CA par client** : Revenu moyen par client
- **Taux d'annulation** : % de commandes annulées

### Analyses disponibles :
- ✅ Analyse par catégorie de produits
- ✅ Analyse par région géographique
- ✅ Analyse par canal de vente (Online, Magasin, etc.)
- ✅ Analyse par produit (top performers)
- ✅ Évolution temporelle (mensuelle)
- ✅ Segmentation clients (RFM)

## 📈 Exemples de visualisations

### Dashboard de vue d'ensemble
- KPI principaux en grand format
- CA par catégorie (barres horizontales)
- CA par région (barres horizontales colorées)
- Répartition par canal (camembert)

### Graphique d'évolution temporelle
- CA et profit mensuel (courbes avec zones remplies)
- Nombre de commandes mensuelles (barres)

### Performance produits (Top 10)
- CA par produit
- Quantités vendues
- Profit généré
- Marge moyenne

### Dashboard interactif (Plotly)
- Graphiques interactifs avec zoom, hover, etc.
- Export en HTML pour partage facile

## 🔧 Fonctionnalités

- ✅ Génération de données réalistes (12 produits, 5 régions, 4 canaux)
- ✅ Dataset configurable (nombre d'enregistrements, période)
- ✅ Calcul automatique de 8+ KPI
- ✅ 6 types d'analyses différentes
- ✅ Segmentation clients automatique
- ✅ 4 types de dashboards différents
- ✅ Dashboards statiques (PNG) et interactifs (HTML)
- ✅ Code commenté et modulaire

## 📝 Dataset généré

Le dataset contient les colonnes suivantes :
- `order_id` : ID unique de commande
- `date` : Date de la commande
- `customer_id` : ID du client
- `product` : Nom du produit
- `category` : Catégorie (Électronique, Accessoires, Stockage)
- `quantity` : Quantité commandée
- `unit_price` / `total_price` : Prix unitaire et total
- `unit_cost` / `total_cost` : Coût unitaire et total
- `profit` : Profit (prix - coût)
- `margin_percent` : Marge en pourcentage
- `region` : Région (Nord, Sud, Est, Ouest, Centre)
- `channel` : Canal (Online, Magasin, Revendeur, Direct)
- `status` : Statut (Livrée, En cours, Annulée)

## 🎓 Concepts utilisés

- **Analyse de données** : Pandas pour manipulation de données
- **KPI** : Métriques clés de performance
- **Agrégation** : GroupBy pour analyses multidimensionnelles
- **Segmentation RFM** : Recency, Frequency, Monetary
- **Visualisation** : Matplotlib (statique) + Plotly (interactif)
- **Time series** : Analyse des tendances temporelles

## 📈 Améliorations possibles

- [ ] Export Power BI (.pbix) avec modèle pré-configuré
- [ ] Prévisions avec machine learning
- [ ] Détection d'anomalies
- [ ] Analyse de panier (market basket analysis)
- [ ] Rapport PDF automatique
- [ ] Interface web avec Streamlit/Dash
- [ ] Connexion à bases de données réelles

## 👤 Auteur

**Ilyes Elhamdi**
- LinkedIn: [ilyes-elhamdi](https://www.linkedin.com/in/ilyes-elhamdi-320202248)
- Email: ilyeshamdi48@gmail.com

## 📄 Licence

Projet personnel - libre d'utilisation à des fins éducatives
