"""
Sanity checks op de dataset en het baseline-model:
1. Zitten er (bijna-)duplicaten in de dataset? Dat zou de testscore kunstmatig
   ophogen, omdat de testset dan rijen bevat die (bijna) letterlijk ook in de
   trainset staan.
2. Hoe stabiel is de accuracy over meerdere, verschillende train/test-splits
   (cross-validation), in plaats van maar één toevallige split?
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from src.feature_lists import URL_ONLY_FEATURES, LABEL_COLUMN

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phiusiil_phishing_urls.csv")


def main():
    df = pd.read_csv(DATA_PATH)

    # --- Check 1: exacte duplicaten op basis van de URL-only features ---
    print("--- Check 1: duplicaten in de features ---")
    feature_data = df[URL_ONLY_FEATURES]
    n_duplicates = feature_data.duplicated().sum()
    print(f"Aantal rijen met exact dezelfde URL-only kenmerken als een andere rij: {n_duplicates}")
    print(f"Dat is {n_duplicates / len(df) * 100:.1f}% van de dataset.")

    # --- Check 2: cross-validation in plaats van één split ---
    print("\n--- Check 2: 5-voudige cross-validation ---")
    X = df[URL_ONLY_FEATURES].copy()
    top_tlds = X["TLD"].value_counts().nlargest(20).index
    X["TLD"] = X["TLD"].where(X["TLD"].isin(top_tlds), other="overig")
    X = pd.get_dummies(X, columns=["TLD"], prefix="TLD")
    y = df[LABEL_COLUMN]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LogisticRegression(max_iter=1000, random_state=42)
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(model, X_scaled, y, cv=cv, scoring="accuracy")

    print(f"Accuracy per fold: {[f'{s:.4f}' for s in scores]}")
    print(f"Gemiddelde: {scores.mean():.4f}  (std: {scores.std():.4f})")


if __name__ == "__main__":
    main()
