import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

URL = "https://www.sikafinance.com/marches/historiques/ORAC.ci"

# Récupération des données
def fetch_data(url):
    tables = pd.read_html(url)
    df = tables[0]
    return df

df = fetch_data(URL)

# Nettoyage (important)
df['Clôture'] = (
    df['Clôture']
    .astype(str)
    .str.replace('\xa0', '', regex=False)  # espaces insécables
    .str.replace(' ', '', regex=False)     # espaces normaux
    .str.replace(',', '.', regex=False)    # virgule → point
)

df['Clôture'] = pd.to_numeric(df['Clôture'], errors='coerce')

# Calcul du rendement
def calculate_returns(dataframe):
    dataframe['Returns'] = dataframe['Clôture'].pct_change()
    return dataframe

df = calculate_returns(df)

# Affichage des 5 premières lignes
print(df.head())

# Volatilité annualisée
volatility = df['Returns'].std() * np.sqrt(252)
print(f"Volatilité annualisée d'Orange CI : {volatility:.2%}")

# Graphique
plt.figure(figsize=(12, 6))
plt.plot(df['Clôture'], label='Prix de Clôture')
plt.plot(df['Clôture'].rolling(window=20).mean(), label='Moyenne Mobile 20 jours')
plt.title("Analyse de tendance : Orange Côte d'Ivoire")
plt.legend()
plt.grid(True)
plt.show()
# Paramètres
risk_free_rate = 0.03  # 3% annuel
trading_days = 252

# Rendement moyen annualisé
mean_return_annual = df['Returns'].mean() * trading_days

# Volatilité annualisée
volatility_annual = df['Returns'].std() * np.sqrt(trading_days)

# Sharpe Ratio
sharpe_ratio = (mean_return_annual - risk_free_rate) / volatility_annual

print(f"Sharpe Ratio (Orange CI) : {sharpe_ratio:.2f}")







