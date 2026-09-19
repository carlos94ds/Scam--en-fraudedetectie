"""
Traint het productiemodel opnieuw, maar nu met onze EIGEN feature-extractie
(src/feature_extraction.py) in plaats van de vooraf berekende kolommen uit
de PhiUSIIL-dataset. Zo zijn trainen en het live gebruik in de webapp altijd
consistent met elkaar.
"""
import sys
import os
import json

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report

from src.feature_lists import LABEL_COLUMN
from src.feature_extraction import extract_full_features

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "phiusiil_phishing_urls.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "models")
RANDOM_STATE = 42

FEATURE_ORDER = [
    "URLLength", "DomainLength", "IsDomainIP", "TLDLength", "NoOfSubDomain",
    "HasObfuscation", "NoOfObfuscatedChar", "ObfuscationRatio",
    "NoOfLettersInURL", "LetterRatioInURL", "NoOfDegitsInURL", "DegitRatioInURL",
    "NoOfEqualsInURL", "NoOfQMarkInURL", "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL", "SpacialCharRatioInURL", "IsHTTPS",
    "CharContinuationRate", "URLCharProb", "TLDLegitimateProb",
]


def build_tld_probability_table(train_df, tld_series):
    combined = pd.DataFrame({"TLD": tld_series, "label": train_df[LABEL_COLUMN].values})
    grouped = combined.groupby("TLD")["label"].mean()  # aandeel legitiem per TLD
    return grouped.to_dict(), train_df[LABEL_COLUMN].mean()


def build_char_frequency_table(urls):
    from collections import Counter
    counter = Counter()
    total = 0
    for url in urls:
        counter.update(url)
        total += len(url)
    return {ch: count / total for ch, count in counter.items()}, 1 / max(total, 1)


def main():
    df = pd.read_csv(DATA_PATH)
    print("Ruwe features berekenen uit de URL-tekst zelf...")

    # Eerst de TLD en de basiskenmerken voor iedere rij berekenen
    base_rows = [extract_base_features(url) if False else None for url in df["URL"]]
    from src.feature_extraction import extract_base_features
    base_rows = [extract_base_features(url) for url in df["URL"]]
    base_df = pd.DataFrame(base_rows)

    # --- Train/test split EERST, referentietabellen alleen op trainingsdata ---
    train_idx, test_idx = train_test_split(
        df.index, test_size=0.2, random_state=RANDOM_STATE, stratify=df[LABEL_COLUMN]
    )

    tld_prob_table, default_tld_prob = build_tld_probability_table(
        df.loc[train_idx], base_df.loc[train_idx, "TLD"]
    )
    char_freq_table, default_char_prob = build_char_frequency_table(df.loc[train_idx, "URL"])

    print("Volledige featureset berekenen (incl. TLD-kans en teken-kans)...")
    base_df["URLCharProb"] = df["URL"].apply(
        lambda u: sum(char_freq_table.get(c, default_char_prob) for c in u) / max(len(u), 1)
    )
    base_df["TLDLegitimateProb"] = base_df["TLD"].map(tld_prob_table).fillna(default_tld_prob)

    X = base_df[FEATURE_ORDER]
    y = df[LABEL_COLUMN]

    X_train, X_test = X.loc[train_idx], X.loc[test_idx]
    y_train, y_test = y.loc[train_idx], y.loc[test_idx]

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    print("\n--- Resultaten met zelf-berekende features (productiemodel) ---")
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"F1-score:  {f1_score(y_test, y_pred):.4f}")
    print("\n" + classification_report(y_test, y_pred, target_names=["Phishing", "Legitiem"]))

    # --- Opslaan: model, scaler, en de referentietabellen die de webapp nodig heeft ---
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, os.path.join(MODEL_DIR, "production_model.pkl"))
    joblib.dump(scaler, os.path.join(MODEL_DIR, "production_scaler.pkl"))
    joblib.dump(FEATURE_ORDER, os.path.join(MODEL_DIR, "production_feature_order.pkl"))

    with open(os.path.join(MODEL_DIR, "tld_probability_table.json"), "w") as f:
        json.dump({"table": tld_prob_table, "default": default_tld_prob}, f)

    with open(os.path.join(MODEL_DIR, "char_frequency_table.json"), "w") as f:
        json.dump({"table": char_freq_table, "default": default_char_prob}, f)

    print(f"\nProductiemodel en referentietabellen opgeslagen in: {MODEL_DIR}")


if __name__ == "__main__":
    main()
